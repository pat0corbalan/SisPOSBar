function removeFromCart(productId) {
    let quantityToRemove = cart[productId].quantity;
    delete cart[productId];
    updateCartDisplay();

    // Update the number of products in the cart icon
    let cartCount = document.getElementById('cart-count');
    let currentCount = parseInt(cartCount.textContent);
    cartCount.textContent = currentCount - quantityToRemove;
}
