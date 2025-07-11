const cantidadText = document.getElementById('cantidadText');
const btnSumar = document.getElementById('btn-sumar');
const btnRestar = document.getElementById('btn-restar');

let cantidad = 1; // Valor inicial

btnSumar.addEventListener('click', () => {
    cantidad++;
    cantidadText.textContent = cantidad;
});

btnRestar.addEventListener('click', () => {
    if (cantidad > 0) {
        cantidad--;
        cantidadText.textContent = cantidad;
    }
});

document.addEventListener("DOMContentLoaded", () => {
    // Formatear fechas en tiempo real
    const fechas = document.querySelectorAll('.fecha-publicacion');
    fechas.forEach(el => {
        const fechaISO = el.dataset.fecha;
        const fecha = new Date(fechaISO);
        const opciones = {
            day: '2-digit', month: '2-digit', year: 'numeric',
            hour: '2-digit', minute: '2-digit',
            hour12: true
        };
        el.textContent = fecha.toLocaleString('es-CO', opciones);
    });

    // Toggle para mostrar/ocultar formulario de edición de reseñas
    document.querySelectorAll('.toggleEditBtn').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            const form = document.querySelector(`form[action$="${id}/"]`);
            if (form) {
                form.classList.toggle('d-none');
            }
        });
    });
});




document.addEventListener('DOMContentLoaded', function() {
    let cantidad = 1;
    const stock = {{ producto.stock }};
    const cantidadText = document.getElementById('cantidadText');
    const btnSumar = document.getElementById('btn-sumar');
    const btnRestar = document.getElementById('btn-restar');
    const cantidadInput = document.getElementById('cantidadInput');

    function actualizarBotones() {
        btnSumar.disabled = cantidad >= stock;
        btnRestar.disabled = cantidad <= 1;
    }

    actualizarBotones();

    btnSumar.addEventListener('click', function() {
        if (cantidad < stock) {
            cantidad++;
            cantidadText.textContent = cantidad;
            cantidadInput.value = cantidad;
            actualizarBotones();
        }
    });

    btnRestar.addEventListener('click', function() {
        if (cantidad > 1) {
            cantidad--;
            cantidadText.textContent = cantidad;
            cantidadInput.value = cantidad;
            actualizarBotones();
        }
    });
});



