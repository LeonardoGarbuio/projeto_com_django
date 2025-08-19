from django.contrib import admin
from .models import Noticia

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data_publicacao', 'publicada']
    list_filter = ['publicada', 'data_publicacao']
    search_fields = ['titulo', 'resumo', 'conteudo']
    list_editable = ['publicada']
    date_hierarchy = 'data_publicacao'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'resumo', 'conteudo', 'imagem')
        }),
        ('Publicação', {
            'fields': ('data_publicacao', 'publicada')
        }),
    )
    
    readonly_fields = ['data_criacao']
