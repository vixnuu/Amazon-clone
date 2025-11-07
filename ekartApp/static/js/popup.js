function closePopup() {
    document.getElementById('message-popup').classList.remove('show');
}
function showPopup() {
    document.getElementById('message-popup').classList.add('show');
    setTimeout(closePopup, 5000); // Auto close after 5 seconds
}

// Check if there are messages and show popup on page load
document.addEventListener('DOMContentLoaded', function() {
    const popup = document.getElementById('message-popup');
    if (popup && popup.dataset.hasMessages === 'true') {
        showPopup();
    }
});
