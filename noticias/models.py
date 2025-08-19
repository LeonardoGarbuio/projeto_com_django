from django.db import models
from django.urls import reverse
from django.utils import timezone

class Noticia(models.Model):
    titulo = models.CharField(max_length=200, verbose_name='Título')
    resumo = models.TextField(max_length=500, verbose_name='Resumo')
    conteudo = models.TextField(verbose_name='Conteúdo')
    imagem = models.ImageField(upload_to='noticias/', verbose_name='Imagem da Notícia', blank=False, null=False)
    destaque = models.BooleanField(default=False, verbose_name='Notícia em Destaque')
    relevancia_score = models.FloatField(default=0.0, verbose_name='Score de Relevância')
    palavras_chave = models.TextField(blank=True, verbose_name='Palavras-chave Extraídas')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_publicacao = models.DateTimeField(default=timezone.now, verbose_name='Data de Publicação')
    publicada = models.BooleanField(default=True, verbose_name='Publicada')

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('noticias:noticia_detalhe', args=[str(self.id)])

    def calcular_relevancia(self):
        """Calcula automaticamente a relevância da notícia"""
        from .services import RelevanciaService
        service = RelevanciaService()
        self.relevancia_score = service.calcular_relevancia(self)
        self.palavras_chave = service.extrair_palavras_chave(self)
        
        # Marca como destaque se score > 7.0
        self.destaque = self.relevancia_score >= 7.0
        self.save()

    @property
    def tempo_atras(self):
        """Retorna o tempo decorrido desde a publicação"""
        if self.data_publicacao:
            delta = timezone.now() - self.data_publicacao
            if delta.days > 0:
                return f"{delta.days} dia{'s' if delta.days > 1 else ''} atrás"
            elif delta.seconds > 3600:
                horas = delta.seconds // 3600
                return f"{horas} hora{'s' if horas > 1 else ''} atrás"
            elif delta.seconds > 60:
                minutos = delta.seconds // 60
                return f"{minutos} minuto{'s' if minutos > 1 else ''} atrás"
            else:
                return "Agora mesmo"
        return ""

    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'
        ordering = ['-relevancia_score', '-data_publicacao']
