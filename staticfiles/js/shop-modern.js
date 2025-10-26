/**
 * Modern Shop Page - JavaScript
 * Horizontal Filter Bar Interactions
 */

(function() {
    'use strict';
    
    // ===== FILTER TOGGLE =====
    const filterToggle = document.getElementById('filterToggle');
    const filterContent = document.getElementById('filterContent');
    
    if (filterToggle && filterContent) {
        // Load saved state
        const isFilterOpen = localStorage.getItem('filterOpen') === 'true';
        if (isFilterOpen) {
            filterContent.classList.add('show');
            filterToggle.classList.add('active');
        }
        
        // Toggle filter on click
        filterToggle.addEventListener('click', function() {
            filterContent.classList.toggle('show');
            filterToggle.classList.toggle('active');
            
            // Save state
            const isOpen = filterContent.classList.contains('show');
            localStorage.setItem('filterOpen', isOpen);
        });
    }
    
    // ===== STOCK TOGGLE =====
    const inStockToggle = document.getElementById('inStockToggle');
    if (inStockToggle) {
        inStockToggle.addEventListener('change', function() {
            const url = new URL(window.location.href);
            if (this.checked) {
                url.searchParams.set('in_stock', 'on');
            } else {
                url.searchParams.delete('in_stock');
            }
            window.location.href = url.toString();
        });
    }
    
    // ===== VIEW MODE TOGGLE =====
    const viewButtons = document.querySelectorAll('.view-btn');
    const productsGrid = document.querySelector('.products-grid');
    
    if (viewButtons.length > 0 && productsGrid) {
        // Load saved view mode
        const savedView = localStorage.getItem('viewMode') || 'grid';
        productsGrid.classList.add(savedView + '-view');
        
        viewButtons.forEach(btn => {
            if (btn.dataset.view === savedView) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
            
            btn.addEventListener('click', function() {
                const view = this.dataset.view;
                
                // Update active state
                viewButtons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                // Update grid class
                productsGrid.classList.remove('grid-view', 'list-view');
                productsGrid.classList.add(view + '-view');
                
                // Save preference
                localStorage.setItem('viewMode', view);
                
                // Show toast
                showToast(`Switched to ${view} view`, 'success');
            });
        });
    }
    
    // ===== ADD TO CART ANIMATION =====
    const addCartForms = document.querySelectorAll('.add-cart-form');
    addCartForms.forEach(form => {
        form.addEventListener('submit', function() {
            const btn = this.querySelector('.btn-add-cart');
            if (btn && !btn.disabled) {
                btn.classList.add('loading');
                btn.disabled = true;
                
                // Show loading text
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="bi bi-arrow-repeat"></i> Adding...';
                
                // Note: Form will submit normally, this is just visual feedback
            }
        });
    });
    
    // ===== WISHLIST TOGGLE =====
    const wishlistButtons = document.querySelectorAll('.wishlist-toggle');
    wishlistButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const url = this.getAttribute('data-wishlist-url');
            const icon = this.querySelector('i');
            const isActive = this.classList.contains('active');
            
            // Get CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Disable button during request
            this.disabled = true;
            
            // Send AJAX request
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Toggle active state
                    this.classList.toggle('active');
                    
                    // Update icon
                    if (data.in_wishlist) {
                        icon.classList.remove('bi-heart');
                        icon.classList.add('bi-heart-fill');
                        showToast('Đã thêm vào yêu thích!', 'success');
                    } else {
                        icon.classList.remove('bi-heart-fill');
                        icon.classList.add('bi-heart');
                        showToast('Đã xóa khỏi yêu thích', 'info');
                    }
                } else {
                    showToast('Có lỗi xảy ra', 'error');
                }
                
                // Re-enable button
                this.disabled = false;
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Không thể kết nối với server', 'error');
                this.disabled = false;
            });
        });
    });
    
    // ===== LAZY LOADING IMAGES =====
    if ('IntersectionObserver' in window) {
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
        
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
    }
    
    // ===== SMOOTH SCROLL FOR PAGINATION =====
    const paginationLinks = document.querySelectorAll('.pagination .page-link');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Let the link work normally, but scroll to top smoothly
            setTimeout(() => {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }, 100);
        });
    });
    
    // ===== SCROLL ANIMATIONS =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe product cards (but only add animation if not already animated)
    setTimeout(() => {
        const productCards = document.querySelectorAll('.product-card');
        productCards.forEach((card, index) => {
            // Only observe cards that haven't been animated yet
            if (index > 8) {
                card.style.opacity = '0';
                card.style.transform = 'translateY(30px)';
                card.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
                scrollObserver.observe(card);
            }
        });
    }, 500);
    
    // ===== TOAST NOTIFICATION =====
    function showToast(message, type = 'info') {
        // Remove existing toast
        const existingToast = document.querySelector('.custom-toast');
        if (existingToast) {
            existingToast.remove();
        }
        
        // Create toast
        const toast = document.createElement('div');
        toast.className = `custom-toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-icon">
                ${getToastIcon(type)}
            </div>
            <div class="toast-message">${message}</div>
        `;
        
        // Add styles
        Object.assign(toast.style, {
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            background: 'white',
            padding: '1rem 1.5rem',
            borderRadius: '12px',
            boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            zIndex: '9999',
            animation: 'slideInRight 0.3s ease-out',
            minWidth: '250px',
            maxWidth: '400px',
            borderLeft: `4px solid ${getToastColor(type)}`
        });
        
        document.body.appendChild(toast);
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    function getToastIcon(type) {
        const icons = {
            success: '<i class="bi bi-check-circle-fill" style="color: #28a745; font-size: 1.5rem;"></i>',
            error: '<i class="bi bi-x-circle-fill" style="color: #dc3545; font-size: 1.5rem;"></i>',
            info: '<i class="bi bi-info-circle-fill" style="color: #17a2b8; font-size: 1.5rem;"></i>',
            warning: '<i class="bi bi-exclamation-triangle-fill" style="color: #ffc107; font-size: 1.5rem;"></i>'
        };
        return icons[type] || icons.info;
    }
    
    function getToastColor(type) {
        const colors = {
            success: '#28a745',
            error: '#dc3545',
            info: '#17a2b8',
            warning: '#ffc107'
        };
        return colors[type] || colors.info;
    }
    
    // Add toast animations to document
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
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
                transform: translateX(400px);
                opacity: 0;
            }
        }
        
        .custom-toast {
            font-family: 'Poppins', sans-serif;
        }
        
        .toast-message {
            font-weight: 500;
            color: #2c3e50;
        }
        
        /* Mobile responsive toast */
        @media (max-width: 576px) {
            .custom-toast {
                right: 10px !important;
                left: 10px !important;
                min-width: auto !important;
                max-width: none !important;
            }
        }
    `;
    document.head.appendChild(style);
    
    // ===== PRICE FILTER FORM ENHANCEMENT =====
    const priceFilterForm = document.getElementById('priceFilterForm');
    if (priceFilterForm) {
        // Preserve other query parameters
        priceFilterForm.addEventListener('submit', function(e) {
            const minPrice = this.querySelector('[name="min_price"]').value;
            const maxPrice = this.querySelector('[name="max_price"]').value;
            
            if (!minPrice && !maxPrice) {
                e.preventDefault();
                showToast('Please enter a price range', 'warning');
            }
        });
    }
    
    // ===== ACTIVE FILTERS DISPLAY =====
    function updateActiveFilters() {
        const activeFiltersContainer = document.getElementById('activeFilters');
        if (!activeFiltersContainer) return;
        
        const urlParams = new URLSearchParams(window.location.search);
        const filters = [];
        
        // Check for active filters
        if (urlParams.has('min_price') || urlParams.has('max_price')) {
            const min = urlParams.get('min_price') || '0';
            const max = urlParams.get('max_price') || '∞';
            filters.push({
                label: `Price: $${min} - $${max}`,
                param: 'price'
            });
        }
        
        if (urlParams.has('in_stock')) {
            filters.push({
                label: 'In Stock Only',
                param: 'in_stock'
            });
        }
        
        // Render active filters
        if (filters.length > 0) {
            activeFiltersContainer.innerHTML = filters.map(filter => `
                <span class="filter-tag">
                    ${filter.label}
                    <span class="remove" data-param="${filter.param}">
                        <i class="bi bi-x-lg"></i>
                    </span>
                </span>
            `).join('');
            
            // Add remove handlers
            activeFiltersContainer.querySelectorAll('.remove').forEach(btn => {
                btn.addEventListener('click', function() {
                    const param = this.dataset.param;
                    const url = new URL(window.location.href);
                    
                    if (param === 'price') {
                        url.searchParams.delete('min_price');
                        url.searchParams.delete('max_price');
                    } else {
                        url.searchParams.delete(param);
                    }
                    
                    window.location.href = url.toString();
                });
            });
        } else {
            activeFiltersContainer.innerHTML = '';
        }
    }
    
    // Initialize active filters
    updateActiveFilters();
    
    // ===== KEYBOARD SHORTCUTS =====
    document.addEventListener('keydown', function(e) {
        // Press 'F' to toggle filters
        if (e.key === 'f' || e.key === 'F') {
            if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
                if (filterToggle) filterToggle.click();
            }
        }
    });
    
    // ===== PERFORMANCE OPTIMIZATION =====
    // Debounce function for search/filter inputs
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
    
    // ===== MOBILE OPTIMIZATIONS =====
    if (window.innerWidth <= 768) {
        // Disable hover effects on touch devices
        const style = document.createElement('style');
        style.textContent = `
            @media (hover: none) {
                .product-card:hover {
                    transform: none !important;
                }
                .product-card:hover .product-image {
                    transform: none !important;
                }
            }
        `;
        document.head.appendChild(style);
        
        // Auto-show quick actions on mobile
        document.querySelectorAll('.product-quick-actions').forEach(actions => {
            actions.style.right = '1rem';
        });
    }
    
    // ===== PAGE LOAD COMPLETE =====
    console.log('✅ Modern Shop Page: JavaScript loaded successfully');
    
})();

