from django.urls import path
from . import views

app_name = 'noticias'

urlpatterns = [
    # URLs públicas
    path('', views.home, name='home'),
    path('noticias/', views.NoticiaListView.as_view(), name='lista_noticias'),
    path('noticia/<int:pk>/', views.NoticiaDetailView.as_view(), name='noticia_detalhe'),
    
    # URLs do painel administrativo personalizado
    path('painel/login/', views.login_admin, name='login_admin'),
    path('painel/logout/', views.logout_admin, name='logout_admin'),
    path('painel/', views.painel_admin, name='painel_admin'),
    path('painel/criar/', views.criar_noticia, name='criar_noticia'),
    path('painel/editar/<int:pk>/', views.editar_noticia, name='editar_noticia'),
    path('painel/excluir/<int:pk>/', views.excluir_noticia, name='excluir_noticia'),
    path('painel/toggle/<int:pk>/', views.toggle_publicacao, name='toggle_publicacao'),
]
