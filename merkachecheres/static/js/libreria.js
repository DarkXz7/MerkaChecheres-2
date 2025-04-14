// Obtener los elementos necesarios
var modal = document.getElementById("modal_login");
var openBtn = document.getElementById("open_login");
var closeBtn = document.getElementById("close_login");

// Abrir el modal cuando se hace clic en el botón de "Iniciar Sesión"
openBtn.onclick = function() {
    modal.style.display = "flex";
}

// Cerrar el modal cuando se hace clic en la "x"
closeBtn.onclick = function() {
    modal.style.display = "none";
}

// Cerrar el modal cuando el usuario hace clic fuera de la caja de inicio de sesión
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
