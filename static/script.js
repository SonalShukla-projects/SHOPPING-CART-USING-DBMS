document.addEventListener('DOMContentLoaded', () => {
    const productsContainer = document.getElementById('products-container');
    const cartContainer = document.getElementById('cart-container');
    const cartItemsEl = document.getElementById('cart-items');
    const cartTotalEl = document.getElementById('cart-total');
    const cartCountEl = document.getElementById('cart-count');
    const viewCartBtn = document.getElementById('view-cart-btn');
    const closeCartBtn = document.getElementById('close-cart-btn');
    const confirmOrderBtn = document.getElementById('confirm-order-btn');

    let cart = {};

    // Load products
    fetch('/api/products')
        .then(res => res.json())
        .then(products => {
            productsContainer.innerHTML = '';
            products.forEach(p => {
                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <img src="${p.image_url || 'https://via.placeholder.com/200'}" alt="${p.name}">
                    <h3>${p.name}</h3>
                    <p>${p.description || ''}</p>
                    <p>Price: $${p.price}</p>
                    <p>Stock: ${p.stock}</p>
                    <button onclick="addToCart(${p.id})">Add to Cart</button>
                `;
                productsContainer.appendChild(card);
            });
        });

    // Add to cart
    window.addToCart = function(productId) {
        fetch('/api/cart/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId, quantity: 1 })
        })
        .then(res => res.json())
        .then(data => {
            cart = data.cart;
            updateCartCount();
            alert('Product added to cart!');
        });
    }

    function updateCartCount() {
        let count = 0;
        for (let pid in cart) count += cart[pid];
        cartCountEl.innerText = count;
    }

    function loadCart() {
        fetch('/api/cart')
        .then(res => res.json())
        .then(data => {
            cart = data;
            cartItemsEl.innerHTML = '';
            let total = 0;
            for (let pid in cart) {
                const qty = cart[pid];
                const li = document.createElement('li');
                li.innerText = `Product ID ${pid} x ${qty}`;
                cartItemsEl.appendChild(li);
                total += qty; // Price placeholder
            }
            cartTotalEl.innerText = total;
        });
    }

    viewCartBtn.addEventListener('click', () => {
        loadCart();
        cartContainer.style.display = 'block';
    });

    closeCartBtn.addEventListener('click', () => {
        cartContainer.style.display = 'none';
    });

    confirmOrderBtn.addEventListener('click', () => {
        fetch('/order/confirm', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            alert(data.status + (data.total ? ` Total: $${data.total}` : ''));
            cartContainer.style.display = 'none';
            cart = {};
            updateCartCount();
        });
    });

});
