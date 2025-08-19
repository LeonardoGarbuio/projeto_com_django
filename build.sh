#!/usr/bin/env bash
# exit on error
set -o errexit

# Definir variável de ambiente para o Django
export DJANGO_SETTINGS_MODULE=portal_noticias.settings_render

# Instalar dependências
pip install -r requirements.txt

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Aplicar migrações
python manage.py migrate

# Atualizar relevância das notícias existentes
python manage.py atualizar_relevancia
