document.addEventListener("DOMContentLoaded", () => {
    const userButton = document.getElementById("user-button");
    const userSidebar = document.getElementById("user-sidebar");
    const closeUserButton = document.getElementById("close-user");

    // Abrir el sidebar de usuario al hacer clic en el botón
    userButton.addEventListener("click", () => {
        userSidebar.classList.add("active");
    });

    // Cerrar el sidebar de usuario al hacer clic en el botón de cierre
    closeUserButton.addEventListener("click", () => {
        userSidebar.classList.remove("active");
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const cartSidebar = document.getElementById("cart-sidebar");
    const mainContent = document.getElementById("main-content");
    const cartToggle = document.getElementById("cart-toggle"); // Botón para abrir el carrito
    const closeCart = document.getElementById("close-cart"); // Botón para cerrar el carrito

    // Abrir el carrito y aplicar el efecto de blur
    cartToggle.addEventListener("click", () => {
        cartSidebar.classList.add("active");
        mainContent.classList.add("blur");
    });

    // Cerrar el carrito y quitar el efecto de blur
    closeCart.addEventListener("click", () => {
        cartSidebar.classList.remove("active");
        mainContent.classList.remove("blur");
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const userButton = document.getElementById("user-button"); // Botón para abrir el sidebar del usuario
    const userSidebar = document.getElementById("user-sidebar"); // Sidebar del usuario
    const closeUserButton = document.getElementById("close-user"); // Botón para cerrar el sidebar
    const mainContent = document.querySelector("main"); // Contenido principal
    const header = document.querySelector("header"); // Header
    const footer = document.querySelector("footer"); // Footer

    // Abrir el sidebar del usuario y aplicar el efecto de blur
    userButton.addEventListener("click", () => {
        userSidebar.classList.add("active");
        mainContent.classList.add("blur");
        header.classList.add("blur");
        footer.classList.add("blur");
    });

    // Cerrar el sidebar del usuario y quitar el efecto de blur
    closeUserButton.addEventListener("click", () => {
        userSidebar.classList.remove("active");
        mainContent.classList.remove("blur");
        header.classList.remove("blur");
        footer.classList.remove("blur");
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const messageContainer = document.getElementById("message-container");
    if (messageContainer) {
        setTimeout(() => {
            messageContainer.style.transition = "opacity 0.5s ease";
            messageContainer.style.opacity = "0";
            setTimeout(() => {
                messageContainer.remove();
            }, 500); // Esperar a que termine la transición antes de eliminarlo
        }, 3000); // 3 segundos
    }
});