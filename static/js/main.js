// Main JavaScript for STAY UP Furniture

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Product image gallery
    initializeProductGallery();
    
    // Quantity controls
    initializeQuantityControls();
    
    // Cart functionality
    initializeCart();
    
    // Search functionality
    initializeSearch();
    
    // Newsletter form
    initializeNewsletter();

    // Theme toggle
    initializeThemeToggle();
});

// Product Gallery Functions
function initializeProductGallery() {
    const mainImage = document.querySelector('.main-image img');
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    if (thumbnails.length > 0 && mainImage) {
        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                const newImageSrc = this.querySelector('img').src;
                mainImage.src = newImageSrc;
            });
        });
    }
    
    // Update thumbnail active state on carousel slide
    const carousel = document.getElementById('productCarousel');
    if (carousel) {
        carousel.addEventListener('slide.bs.carousel', function(event) {
            const thumbnails = document.querySelectorAll('.thumbnail');
            thumbnails.forEach((thumb, index) => {
                if (index === event.to) {
                    thumb.classList.add('active');
                    thumb.style.borderColor = 'var(--primary-color)';
                } else {
                    thumb.classList.remove('active');
                    thumb.style.borderColor = 'transparent';
                }
            });
        });
    }
}

// Function to go to specific slide (called from thumbnail click)
function goToSlide(index) {
    const carousel = document.getElementById('productCarousel');
    if (carousel) {
        const bsCarousel = new bootstrap.Carousel(carousel);
        bsCarousel.to(index);
    }
}

// Quantity Controls
function initializeQuantityControls() {
    // Handle +/- buttons with data-action attribute
    document.querySelectorAll('[data-action="decrease"], [data-action="increase"]').forEach(btn => {
        btn.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            const input = document.querySelector(`input[data-cart-item-id="${itemId}"]`);
            if (input) {
                let currentValue = parseInt(input.value) || 1;
                if (this.dataset.action === 'decrease' && currentValue > 1) {
                    input.value = currentValue - 1;
                } else if (this.dataset.action === 'increase') {
                    input.value = currentValue + 1;
                }
                updateQuantity(input);
            }
        });
    });
    
    // Handle input changes
    document.querySelectorAll('input[data-cart-item-id]').forEach(input => {
        input.addEventListener('change', function() {
            let value = parseInt(this.value) || 1;
            if (value < 1) value = 1;
            this.value = value;
            updateQuantity(this);
        });
    });
}

function updateQuantity(input) {
    const cartItemId = input.dataset.cartItemId;
    const newQuantity = parseInt(input.value);
    
    if (cartItemId) {
        // Make AJAX call to update cart
        fetch(`/cart/update/${cartItemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                'quantity': newQuantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateCartSummary(data.cart_total, data.cart_items);
                showMessage('Cart updated successfully', 'success');
            } else {
                showMessage('Error updating cart', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Error updating cart', 'danger');
        });
    }
}

// Cart Functions
function initializeCart() {
    // Add to cart buttons
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
    
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const quantity = 1;
            
            addToCart(productId, quantity);
        });
    });
    
    // Remove from cart buttons
    const removeFromCartBtns = document.querySelectorAll('.remove-from-cart-btn');
    
    removeFromCartBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const cartItemId = this.dataset.cartItemId;
            
            if (confirm('Are you sure you want to remove this item from your cart?')) {
                removeFromCart(cartItemId);
            }
        });
    });
}

function addToCart(productId, quantity) {
    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            'product_id': productId,
            'quantity': quantity
        })
    })
    .then(response => {
        if (response.status === 302 || response.redirected) {
            window.location.href = '/accounts/login/';
            return null;
        }
        return response.json();
    })
    .then(data => {
        if (!data) return;
        
        if (data.success) {
            updateCartBadge(data.cart_items);
            showMessage('Product added to cart!', 'success');
            
            // Update button state
            const btn = document.querySelector(`[data-product-id="${productId}"]`);
            if (btn) {
                btn.innerHTML = '<i class="fas fa-check"></i> Added to Cart';
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-success');
                
                setTimeout(() => {
                    btn.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
                    btn.classList.remove('btn-success');
                    btn.classList.add('btn-primary');
                }, 2000);
            }
        } else {
            showMessage(data.message || 'Error adding to cart', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Error adding to cart', 'danger');
    });
}

function removeFromCart(cartItemId) {
    fetch(`/cart/remove/${cartItemId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove cart item row
            const cartItem = document.querySelector(`[data-cart-item-id="${cartItemId}"]`).closest('.cart-item');
            cartItem.remove();
            
            updateCartSummary(data.cart_total, data.cart_items);
            updateCartBadge(data.cart_items);
            showMessage('Item removed from cart', 'success');
        } else {
            showMessage('Error removing item', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Error removing item', 'danger');
    });
}

function updateCartSummary(totalPrice, totalItems) {
    const totalElement = document.querySelector('.cart-total');
    const itemsElement = document.querySelector('.cart-items-count');
    
    if (totalElement) {
        totalElement.textContent = `$${totalPrice.toFixed(2)}`;
    }
    
    if (itemsElement) {
        itemsElement.textContent = totalItems;
    }
}

function updateCartBadge(totalItems) {
    const badge = document.querySelector('.cart-badge');
    if (badge) {
        badge.textContent = totalItems;
    }
}

// Wishlist Function
function addToWishlist(productId) {
    fetch('/wishlist/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            'product_id': productId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('Added to wishlist!', 'success');
            // Toggle heart icon
            const btn = document.querySelector(`[onclick="addToWishlist(${productId})"]`);
            if (btn) {
                const icon = btn.querySelector('i');
                icon.classList.remove('far');
                icon.classList.add('fas', 'text-danger');
            }
        } else {
            showMessage(data.message || 'Error adding to wishlist', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Please login to add to wishlist', 'warning');
    });
}

// Search Functions
function initializeSearch() {
    const searchInput = document.querySelector('input[name="q"]');
    const searchForm = document.querySelector('form[action*="search"]');
    
    if (searchInput && searchForm) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    performLiveSearch(query);
                }, 300);
            }
        });
    }
}

