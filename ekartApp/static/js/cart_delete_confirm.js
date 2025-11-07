document.addEventListener('DOMContentLoaded', function() {
    var removeButtons = document.querySelectorAll('.cart-remove-btn');
    removeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var url = this.getAttribute('data-url');
            if (confirm('Are you sure you want to remove this item from your cart?')) {
                window.location.href = url;
            }
        });
    });
});
