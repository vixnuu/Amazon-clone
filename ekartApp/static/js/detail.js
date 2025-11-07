function changeImage(thumbnail) {
    const mainImage = document.getElementById('main-product-image');
    mainImage.src = thumbnail.src;
    // Remove active class from all thumbnails
    var thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(function(thumb) {
        thumb.classList.remove('active');
    });
    // Add active class to clicked thumbnail
    thumbnail.classList.add('active');
}

function openTab(evt, tabName) {
    var tabContents = document.querySelectorAll('.tab-content');
    var tabButtons = document.querySelectorAll('.tab-button');
    tabContents.forEach(function(content) {
        content.classList.remove('active');
    });
    tabButtons.forEach(function(button) {
        button.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
    evt.currentTarget.classList.add('active');
}

function addToCart(productId) {
    var quantity = document.getElementById('quantity').value;

    // Redirect to add to cart URL
    if (!quantity || quantity <= 0) {
        alert('Please enter a valid quantity.');
        return;
    }
    else {
        window.location.href = '/add-to-cart/' + productId + '?quantity=' + quantity;
    }
}

function buyNow(productId) {
    var quantity = document.getElementById('quantity').value;

    // Redirect to buy now place order URL
    if (!quantity || quantity <= 0) {
        alert('Please enter a valid quantity.');
        return;
    }
    else {
        window.location.href = '/buy-now-place-order/' + productId + '?quantity=' + quantity;
    }
}
