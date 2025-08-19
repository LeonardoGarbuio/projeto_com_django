# Portal de Notícias - Django

Um portal de notícias moderno e responsivo desenvolvido com Django, com área administrativa completa e layout moderno.

## 🚀 Funcionalidades

- **Área Administrativa**: Interface completa para gerenciar notícias
- **Layout Moderno**: Design responsivo com Bootstrap 5 e CSS personalizado
- **Sistema de Notícias**: CRUD completo com imagens, resumos e conteúdo
- **Páginas Dinâmicas**: Página inicial, lista de notícias e detalhes
- **Funcionalidades Interativas**: Compartilhamento, favoritos, paginação
- **Responsivo**: Funciona perfeitamente em dispositivos móveis

## 📋 Pré-requisitos

- Python 3.8+
- Django 5.1+
- Pillow (para manipulação de imagens)

## 🛠️ Instalação

1. **Clone o repositório ou navegue até o diretório do projeto**
   ```bash
   cd Trabalho_Ven
   ```

2. **Instale as dependências**
   ```bash
   pip install django pillow
   ```

3. **Execute as migrações**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Crie um superusuário (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Execute o servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```

## 🎯 Como Usar

### Acessando o Portal

- **Página Inicial**: http://127.0.0.1:8000/
- **Lista de Notícias**: http://127.0.0.1:8000/noticias/
- **Área Administrativa**: http://127.0.0.1:8000/admin/

### Credenciais do Admin (se criado automaticamente)
- **Usuário**: admin
- **Email**: admin@example.com
- **Senha**: (será solicitada na primeira execução)

### Gerenciando Notícias

1. Acesse a área administrativa em `/admin/`
2. Faça login com suas credenciais
3. Clique em "Notícias" para gerenciar
4. Use "Adicionar Notícia" para criar novas notícias
5. Preencha:
   - **Título**: Título da notícia
   - **Resumo**: Breve descrição (máximo 300 caracteres)
   - **Conteúdo**: Texto completo da notícia
   - **Imagem**: Foto relacionada à notícia
   - **Data de Publicação**: Quando a notícia deve aparecer
   - **Publicada**: Marque para tornar visível no site

## 📁 Estrutura do Projeto

```
Trabalho_Ven/
├── portal_noticias/          # Configurações do projeto
├── noticias/                 # App principal
│   ├── models.py            # Modelo de dados
│   ├── views.py             # Lógicas de negócio
│   ├── admin.py             # Configuração do admin
│   └── urls.py              # URLs do app
├── templates/               # Templates HTML
│   ├── base.html           # Template base
│   └── noticias/           # Templates específicos
├── static/                 # Arquivos estáticos
│   ├── css/               # Estilos CSS
│   └── js/                # JavaScript
├── media/                  # Upload de imagens
└── manage.py              # Script de gerenciamento
```

## 🎨 Características do Design

- **Bootstrap 5**: Framework CSS moderno
- **Font Awesome**: Ícones profissionais
- **Google Fonts**: Tipografia Inter
- **CSS Personalizado**: Estilos únicos
- **Animações**: Transições suaves
- **Responsivo**: Mobile-first design

## 🔧 Funcionalidades Técnicas

### Modelo de Dados
- **Noticia**: Título, resumo, conteúdo, imagem, datas, status

### Views
- **Home**: Página inicial com destaques
- **NoticiaListView**: Lista paginada de notícias
- **NoticiaDetailView**: Detalhes completos da notícia

### Templates
- **Base**: Layout principal com navegação
- **Home**: Página inicial com seções
- **Lista**: Grid de notícias com paginação
- **Detalhe**: Página completa da notícia

### JavaScript
- Animações de entrada
- Compartilhamento social
- Sistema de favoritos
- Navegação suave
- Tooltips interativos

## 📱 Páginas Disponíveis

### 1. Página Inicial (`/`)
- Hero section com título
- Destaques principais
- Notícias recentes
- Estatísticas
- Newsletter

### 2. Lista de Notícias (`/noticias/`)
- Grid responsivo de notícias
- Paginação
- Filtros (futuro)
- Busca (futuro)

### 3. Detalhes da Notícia (`/noticia/<id>/`)
- Conteúdo completo
- Imagem em destaque
- Meta informações
- Botões de compartilhamento
- Sidebar com informações extras
- Navegação entre notícias

### 4. Área Administrativa (`/admin/`)
- CRUD completo de notícias
- Interface intuitiva
- Filtros e busca
- Upload de imagens
- Controle de publicação

## 🚀 Deploy

Para fazer deploy em produção:

1. **Configurar variáveis de ambiente**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['seu-dominio.com']
   SECRET_KEY = 'sua-chave-secreta'
   ```

2. **Configurar banco de dados**
   - PostgreSQL (recomendado)
   - MySQL
   - SQLite (desenvolvimento)

3. **Configurar arquivos estáticos**
   ```bash
   python manage.py collectstatic
   ```

4. **Configurar servidor web**
   - Nginx + Gunicorn
   - Apache + mod_wsgi

## 🔮 Próximas Funcionalidades

- [ ] Sistema de categorias
- [ ] Comentários
- [ ] Sistema de busca
- [ ] API REST
- [ ] Sistema de usuários
- [ ] Notificações push
- [ ] SEO otimizado
- [ ] Cache Redis
- [ ] Testes automatizados

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências estão instaladas
2. Confirme se as migrações foram executadas
3. Verifique os logs do servidor
4. Consulte a documentação do Django

## 📄 Licença

Este projeto é de uso livre para fins educacionais e comerciais.

---

**Desenvolvido com ❤️ usando Django**
