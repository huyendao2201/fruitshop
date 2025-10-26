// ===== SHOP PAGE ENHANCEMENTS =====
// Enhanced JavaScript for Product List Page

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== VIEW MODE TOGGLE =====
    const viewBtns = document.querySelectorAll('.view-btn');
    const productsGrid = document.querySelector('.products-grid');
    
    if (viewBtns.length && productsGrid) {
        viewBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const view = this.getAttribute('data-view');
                
                // Update active button
                viewBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                // Toggle grid view
                if (view === 'list') {
                    productsGrid.style.gridTemplateColumns = '1fr';
                } else {
                    productsGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(280px, 1fr))';
                }
                
                // Store preference
                localStorage.setItem('shopViewMode', view);
            });
        });
        
        // Load saved preference
        const savedView = localStorage.getItem('shopViewMode');
        if (savedView === 'list') {
            document.querySelector('[data-view="list"]')?.click();
        }
    }
    
    // ===== SORT PRESERVE CATEGORY =====
    const sortSelect = document.querySelector('.sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const url = new URL(this.value, window.location.origin);
            const currentParams = new URLSearchParams(window.location.search);
            
            // Preserve category parameter
            if (currentParams.has('category')) {
                url.searchParams.set('category', currentParams.get('category'));
            }
            
            window.location.href = url.toString();
        });
        
        // Set current sort option as selected
        const currentSort = new URLSearchParams(window.location.search).get('sort_by');
        if (currentSort) {
            sortSelect.value = `?sort_by=${currentSort}`;
        }
    }
    
    // ===== PRICE FILTER =====
    const priceFilterForm = document.getElementById('priceFilterForm');
    if (priceFilterForm) {
        priceFilterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const minPrice = this.querySelector('[name="min_price"]').value;
            const maxPrice = this.querySelector('[name="max_price"]').value;
            const currentParams = new URLSearchParams(window.location.search);
            
            if (minPrice) currentParams.set('min_price', minPrice);
            if (maxPrice) currentParams.set('max_price', maxPrice);
            
            window.location.href = `${window.location.pathname}?${currentParams.toString()}`;
        });
    }
    
    // ===== STOCK FILTER =====
    const stockCheckbox = document.querySelector('[name="in_stock"]');
    if (stockCheckbox) {
        stockCheckbox.addEventListener('change', function() {
            const currentParams = new URLSearchParams(window.location.search);
            
            if (this.checked) {
                currentParams.set('in_stock', 'true');
            } else {
                currentParams.delete('in_stock');
            }
            
            window.location.href = `${window.location.pathname}?${currentParams.toString()}`;
        });
    }
    
    // ===== ADD TO CART ANIMATION =====
    const addToCartForms = document.querySelectorAll('.add-cart-form');
    
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const btn = this.querySelector('.btn-add-cart');
            const originalContent = btn.innerHTML;
            
            // Disable button and show loading
            btn.disabled = true;
            btn.innerHTML = '<i class="bi bi-arrow-repeat spin"></i> Adding...';
            
            // Add spinning animation
            const style = document.createElement('style');
            style.textContent = `
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
                .spin {
                    animation: spin 1s linear infinite;
                }
            `;
            document.head.appendChild(style);
            
            // Note: Form will submit normally
            // This animation gives user feedback before page refresh
        });
    });
    
    // ===== WISHLIST TOGGLE =====
    const wishlistBtns = document.querySelectorAll('.quick-action-btn[title="Add to Wishlist"]');
    
    wishlistBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const icon = this.querySelector('i');
            
            if (icon.classList.contains('bi-heart')) {
                icon.classList.remove('bi-heart');
                icon.classList.add('bi-heart-fill');
                this.style.color = '#dc3545';
                
                // Show success message
                showToast('Added to wishlist!', 'success');
            } else {
                icon.classList.remove('bi-heart-fill');
                icon.classList.add('bi-heart');
                this.style.color = '';
                
                showToast('Removed from wishlist', 'info');
            }
        });
    });
    
    // ===== SMOOTH SCROLL FOR PAGINATION =====
    const paginationLinks = document.querySelectorAll('.pagination .page-link');
    
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Scroll to top of products smoothly
            const shopPage = document.querySelector('.shop-page');
            if (shopPage) {
                setTimeout(() => {
                    shopPage.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            }
        });
    });
    
    // ===== LAZY LOADING IMAGES =====
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
    
    // ===== TOOLTIP INIT (for stock badges) =====
    const tooltips = document.querySelectorAll('[title]');
    tooltips.forEach(el => {
        el.setAttribute('data-bs-toggle', 'tooltip');
    });
    
    // ===== TOAST NOTIFICATION HELPER =====
    function showToast(message, type = 'success') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 250px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    // ===== PRODUCT CARD ANIMATIONS ON SCROLL =====
    const productCards = document.querySelectorAll('.product-card');
    
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 50);
                cardObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    productCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        cardObserver.observe(card);
    });
    
    // ===== SEARCH IN SIDEBAR =====
    const searchInput = document.querySelector('.search-form input');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            searchTimeout = setTimeout(() => {
                const searchTerm = this.value.toLowerCase();
                
                if (searchTerm.length > 2) {
                    // Here you could implement AJAX search
                    console.log('Searching for:', searchTerm);
                }
            }, 500);
        });
    }
    
    // ===== CATEGORY ACTIVE STATE =====
    const categoryItems = document.querySelectorAll('.category-item');
    const currentUrl = window.location.href;
    
    categoryItems.forEach(item => {
        if (item.href === currentUrl) {
            item.classList.add('active');
        }
    });
    
    // ===== PRODUCT QUICK VIEW (placeholder) =====
    const quickViewBtns = document.querySelectorAll('.quick-action-btn[title="Quick View"]');
    
    quickViewBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // This would typically open a modal with product details
            // For now, it just navigates to the product page
            console.log('Quick view clicked');
        });
    });
    
    // ===== RESPONSIVE SIDEBAR TOGGLE (Mobile) =====
    if (window.innerWidth <= 992) {
        const sidebar = document.querySelector('.shop-sidebar');
        
        if (sidebar) {
            // Create toggle button
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'btn btn-outline-success mb-3 w-100';
            toggleBtn.innerHTML = '<i class="bi bi-funnel"></i> Filters';
            
            const sidebarContainer = sidebar.parentElement;
            sidebarContainer.insertBefore(toggleBtn, sidebar);
            
            // Initially hide sidebar on mobile
            sidebar.style.display = 'none';
            
            toggleBtn.addEventListener('click', function() {
                if (sidebar.style.display === 'none') {
                    sidebar.style.display = 'block';
                    this.innerHTML = '<i class="bi bi-x"></i> Close Filters';
                } else {
                    sidebar.style.display = 'none';
                    this.innerHTML = '<i class="bi bi-funnel"></i> Filters';
                }
            });
        }
    }
    
    // ===== LOADING STATE FOR PAGE TRANSITIONS =====
    window.addEventListener('beforeunload', function() {
        document.body.style.opacity = '0.6';
        document.body.style.pointerEvents = 'none';
    });
    
    // ===== PRINT STYLES =====
    window.addEventListener('beforeprint', function() {
        document.querySelector('.shop-sidebar')?.style.setProperty('display', 'none', 'important');
        document.querySelector('.shop-toolbar')?.style.setProperty('display', 'none', 'important');
        document.querySelector('.pagination-wrapper')?.style.setProperty('display', 'none', 'important');
    });
    
    window.addEventListener('afterprint', function() {
        document.querySelector('.shop-sidebar')?.style.removeProperty('display');
        document.querySelector('.shop-toolbar')?.style.removeProperty('display');
        document.querySelector('.pagination-wrapper')?.style.removeProperty('display');
    });
    
    console.log('🛍️ Shop page enhancements loaded!');
});

// ===== UTILITY FUNCTIONS =====

// Format price
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}
