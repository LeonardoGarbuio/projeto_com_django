"""
URLs específicas para o Render
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('noticias.urls')),
]

# Configuração para servir arquivos de mídia no Render
if not settings.DEBUG:
    # Em produção, usar whitenoise para servir mídia
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
else:
    # Em desenvolvimento, usar configuração padrão
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