function performLiveSearch(query) {
    fetch(`/api/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data.results);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function displaySearchResults(results) {
    // Implementation for displaying live search results
    // This would show a dropdown with search suggestions
}

// Newsletter Form
function initializeNewsletter() {
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = this.querySelector('input[type="email"]').value;
            
            fetch('/newsletter/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({
                    'email': email
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessage('Successfully subscribed to newsletter!', 'success');
                    this.reset();
                } else {
                    showMessage(data.message || 'Error subscribing', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Error subscribing', 'danger');
            });
        });
    }
}

// Utility Functions
function getCSRFToken() {
    const cookie = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    return cookie ? cookie.pop() : '';
}

function showMessage(message, type) {
    // Remove existing messages
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the main content area
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(alertDiv, main.firstChild);
    }
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// Lazy loading for images
if ('IntersectionObserver' in window) {
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

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Form validation
const forms = document.querySelectorAll('.needs-validation');
forms.forEach(form => {
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });
});

// Image zoom functionality
function initializeImageZoom() {
    const productImages = document.querySelectorAll('.product-image img, .main-image img');
    
    productImages.forEach(img => {
        img.addEventListener('click', function() {
            const modal = document.createElement('div');
            modal.className = 'image-zoom-modal';
            modal.innerHTML = `
                <div class="image-zoom-overlay" onclick="closeImageZoom()">
                    <div class="image-zoom-content">
                        <img src="${this.src}" alt="${this.alt}">
                        <button class="close-btn" onclick="closeImageZoom()">&times;</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        });
    });
}

function closeImageZoom() {
    const modal = document.querySelector('.image-zoom-modal');
    if (modal) {
        modal.remove();
    }
}

// Add CSS for image zoom
const zoomCSS = `
.image-zoom-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.9);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    cursor: pointer;
}

.image-zoom-content {
    position: relative;
    max-width: 90%;
    max-height: 90%;
}

.image-zoom-content img {
    max-width: 100%;
    max-height: 90vh;
    object-fit: contain;
    border-radius: 8px;
}

.close-btn {
    position: absolute;
    top: -40px;
    right: 0;
    background: none;
    border: none;
    color: white;
    font-size: 2rem;
    cursor: pointer;
    padding: 0;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
}
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = zoomCSS;
document.head.appendChild(styleSheet);

// Initialize image zoom
initializeImageZoom();

// Theme toggle
function initializeThemeToggle() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;

    const body = document.body;
    const storedTheme = localStorage.getItem('stayup-theme');
    if (storedTheme === 'dark') {
        body.classList.add('dark-mode');
        toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
    }

    toggleBtn.addEventListener('click', function() {
        body.classList.toggle('dark-mode');
        const isDark = body.classList.contains('dark-mode');
        localStorage.setItem('stayup-theme', isDark ? 'dark' : 'light');
        toggleBtn.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    });
}