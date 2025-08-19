// JavaScript específico para a página de detalhes da notícia

document.addEventListener('DOMContentLoaded', function() {
    
    // Função para favoritar notícia
    function toggleFavorite(noticiaId) {
        const favoriteBtn = document.querySelector(`[data-noticia-id="${noticiaId}"]`);
        if (favoriteBtn) {
            const icon = favoriteBtn.querySelector('i');
            const span = favoriteBtn.querySelector('span');
            
            if (favoriteBtn.classList.contains('favorited')) {
                // Remover dos favoritos
                favoriteBtn.classList.remove('favorited');
                icon.classList.remove('fas');
                icon.classList.add('far');
                span.textContent = 'Favoritar';
                showToast('Notícia removida dos favoritos!', 'info');
            } else {
                // Adicionar aos favoritos
                favoriteBtn.classList.add('favorited');
                icon.classList.remove('far');
                icon.classList.add('fas');
                span.textContent = 'Favoritado';
                showToast('Notícia adicionada aos favoritos!', 'success');
            }
        }
    }
    
    // Função para compartilhar notícia
    function shareArticle(url, title) {
        if (navigator.share) {
            // Web Share API (dispositivos móveis)
            navigator.share({
                title: title,
                url: url
            }).then(() => {
                showToast('Notícia compartilhada com sucesso!', 'success');
            }).catch((error) => {
                console.log('Erro ao compartilhar:', error);
                fallbackShare(url, title);
            });
        } else {
            // Fallback para navegadores desktop
            fallbackShare(url, title);
        }
    }
    
    // Fallback para compartilhamento
    function fallbackShare(url, title) {
        // Tentar copiar para clipboard
        if (navigator.clipboard) {
            navigator.clipboard.writeText(url).then(() => {
                showToast('Link copiado para a área de transferência!', 'success');
            }).catch(() => {
                // Se falhar, abrir em nova aba
                window.open(url, '_blank');
                showToast('Link aberto em nova aba!', 'info');
            });
        } else {
            // Fallback final: abrir em nova aba
            window.open(url, '_blank');
            showToast('Link aberto em nova aba!', 'info');
        }
    }
    
    // Função para mostrar toast notifications
    function showToast(message, type = 'info') {
        // Remover toasts existentes
        const existingToasts = document.querySelectorAll('.custom-toast');
        existingToasts.forEach(toast => toast.remove());
        
        // Criar novo toast
        const toast = document.createElement('div');
        toast.className = `custom-toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="toast-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // Adicionar ao body
        document.body.appendChild(toast);
        
        // Mostrar toast
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        // Remover automaticamente após 4 segundos
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.remove();
                }
            }, 300);
        }, 4000);
    }
    
    // Adicionar eventos aos botões
    const favoriteBtn = document.querySelector('.favorite-btn');
    if (favoriteBtn) {
        favoriteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const noticiaId = this.getAttribute('data-noticia-id');
            toggleFavorite(noticiaId);
        });
    }
    
    const shareBtn = document.querySelector('.share-btn');
    if (shareBtn) {
        shareBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('data-url');
            const title = this.getAttribute('data-title');
            shareArticle(url, title);
        });
    }
    
    // Inicializar tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    console.log('Funcionalidades de notícia carregadas com sucesso!');
});

// Adicionar estilos CSS para os toasts
const toastStyles = document.createElement('style');
toastStyles.textContent = `
    .custom-toast {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border-left: 4px solid #17a2b8;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 350px;
        min-width: 300px;
    }
    
    .custom-toast.show {
        transform: translateX(0);
    }
    
    .custom-toast .toast-content {
        display: flex;
        align-items: center;
        padding: 1rem 1.5rem;
        color: #333;
    }
    
    .custom-toast .toast-close {
        background: none;
        border: none;
        color: #999;
        cursor: pointer;
        margin-left: auto;
        padding: 0;
        font-size: 0.9rem;
    }
    
    .custom-toast .toast-close:hover {
        color: #666;
    }
    
    .toast-success {
        border-left-color: #28a745;
    }
    
    .toast-error {
        border-left-color: #dc3545;
    }
    
    .toast-warning {
        border-left-color: #ffc107;
    }
    
    .toast-info {
        border-left-color: #17a2b8;
    }
`;

document.head.appendChild(toastStyles);
