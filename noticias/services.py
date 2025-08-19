import re
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
import json

class RelevanciaService:
    """Serviço para calcular relevância automática das notícias"""
    
    def __init__(self):
        self.tendencias_cache = {}
        self.cache_expiry = None
        self.tendencias_url = "https://trends.google.com/trends/api/dailytrends"
        
    def calcular_relevancia(self, noticia):
        """Calcula score de relevância de 0 a 10"""
        score = 0.0
        
        # 1. Análise de palavras-chave (30%)
        palavras_score = self._analisar_palavras_chave(noticia)
        score += palavras_score * 0.3
        
        # 2. Análise de tendências (40%)
        tendencias_score = self._analisar_tendencias(noticia)
        score += tendencias_score * 0.4
        
        # 3. Análise de conteúdo (20%)
        conteudo_score = self._analisar_conteudo(noticia)
        score += conteudo_score * 0.2
        
        # 4. Análise temporal (10%)
        temporal_score = self._analisar_temporal(noticia)
        score += temporal_score * 0.1
        
        return round(score, 2)
    
    def _analisar_palavras_chave(self, noticia):
        """Analisa palavras-chave importantes"""
        score = 0.0
        
        # Palavras de alta relevância
        palavras_importantes = [
            'urgente', 'breaking', 'exclusivo', 'política', 'economia',
            'tecnologia', 'saúde', 'educação', 'meio ambiente', 'cultura',
            'esporte', 'entretenimento', 'internacional', 'nacional'
        ]
        
        texto_completo = f"{noticia.titulo} {noticia.resumo} {noticia.conteudo}".lower()
        
        for palavra in palavras_importantes:
            if palavra in texto_completo:
                score += 1.0
        
        # Normaliza para 0-10
        return min(score, 10.0)
    
    def _analisar_tendencias(self, noticia):
        """Analisa tendências atuais do Google"""
        try:
            if not self._cache_valido():
                self._atualizar_tendencias()
            
            score = 0.0
            texto_completo = f"{noticia.titulo} {noticia.resumo}".lower()
            
            # Verifica se palavras da notícia estão nas tendências
            for tendencia in self.tendencias_cache.get('trendingSearchesDays', []):
                for search in tendencia.get('trendingSearches', []):
                    query = search.get('title', {}).get('query', '').lower()
                    if query in texto_completo:
                        score += 2.0
            
            return min(score, 10.0)
            
        except Exception as e:
            print(f"Erro ao analisar tendências: {e}")
            return 5.0  # Score médio em caso de erro
    
    def _analisar_conteudo(self, noticia):
        """Analisa qualidade e extensão do conteúdo"""
        score = 0.0
        
        # Tamanho do título (não muito curto, não muito longo)
        if 20 <= len(noticia.titulo) <= 100:
            score += 2.0
        
        # Tamanho do resumo
        if 100 <= len(noticia.resumo) <= 300:
            score += 2.0
        
        # Tamanho do conteúdo
        if len(noticia.conteudo) > 500:
            score += 3.0
        
        # Presença de números/dados
        if re.search(r'\d+', noticia.conteudo):
            score += 1.0
        
        # Presença de citações
        if '"' in noticia.conteudo or "'" in noticia.conteudo:
            score += 1.0
        
        # Presença de links ou referências
        if 'http' in noticia.conteudo or 'www' in noticia.conteudo:
            score += 1.0
        
        return min(score, 10.0)
    
    def _analisar_temporal(self, noticia):
        """Analisa relevância temporal"""
        score = 0.0
        
        # Notícia muito recente (últimas 24h)
        if noticia.data_publicacao >= timezone.now() - timedelta(days=1):
            score += 3.0
        # Notícia recente (última semana)
        elif noticia.data_publicacao >= timezone.now() - timedelta(days=7):
            score += 2.0
        # Notícia do mês
        elif noticia.data_publicacao >= timezone.now() - timedelta(days=30):
            score += 1.0
        
        # Verifica se é notícia de fim de semana (menos relevante)
        if noticia.data_publicacao.weekday() >= 5:  # Sábado ou domingo
            score -= 1.0
        
        return max(score, 0.0)
    
    def _cache_valido(self):
        """Verifica se o cache de tendências ainda é válido"""
        if not self.cache_expiry:
            return False
        return timezone.now() < self.cache_expiry
    
    def _atualizar_tendencias(self):
        """Atualiza cache de tendências do Google"""
        try:
            # Simula tendências (em produção, usar API real)
            self.tendencias_cache = {
                'trendingSearchesDays': [
                    {
                        'trendingSearches': [
                            {'title': {'query': 'tecnologia'}},
                            {'title': {'query': 'política'}},
                            {'title': {'query': 'economia'}},
                            {'title': {'query': 'saúde'}},
                            {'title': {'query': 'educação'}},
                            {'title': {'query': 'meio ambiente'}},
                            {'title': {'query': 'cultura'}},
                            {'title': {'query': 'esporte'}},
                            {'title': {'query': 'internacional'}},
                            {'title': {'query': 'nacional'}}
                        ]
                    }
                ]
            }
            
            # Cache válido por 1 hora
            self.cache_expiry = timezone.now() + timedelta(hours=1)
            
        except Exception as e:
            print(f"Erro ao atualizar tendências: {e}")
            # Fallback para tendências básicas
            self.tendencias_cache = {'trendingSearchesDays': []}
    
    def extrair_palavras_chave(self, noticia):
        """Extrai palavras-chave da notícia"""
        texto = f"{noticia.titulo} {noticia.resumo}"
        
        # Remove palavras comuns
        palavras_comuns = ['a', 'o', 'e', 'de', 'da', 'do', 'em', 'um', 'uma', 'com', 'para', 'por', 'que', 'se', 'não', 'mais', 'como', 'mas', 'foi', 'são', 'está', 'pode', 'ser', 'tem', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'quando', 'muito', 'nos', 'já', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'era', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'suas', 'minha', 'têm', 'naquele', 'neles', 'estavam', 'fosse', 'nessa', 'nesses', 'nessa', 'numa', 'disso', 'aquela', 'àquela', 'estivessem', 'fossem', 'estivesse', 'tivesse', 'estivessem', 'tivessem', 'houvesse', 'houvessem', 'houver', 'haver', 'haveria', 'haveriam', 'haja', 'hajam', 'tenha', 'tenham', 'terei', 'terá', 'terão', 'teria', 'teriam', 'terei', 'terá', 'terão', 'teria', 'teriam', 'quero', 'quer', 'querem', 'queria', 'queriam', 'deseje', 'deseja', 'desejem', 'desejaria', 'desejariam', 'preciso', 'precisa', 'precisam', 'precisaria', 'precisariam', 'gostaria', 'gostariam', 'gosto', 'gosta', 'gostam', 'gostaria', 'gostariam', 'adoro', 'adora', 'adoram', 'adoraria', 'adorariam', 'detesto', 'detesta', 'detestam', 'detestaria', 'detestariam', 'odeio', 'odeia', 'odeiam', 'odearia', 'odeariam', 'amo', 'ama', 'amam', 'amaria', 'amariam', 'gosto', 'gosta', 'gostam', 'gostaria', 'gostariam', 'adoro', 'adora', 'adoram', 'adoraria', 'adorariam', 'detesto', 'detesta', 'detestam', 'detestaria', 'detestariam', 'odeio', 'odeia', 'odeiam', 'odearia', 'odeariam', 'amo', 'ama', 'amam', 'amaria', 'amariam']
        
        # Divide o texto em palavras
        palavras = re.findall(r'\b\w+\b', texto.lower())
        
        # Filtra palavras relevantes
        palavras_relevantes = []
        for palavra in palavras:
            if (len(palavra) > 3 and 
                palavra not in palavras_comuns and 
                palavra not in palavras_relevantes):
                palavras_relevantes.append(palavra)
        
        # Retorna as 10 palavras mais relevantes
        return ', '.join(palavras_relevantes[:10])
    
    def atualizar_relevancia_todas(self):
        """Atualiza relevância de todas as notícias"""
        from .models import Noticia
        
        noticias = Noticia.objects.filter(publicada=True)
        for noticia in noticias:
            noticia.calcular_relevancia()
        
        return f"Relevância atualizada para {noticias.count()} notícias"
