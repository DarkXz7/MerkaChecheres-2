document.addEventListener('DOMContentLoaded', () => {
    const mensajeDiv = document.getElementById('mensaje');

    // Verifica si el div existe y tiene contenido
    if (mensajeDiv && mensajeDiv.innerHTML.trim() !== '') {
        // Usa setTimeout para iniciar la transición después de 5 segundos
        setTimeout(() => {
            mensajeDiv.classList.add('oculto'); // Agrega la clase para la transición

            // Después de la transición (1s), oculta completamente el elemento
            setTimeout(() => {
                mensajeDiv.style.display = 'none';
            }, 1000); // 1000 ms = duración de la transición en CSS
        }, 5000); // 5000 ms = tiempo antes de iniciar la transición
    } else {
        // Si no hay contenido, oculta el div inmediatamente
        mensajeDiv.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const telefonoInput = document.getElementById('telefono');

    telefonoInput.addEventListener('input', function () {
        // Elimina cualquier carácter que no sea un número
        this.value = this.value.replace(/[^0-9]/g, '');

        if (this.value.length > 10) {
            this.value = this.value.slice(0, 10);
        }
    });
});