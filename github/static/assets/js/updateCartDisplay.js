function updateCartDisplay() {
    let cartList = document.getElementById('cart');
    let total = 0;

    // Clear previous cart items
    cartList.innerHTML = '';

    // Populate cart items
    for (let productId in cart) {
        let item = cart[productId];
        let listItem = document.createElement('li');
        listItem.textContent = `${item.name} x${item.quantity} - $${(item.price * item.quantity).toFixed(2)}`;

        // Add remove button
        let removeButton = document.createElement('button');
        removeButton.textContent = 'Eliminar';
        removeButton.className = 'btn btn-danger btn-sm';
        removeButton.onclick = function() {
            removeFromCart(productId);
        };
        listItem.appendChild(removeButton);

        cartList.appendChild(listItem);
        total += item.price * item.quantity;
    }

    // Update total
    document.getElementById('total').textContent = total.toFixed(2);

    // Update hidden input for form submission
    document.getElementById('cart_input').value = JSON.stringify(cart);
}
