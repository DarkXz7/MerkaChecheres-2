document.addEventListener('DOMContentLoaded', function() {
    const departamentoSelect = document.getElementById('departamento');
    const municipioSelect = document.getElementById('municipio');

    // Función para cargar los municipios según el departamento seleccionado
    function cargarMunicipios() {
        // Obtener el departamento seleccionado
        const departamentoSeleccionado = departamentoSelect.value;
        
        // Limpiar el select de municipios
        municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
        
        // Si se seleccionó un departamento válido
        if (departamentoSeleccionado && departamentosMunicipios[departamentoSeleccionado]) {
            // Ordenar los municipios alfabéticamente
            const municipios = departamentosMunicipios[departamentoSeleccionado].sort();
            
            // Agregar cada municipio como una opción
            municipios.forEach(function(municipio) {
                const option = document.createElement('option');
                option.value = municipio;
                option.textContent = municipio;
                municipioSelect.appendChild(option);
            });
        }
    }

    // Escuchar cambios en el select de departamento
    departamentoSelect.addEventListener('change', cargarMunicipios);

    // Cargar municipios iniciales si ya hay un departamento seleccionado
    if (departamentoSelect.value) {
        cargarMunicipios();
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

  function toggleDropdown() {
    const submenu = document.getElementById('submenuProductos');
    submenu.style.display = submenu.style.display === 'none' ? 'block' : 'none';
  }

  // Cerrar menú si se hace clic fuera
  document.addEventListener('click', function (e) {
    const menu = document.getElementById('submenuProductos');
    if (!e.target.closest('.dropdown')) {
      menu.style.display = 'none';
    }
  });



  //mostrar el icono del ojo de contraseña 

const passwordInput = document.getElementById('password_actual');
const togglePassword = document.getElementById('togglePassword');
const iconEye = document.getElementById('iconEye');

togglePassword.addEventListener('click', function () {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    iconEye.classList.toggle('fa-eye');
    iconEye.classList.toggle('fa-eye-slash');
});
