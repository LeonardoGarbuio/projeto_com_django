"""
WSGI config for portal_noticias project for Render deployment.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_noticias.settings_render')

application = get_wsgi_application()
