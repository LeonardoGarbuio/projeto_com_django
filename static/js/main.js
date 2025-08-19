// JavaScript para o Portal de Notícias

document.addEventListener('DOMContentLoaded', function() {
    
    // Adicionar animação fade-in aos cards
    const cards = document.querySelectorAll('.news-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // Smooth scroll para links internos
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Lazy loading para imagens
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Tooltip para botões
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Adicionar classe ativa ao link da navegação atual
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Função para formatar data
    function formatDate(dateString) {
        const date = new Date(dateString);
        const options = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        return date.toLocaleDateString('pt-BR', options);
    }
    
    // Aplicar formatação de data aos elementos com classe .date-format
    const dateElements = document.querySelectorAll('.date-format');
    dateElements.forEach(element => {
        const dateString = element.getAttribute('data-date');
        if (dateString) {
            element.textContent = formatDate(dateString);
        }
    });
    
    // Função para compartilhar notícia
    function shareNews(title, url) {
        if (navigator.share) {
            navigator.share({
                title: title,
                url: url
            });
        } else {
            // Fallback para navegadores que não suportam Web Share API
            const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`;
            window.open(shareUrl, '_blank');
        }
    }
    
    // Adicionar evento de clique aos botões de compartilhamento
    const shareButtons = document.querySelectorAll('.share-btn');
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const title = this.getAttribute('data-title');
            const url = this.getAttribute('data-url');
            shareNews(title, url);
        });
    });
    
    // Função para marcar notícia como favorita
    function toggleFavorite(noticiaId) {
        const favoriteBtn = document.querySelector(`[data-noticia-id="${noticiaId}"]`);
        if (favoriteBtn) {
            favoriteBtn.classList.toggle('text-danger');
            const icon = favoriteBtn.querySelector('i');
            if (favoriteBtn.classList.contains('text-danger')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                showToast('Notícia adicionada aos favoritos!', 'success');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                showToast('Notícia removida dos favoritos!', 'info');
            }
        }
    }
    
    // Adicionar evento de clique aos botões de favorito
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const noticiaId = this.getAttribute('data-noticia-id');
            toggleFavorite(noticiaId);
        });
    });
    
    // Função para mostrar toast notifications
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'position-fixed top-0 end-0 p-3';
            container.style.zIndex = '1055';
            document.body.appendChild(container);
        }
        
        const toastId = 'toast-' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast" role="alert">
                <div class="toast-header">
                    <strong class="me-auto">Portal de Notícias</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remover toast após ser fechado
        toastElement.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    }
    
    // Função para buscar notícias (se implementado)
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchInput = this.querySelector('input[name="q"]');
            const query = searchInput.value.trim();
            
            if (query.length > 0) {
                // Implementar busca aqui
                showToast(`Buscando por: ${query}`, 'info');
            }
        });
    }
    
    // Função para carregar mais notícias (infinite scroll)
    let isLoading = false;
    let page = 1;
    
    function loadMoreNews() {
        if (isLoading) return;
        
        isLoading = true;
        const loadingIndicator = document.querySelector('.loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'block';
        }
        
        // Simular carregamento (substituir por chamada AJAX real)
        setTimeout(() => {
            isLoading = false;
            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
            page++;
        }, 1000);
    }
    
    // Detectar quando o usuário chegou ao final da página
    window.addEventListener('scroll', function() {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 1000) {
            loadMoreNews();
        }
    });
    
    // Função para voltar ao topo
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-primary position-fixed bottom-0 end-0 m-3';
    backToTopBtn.style.zIndex = '1000';
    backToTopBtn.style.display = 'none';
    backToTopBtn.setAttribute('data-bs-toggle', 'tooltip');
    backToTopBtn.setAttribute('data-bs-placement', 'top');
    backToTopBtn.setAttribute('title', 'Voltar ao topo');
    
    document.body.appendChild(backToTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Inicializar tooltips
    const tooltipList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    console.log('Portal de Notícias carregado com sucesso!');
});

// Simular contador de visualizações
document.addEventListener('DOMContentLoaded', function() {
    const viewCount = document.getElementById('view-count');
    if (viewCount) {
        let currentViews = Math.floor(Math.random() * 100) + 50;
        viewCount.textContent = currentViews;

        // Incrementar visualizações
        setInterval(() => {
            currentViews += Math.floor(Math.random() * 3) + 1;
            viewCount.textContent = currentViews;
        }, 5000);
    }

    // Funcionalidade de favoritar
    const favoriteBtn = document.querySelector('.favorite-btn');
    if (favoriteBtn) {
        favoriteBtn.addEventListener('click', function() {
            const icon = this.querySelector('i');
            const span = this.querySelector('span');

            if (icon.classList.contains('far')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                span.textContent = 'Favoritado';
                this.classList.add('favorited');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                span.textContent = 'Favoritar';
                this.classList.remove('favorited');
            }
        });
    }

    // Funcionalidade de compartilhar
    const shareBtn = document.querySelector('.share-btn');
    if (shareBtn) {
        shareBtn.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            const title = this.getAttribute('data-title');

            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                });
            } else {
                // Fallback para copiar URL
                navigator.clipboard.writeText(url).then(() => {
                    // Criar toast de notificação
                    showToast('Link copiado para a área de transferência!', 'success');
                });
            }
        });
    }
});

// Função para mostrar toast de notificação
function showToast(message, type = 'info') {
    // Criar elemento toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type} show`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
        padding: 1rem 1.5rem;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
        font-family: 'Georgia', 'Times New Roman', serif;
        color: var(--text-color);
        max-width: 300px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    toast.textContent = message;
    
    // Adicionar ao body
    document.body.appendChild(toast);
    
    // Remover após 3 segundos
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Adicionar estilos de animação
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
