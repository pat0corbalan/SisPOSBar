let cart = {};

function addToCart(productId, productName, productPrice, isFood) {
    let quantity = document.getElementById('quantity' + productId).value;
    quantity = parseInt(quantity);

    if (quantity > 0) {
        let cartItem = {
            name: productName,
            price: productPrice,
            quantity: quantity,
            isFood: isFood
        };

        // Add to cart
        if (cart[productId]) {
            cart[productId].quantity += quantity;
        } else {
            cart[productId] = cartItem;
        }

        updateCartDisplay();

        // Update the number of products in the cart icon
        let cartCount = document.getElementById('cart-count');
        let currentCount = parseInt(cartCount.textContent);
        cartCount.textContent = currentCount + quantity;
    }
}
