function obtenerHora() {
      const ahora = new Date();
      let horas = ahora.getHours();
      const minutos = ahora.getMinutes().toString().padStart(2, '0');
      const ampm = horas >= 12 ? 'p. m.' : 'a. m.';
      horas = horas % 12;
      horas = horas ? horas : 12;
      return `${horas}:${minutos} ${ampm}`;
    }

    function obtenerFecha() {
      const opciones = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      return new Date().toLocaleDateString('es-ES', opciones);
    }

    function enviarMensaje() {
      const input = document.getElementById("entradaTexto");
      const texto = input.value.trim();
      if (texto !== "") {
        const zonaMensajes = document.getElementById("zonaMensajes");
        const mensaje = document.createElement("div");
        mensaje.className = "mensaje usuario";

        const parrafo = document.createElement("p");
        parrafo.innerText = texto;

        const spanHora = document.createElement("span");
        spanHora.className = "horaMensaje";
        spanHora.innerText = obtenerHora();

        parrafo.appendChild(spanHora);
        mensaje.appendChild(parrafo);
        zonaMensajes.appendChild(mensaje);

        zonaMensajes.scrollTop = zonaMensajes.scrollHeight;
        input.value = "";
      }
    }

    document.getElementById("entradaTexto").addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        enviarMensaje();
      }
    });

    document.getElementById("fechaHoy").innerText = obtenerFecha();

    // Función para guardar mensajes en localStorage
function guardarMensajesEnStorage(mensajes) {
  localStorage.setItem('historialMensajes', JSON.stringify(mensajes));
}

// Función para obtener mensajes desde localStorage
function obtenerMensajesDesdeStorage() {
  const mensajes = localStorage.getItem('historialMensajes');
  return mensajes ? JSON.parse(mensajes) : [];
}

// Función para mostrar un mensaje en pantalla (puede usarse para cargar historial)
function mostrarMensaje(texto, hora) {
  const zonaMensajes = document.getElementById("zonaMensajes");
  const mensaje = document.createElement("div");
  mensaje.className = "mensaje usuario";

  const parrafo = document.createElement("p");
  parrafo.innerText = texto;

  const spanHora = document.createElement("span");
  spanHora.className = "horaMensaje";
  spanHora.innerText = hora;

  parrafo.appendChild(spanHora);
  mensaje.appendChild(parrafo);
  zonaMensajes.appendChild(mensaje);

  zonaMensajes.scrollTop = zonaMensajes.scrollHeight;
}

function enviarMensaje() {
  const input = document.getElementById("entradaTexto");
  const texto = input.value.trim();
  if (texto !== "") {
    const hora = obtenerHora();
    mostrarMensaje(texto, hora);

    const mensajes = obtenerMensajesDesdeStorage();
    mensajes.push({ texto, hora });
    guardarMensajesEnStorage(mensajes);

    input.value = "";
  }
}

window.addEventListener('load', () => {
  const mensajes = obtenerMensajesDesdeStorage();
  mensajes.forEach(({ texto, hora }) => {
    mostrarMensaje(texto, hora);
  });
});



document.addEventListener('DOMContentLoaded', function() {
    const chatItems = document.querySelectorAll('.chat-item');
    const cabeceraChat = document.querySelector('.cabeceraChat');

    function actualizarCabeceraChat(producto) {
        cabeceraChat.innerHTML = `
            <img src="${producto.imagen_url}" alt="${producto.titulo}" style="width:50px;height:50px;object-fit:cover;border-radius:6px;">
            <div>
                <div><strong>${producto.titulo}</strong></div>
                <div>Vendedor: ${producto.vendedor}</div>
                <div>Precio: $${producto.precio}</div>
            </div>
        `;
    }

    chatItems.forEach(item => {
    item.addEventListener('click', function() {
        // Quitar la clase 'active' de todos
        chatItems.forEach(i => i.classList.remove('active'));
        // Agregar la clase 'active' al seleccionado
        this.classList.add('active');

        const producto = {
            id: this.dataset.productoId,
            titulo: this.dataset.titulo,
            vendedor: this.dataset.vendedor,
            precio: this.dataset.precio,
            imagen_url: this.dataset.imagenUrl
        };
        actualizarCabeceraChat(producto);
        // Aquí puedes cargar los mensajes del chat correspondiente si lo implementas
    });
});
});