document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('imagen');
    const previewContainer = document.getElementById('preview-container');
    const form = document.querySelector('form');
    let filesArray = [];

    // Inicializar placeholders
    function initPlaceholders() {
        previewContainer.innerHTML = '';
        for (let i = 0; i < 12; i++) {
            const placeholder = document.createElement('div');
            placeholder.className = 'placeholder';
            placeholder.innerHTML = '+';
            placeholder.onclick = () => fileInput.click();
            previewContainer.appendChild(placeholder);
        }
    }

    // Actualizar el input file con los archivos seleccionados
    function updateFileInput() {
        const dataTransfer = new DataTransfer();
        filesArray.forEach(file => dataTransfer.items.add(file));
        fileInput.files = dataTransfer.files;
    }

    // Mostrar previsualizaciones
    function displayPreviews() {
        initPlaceholders();
        const placeholders = previewContainer.querySelectorAll('.placeholder');
        
        filesArray.forEach((file, index) => {
            if (index >= 12) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                const placeholder = placeholders[index];
                placeholder.className = 'image-container';
                placeholder.innerHTML = `
                    <img src="${e.target.result}" alt="Preview">
                    <button type="button" class="remove-btn" data-index="${index}">X</button>
                `;
                
                placeholder.querySelector('.remove-btn').addEventListener('click', function(e) {
                    e.stopPropagation();
                    filesArray.splice(index, 1);
                    updateFileInput();
                    displayPreviews();
                });
            };
            reader.readAsDataURL(file);
        });
    }

    // Manejar selección de archivos
    fileInput.addEventListener('change', function(e) {
        const newFiles = Array.from(e.target.files);
        if (filesArray.length + newFiles.length > 12) {
            alert('Máximo 12 imágenes permitidas');
            return;
        }
        filesArray = filesArray.concat(newFiles);
        updateFileInput();
        displayPreviews();
    });

    // Asegurar que se envíen todos los archivos
    form.addEventListener('submit', function(e) {
        updateFileInput(); // Actualizar por última vez antes de enviar
        
        // Verificar que hay archivos para enviar
        if (fileInput.files.length !== filesArray.length) {
            e.preventDefault();
            alert('Error al preparar los archivos. Intente nuevamente.');
            return;
        }
    });

    // Inicializar
    initPlaceholders();

    // Resto de tu código para manejo de precios...
});

