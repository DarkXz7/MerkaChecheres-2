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
