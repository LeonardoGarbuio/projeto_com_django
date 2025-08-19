from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from .models import Noticia
from .forms import NoticiaForm
from django.utils import timezone

class NoticiaListView(ListView):
    model = Noticia
    template_name = 'noticias/lista_noticias.html'
    context_object_name = 'noticias'
    paginate_by = 10

    def get_queryset(self):
        queryset = Noticia.objects.filter(publicada=True)
        
        # Implementar pesquisa
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(titulo__icontains=q) |
                Q(resumo__icontains=q) |
                Q(conteudo__icontains=q)
            )
        
        return queryset.order_by('-data_publicacao')

class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = 'noticias/detalhe_noticia.html'
    context_object_name = 'noticia'

    def get_queryset(self):
        return Noticia.objects.filter(publicada=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionar notícias relacionadas (excluindo a atual)
        context['noticias_relacionadas'] = Noticia.objects.filter(
            publicada=True
        ).exclude(
            id=self.object.id
        ).order_by('-data_publicacao')[:3]
        return context

def home(request):
    # Buscar notícias em destaque (marcadas manualmente como destaque)
    noticias_destaque = Noticia.objects.filter(
        publicada=True,
        destaque=True
    ).order_by('-data_publicacao')[:3]
    
    # Buscar notícias recentes (todas as mais recentes, incluindo novas)
    noticias_recentes = Noticia.objects.filter(
        publicada=True
    ).order_by('-data_publicacao')[:6]
    
    context = {
        'noticias_destaque': noticias_destaque,
        'noticias_recentes': noticias_recentes,
    }
    
    return render(request, 'noticias/home.html', context)

# Autenticação
def login_admin(request):
    """Página de login para o painel administrativo"""
    if request.user.is_authenticated:
        return redirect('noticias:painel_admin')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.username}!')
            return redirect('noticias:painel_admin')
        else:
            messages.error(request, 'Usuário ou senha incorretos, ou você não tem permissão de administrador.')
    
    return render(request, 'noticias/login_admin.html')

def logout_admin(request):
    """Logout do painel administrativo"""
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('noticias:home')

# Painel Administrativo Personalizado (Protegido)
@login_required(login_url='noticias:login_admin')
def painel_admin(request):
    """Painel administrativo principal"""
    if not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para acessar o painel administrativo.')
        return redirect('noticias:home')
    
    noticias = Noticia.objects.all().order_by('-data_publicacao')
    total_noticias = noticias.count()
    noticias_publicadas = noticias.filter(publicada=True).count()
    noticias_rascunho = noticias.filter(publicada=False).count()
    
    context = {
        'noticias': noticias[:10],  # Últimas 10 notícias
        'total_noticias': total_noticias,
        'noticias_publicadas': noticias_publicadas,
        'noticias_rascunho': noticias_rascunho,
    }
    return render(request, 'noticias/painel_admin.html', context)

@login_required
def criar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.data_publicacao = timezone.now()  # Define a data automaticamente
            noticia.publicada = True  # Por padrão, publica a notícia
            noticia.save()
            
            # Calcula relevância automaticamente
            noticia.calcular_relevancia()
            
            messages.success(request, f'Notícia "{noticia.titulo}" criada com sucesso! Score de relevância: {noticia.relevancia_score}/10')
            return redirect('noticias:painel_admin')
    else:
        form = NoticiaForm()
    
    return render(request, 'noticias/form_noticia.html', {'form': form, 'titulo': 'Criar Nova Notícia'})

@login_required
def editar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            noticia = form.save()  # Não altera a data de publicação
            
            # Recalcula relevância
            noticia.calcular_relevancia()
            
            messages.success(request, f'Notícia "{noticia.titulo}" atualizada com sucesso! Score de relevância: {noticia.relevancia_score}/10')
            return redirect('noticias:painel_admin')
    else:
        form = NoticiaForm(instance=noticia)
    
    return render(request, 'noticias/form_noticia.html', {
        'form': form, 
        'titulo': f'Editar: {noticia.titulo}',
        'noticia': noticia
    })

@login_required(login_url='noticias:login_admin')
def excluir_noticia(request, pk):
    """Excluir notícia"""
    if not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para excluir notícias.')
        return redirect('noticias:home')
    
    noticia = get_object_or_404(Noticia, pk=pk)
    titulo = noticia.titulo
    
    if request.method == 'POST':
        noticia.delete()
        messages.success(request, f'Notícia "{titulo}" excluída com sucesso!')
        return redirect('noticias:painel_admin')
    
    context = {
        'noticia': noticia
    }
    return render(request, 'noticias/confirmar_exclusao.html', context)

@login_required(login_url='noticias:login_admin')
def toggle_publicacao(request, pk):
    """Alternar status de publicação da notícia"""
    if not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para alterar o status das notícias.')
        return redirect('noticias:home')
    
    noticia = get_object_or_404(Noticia, pk=pk)
    noticia.publicada = not noticia.publicada
    noticia.save()
    
    status = "publicada" if noticia.publicada else "despublicada"
    messages.success(request, f'Notícia "{noticia.titulo}" {status} com sucesso!')
    
    return redirect('noticias:painel_admin')
