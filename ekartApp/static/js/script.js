// Custom JS for interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll to products section
    const shopNowBtn = document.querySelector('.hero-banner .btn');
    if (shopNowBtn) {
        shopNowBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const productsSection = document.querySelector('#products');
            if (productsSection) {
                productsSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // Search bar animation
    const searchInput = document.querySelector('.search-bar .form-control');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.style.boxShadow = '0 0 0 2px #febd69';
        });
        searchInput.addEventListener('blur', function() {
            this.style.boxShadow = '';
        });
    }

    // Dropdown toggle for account menu
    const dropdownToggle = document.getElementById('dropdownMenuButton');
    const dropdownMenu = document.getElementById('dropdownMenu');
    if (dropdownToggle && dropdownMenu) {
        dropdownToggle.addEventListener('click', function(e) {
            e.preventDefault();
            dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!dropdownToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
                dropdownMenu.style.display = 'none';
            }
        });
    }

    // Add to cart alert (placeholder)
    // document.querySelectorAll('.btn-warning').forEach(btn => {
    //     btn.addEventListener('click', function() {
    //         alert('Added to cart!');
    //     });
    // });
});
