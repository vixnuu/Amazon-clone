document.addEventListener('DOMContentLoaded', function() {
    var cancelButtons = document.querySelectorAll('.cart-remove-btn');
    cancelButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var url = this.getAttribute('data-url');
            if (confirm('Are you sure you want to cancel this order?')) {
                window.location.href = url;
            }
        });
    });
});
