let cart = [];

document.addEventListener("DOMContentLoaded", () => {
    setupEventListeners();
});

function setupEventListeners() {
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", event => handleAddToCart(event));
    });

    document.getElementById('cart-toggle').addEventListener('click', toggleCartSidebar);
    document.getElementById('clear-cart').addEventListener('click', clearCart);
    document.getElementById('checkout').addEventListener('click', checkout);
}

function handleAddToCart(event) {
    const product = event.target.closest(".card");
    const name = product.querySelector(".product-name").innerText;
    const price = parseFloat(product.querySelector(".product-price").innerText.replace("$", ""));
    addToCart(name, price);
}

function toggleCartSidebar() {
    document.getElementById('cart-sidebar').classList.toggle('active');
}

function clearCart() {
    if (cart.length > 0) {
        cart = [];
        updateCart();
        alert('El carrito ha sido vaciado');
    }
}

function checkout() {
    if (cart.length === 0) {
        alert("El carrito está vacío. Agrega productos antes de pagar.");
        return;
    }
    let total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    alert(`Compra realizada. Total a pagar: $${total.toFixed(2)}`);
    cart = [];
    updateCart();
}

function addToCart(name, price) {
    let existingItem = cart.find(item => item.name === name);
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({ name, price, quantity: 1 });
    }
    updateCart();
}

function updateCart() {
    let cartItems = document.getElementById("cart-items");
    let cartTotal = document.getElementById("cart-total");
    let cartCount = document.getElementById("cart-count");
    let emptyCartMessage = "<li class='list-group-item text-center'>El carrito está vacío</li>";

    cartItems.innerHTML = "";
    let total = 0;
    let count = 0;

    if (cart.length === 0) {
        cartItems.innerHTML = emptyCartMessage;
        cartTotal.innerText = "0.00";
        cartCount.innerText = "0";
        return;
    }

    cart.forEach((item, index) => {
        total += item.price * item.quantity;
        count += item.quantity;

        let li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between align-items-center";
        li.innerHTML = `
            <span>${item.name} - $${item.price} x${item.quantity}</span>
            <div>
                <button class="btn btn-sm btn-danger" onclick="removeFromCart(${index})">
                    <i class="bi bi-trash"></i>
                </button>
                <button class="btn btn-sm btn-success" onclick="increaseQuantity(${index})">
                    <i class="bi bi-plus"></i>
                </button>
                <button class="btn btn-sm btn-warning" onclick="decreaseQuantity(${index})">
                    <i class="bi bi-dash"></i>
                </button>
            </div>
        `;
        cartItems.appendChild(li);
    });

    cartTotal.innerText = total.toFixed(2);
    cartCount.innerText = count;
}

function removeFromCart(index) {
    cart.splice(index, 1);
    updateCart();
}

function increaseQuantity(index) {
    cart[index].quantity++;
    updateCart();
}

function decreaseQuantity(index) {
    if (cart[index].quantity > 1) {
        cart[index].quantity--;
    } else {
        cart.splice(index, 1);
    }
    updateCart();
}

document.addEventListener("DOMContentLoaded", () => {
    const carritoButton = document.getElementById("carrito-button");
    const cartSidebar = document.getElementById("cart-sidebar");
    const closeCartButton = document.getElementById("close-cart");

    // Abrir el carrito al hacer clic en el botón
    carritoButton.addEventListener("click", () => {
        cartSidebar.classList.add("active");
    });

    // Cerrar el carrito al hacer clic en el botón de cierre
    closeCartButton.addEventListener("click", () => {
        cartSidebar.classList.remove("active");
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const carritoButton = document.getElementById("carrito-button");
    const cartSidebar = document.getElementById("cart-sidebar");
    const closeCartButton = document.getElementById("close-cart");
    const mainContent = document.querySelector("main"); // Selecciona el contenido principal
    const header = document.querySelector("header"); // Selecciona el header
    const footer = document.querySelector("footer"); // Selecciona el footer

    // Abrir el carrito al hacer clic en el botón
    carritoButton.addEventListener("click", () => {
        cartSidebar.classList.add("active");
        mainContent.classList.add("blur");
        header.classList.add("blur");
        footer.classList.add("blur");
    });

    // Cerrar el carrito al hacer clic en el botón de cierre
    closeCartButton.addEventListener("click", () => {
        cartSidebar.classList.remove("active");
        mainContent.classList.remove("blur");
        header.classList.remove("blur");
        footer.classList.remove("blur");
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const closeCartButton = document.getElementById("close-cart");
    const cartSidebar = document.getElementById("cart-sidebar");

    // Cerrar el carrito al hacer clic en el botón de cierre
    closeCartButton.addEventListener("click", () => {
        cartSidebar.classList.remove("active");
    });
});