#!/usr/bin/env bash
# exit on error
set -o errexit

# Definir variável de ambiente para o Django
export DJANGO_SETTINGS_MODULE=portal_noticias.settings_render_simple

echo "🚀 Iniciando build do projeto..."

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Tentar aplicar migrações
echo "🗄️  Aplicando migrações..."
python manage.py migrate

# Tentar atualizar relevância
echo "🎯 Atualizando relevância das notícias..."
if python manage.py atualizar_relevancia --help > /dev/null 2>&1; then
    python manage.py atualizar_relevancia
    echo "✅ Relevância atualizada com sucesso!"
else
    echo "⚠️  Comando de relevância não disponível"
fi

echo "🎉 Build concluído com sucesso!"
