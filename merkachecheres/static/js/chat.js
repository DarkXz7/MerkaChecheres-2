// --- CHAT FUNCIONAL BIDIRECCIONAL Y RESPONSIVO ---

// Variables globales para el chat seleccionado
let productoSeleccionado = null;
let otroUsuarioId = null;

// Al cargar la página, selecciona el primer chat si existe
document.addEventListener('DOMContentLoaded', function () {
    const chatItems = document.querySelectorAll('.chat-item');
    if (chatItems.length > 0) {
        chatItems[0].classList.add('active');
        productoSeleccionado = chatItems[0].dataset.productoId;
        otroUsuarioId = chatItems[0].dataset.vendedor;
        actualizarCabeceraChat(chatItems[0]);
        cargarMensajes();
    }

    // Maneja el click en los chats
    chatItems.forEach(item => {
        item.addEventListener('click', function () {
            chatItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            productoSeleccionado = this.dataset.productoId;
            otroUsuarioId = this.dataset.vendedor;
            actualizarCabeceraChat(this);
            cargarMensajes();
        });
    });

    // Muestra la fecha de hoy en el separador
    const fechaHoy = document.getElementById("fechaHoy");
    if (fechaHoy) fechaHoy.innerText = obtenerFecha();

    // Permite enviar mensaje con Enter
    const entrada = document.getElementById("entradaTexto");
    if (entrada) {
        entrada.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                enviarMensaje();
            }
        });
    }
});

// Actualiza la cabecera del chat con los datos del producto
function actualizarCabeceraChat(item) {
    const cabecera = document.querySelector('.cabeceraChat');
    if (!cabecera || !item) return;
    cabecera.innerHTML = `
        <img src="${item.dataset.imagenUrl}" alt="${item.dataset.titulo}" style="width:50px;height:50px;object-fit:cover;border-radius:6px;">
        <div>
            <div><strong>${item.dataset.titulo}</strong></div>
            <div>Vendedor: ${item.dataset.vendedor}</div>
            <div>Precio: $${item.dataset.precio}</div>
        </div>
    `;
}

// Devuelve la fecha de hoy en formato largo
function obtenerFecha() {
    const opciones = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date().toLocaleDateString('es-ES', opciones);
}

// Carga los mensajes del chat actual desde el backend
function cargarMensajes() {
    if (!productoSeleccionado || !otroUsuarioId) return;
    fetch(`/api/mensajes_chat/?producto_id=${productoSeleccionado}&otro_usuario_id=${otroUsuarioId}`)
        .then(r => r.json())
        .then(data => {
            const zona = document.getElementById('zonaMensajes');
            if (!zona) return;
            zona.innerHTML = '';
            // Separador de fecha
            zona.innerHTML += `<div class="separadorFecha" id="fechaHoy">${obtenerFecha()}</div>`;
            if (data.mensajes && data.mensajes.length > 0) {
                data.mensajes.forEach(m => {
                    const clase = m.emisor_id == window.usuarioId ? 'mensaje usuario' : 'mensaje agente';
                    zona.innerHTML += `<div class="${clase}"><p>${m.texto}<span class="horaMensaje">${m.fecha.slice(11,16)}</span></p></div>`;
                });
            } else {
                zona.innerHTML += `<div class="mensaje agente"><p>¡Hola! ¿En qué puedo ayudarte?<span class="horaMensaje">${obtenerHora()}</span></p></div>`;
            }
            zona.scrollTop = zona.scrollHeight;
        });
}

// Envía un mensaje al backend y lo muestra inmediatamente en el chat
function enviarMensaje() {
    const input = document.getElementById('entradaTexto');
    if (!input) return;
    const texto = input.value.trim();
    if (!texto || !productoSeleccionado || !otroUsuarioId) return;

    // Mostrar el mensaje inmediatamente en el chat
    const zona = document.getElementById('zonaMensajes');
    if (zona) {
        const clase = 'mensaje usuario';
        zona.innerHTML += `<div class="${clase}"><p>${texto}<span class="horaMensaje">${obtenerHora()}</span></p></div>`;
        zona.scrollTop = zona.scrollHeight;
    }

    // Limpiar el input inmediatamente después de enviar
    input.value = '';

    fetch('/api/mensajes_chat/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            producto_id: productoSeleccionado,
            texto: texto,
            receptor_id: otroUsuarioId
        })
    }).then(r => r.json()).then(resp => {
        if (!resp.error) {
            // Opcional: recargar mensajes para sincronizar con el backend
            cargarMensajes();
        }
    });

    // Si el chat no está en la lista, agrégalo visualmente (opcional, para mejor UX)
    const chatList = document.querySelector('.listaChats ul.list-group');
    if (chatList && ![...chatList.children].some(li => li.dataset.productoId == productoSeleccionado)) {
        // Puedes obtener los datos del chat actual de los inputs o variables globales
        const titulo = document.querySelector('.cabeceraChat strong')?.innerText || '';
        const vendedor = otroUsuarioId; // O busca el nombre si lo tienes
        const precio = document.querySelector('.cabeceraChat [data-precio]')?.dataset.precio || '';
        const imagenUrl = document.querySelector('.cabeceraChat img')?.src || '';
        const li = document.createElement('li');
        li.className = 'list-group-item chat-item active';
        li.dataset.productoId = productoSeleccionado;
        li.dataset.titulo = titulo;
        li.dataset.vendedor = vendedor;
        li.dataset.precio = precio;
        li.dataset.imagenUrl = imagenUrl;
        li.innerHTML = `<strong>${vendedor} - ${titulo}</strong>`;
        chatList.appendChild(li);
    }
}

// Devuelve la hora actual en formato 12h
function obtenerHora() {
    const ahora = new Date();
    let horas = ahora.getHours();
    const minutos = ahora.getMinutes().toString().padStart(2, '0');
    const ampm = horas >= 12 ? 'p. m.' : 'a. m.';
    horas = horas % 12;
    horas = horas ? horas : 12;
    return `${horas}:${minutos} ${ampm}`;
}

// Recarga automática cada 3 segundos
setInterval(() => {
    if (productoSeleccionado && otroUsuarioId) cargarMensajes();
}, 3000);
// --- FIN DEL CHAT FUNCIONAL ---