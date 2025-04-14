let currentIndex = 0;

  function moveSlide(direction) {
    const carousel = document.getElementById("carousel");
    const cards = carousel.querySelectorAll(".seller_card");
    const cardWidth = cards[0].offsetWidth + 16; // ancho + gap
    const visibleCards = Math.floor(carousel.parentElement.offsetWidth / cardWidth);
    const maxIndex = cards.length - visibleCards;

    currentIndex += direction;
    if (currentIndex < 0) currentIndex = 0;
    if (currentIndex > maxIndex) currentIndex = maxIndex;

    carousel.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
  }