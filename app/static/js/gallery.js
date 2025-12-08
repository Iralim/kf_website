document.addEventListener("DOMContentLoaded", function() {
    let fullscreenSlider = null;
    const fullscreenModal = new bootstrap.Modal(document.getElementById('fullscreenSlider'));

    // Инициализация основной галереи
    const galleryThumbs = new Swiper('.gallery-thumbs', {
        spaceBetween: 10,
        slidesPerView: 5,
        freeMode: true,
        watchSlidesProgress: true,
        breakpoints: {
            320: { slidesPerView: 4 },
            480: { slidesPerView: 5 },
            768: { slidesPerView: 6 }
        }
    });

    const galleryTop = new Swiper('.gallery-top', {
        spaceBetween: 10,
        effect: "slide",
        thumbs: {
            swiper: galleryThumbs
        }
    });

    // Функция открытия полноэкранного слайдера
    window.openFullscreenSlider = function(startIndex = 0) {
        // Инициализация или обновление слайдера
        if (!fullscreenSlider) {
            fullscreenSlider = new Swiper('.fullscreen-slider', {
                initialSlide: startIndex,
                spaceBetween: 10,
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
                keyboard: {
                    enabled: true,
                },
                loop: true,
                effect: 'slide',
                speed: 300
            });
        } else {
            fullscreenSlider.slideTo(startIndex, 0);
        }
        
        // Показываем модальное окно
        fullscreenModal.show();
    };

    // Закрытие по клавише ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && fullscreenModal && fullscreenModal._isShown) {
            fullscreenModal.hide();
        }
    });
});