document.addEventListener('DOMContentLoaded', function() {
    const productsWithCarousel = document.querySelectorAll('.product_image');
    
    productsWithCarousel.forEach(container => {
        const images = container.querySelectorAll('.product-img');
        
        if (images.length > 1) {
            let currentIndex = 0;
            const prevBtn = container.parentElement.querySelector('.carousel-prev');
            const nextBtn = container.parentElement.querySelector('.carousel-next');
            
            // Función para mostrar la imagen actual
            function showImage(index) {
                images.forEach(img => img.classList.remove('active'));
                images[index].classList.add('active');
            }
            
            // Evento para botón anterior
            if (prevBtn) {
                prevBtn.addEventListener('click', () => {
                    currentIndex = (currentIndex - 1 + images.length) % images.length;
                    showImage(currentIndex);
                });
            }
            
            // Evento para botón siguiente
            if (nextBtn) {
                nextBtn.addEventListener('click', () => {
                    currentIndex = (currentIndex + 1) % images.length;
                    showImage(currentIndex);
                });
            }
            
            // Mostrar la primera imagen al cargar
            showImage(0);
        }
    });
});

