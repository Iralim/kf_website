document.addEventListener("DOMContentLoaded", function () {

    let fullscreenSlider = null;
    const fullscreenModalEl = document.getElementById('fullscreenSlider');
    const fullscreenModal = new bootstrap.Modal(fullscreenModalEl);

    /* =========================
       THUMB GALLERY
       ========================= */

    const galleryThumbs = new Swiper('.gallery-thumbs', {
        spaceBetween: 15,
        slidesPerView: 4,
        freeMode: true,
        watchSlidesProgress: true,
        breakpoints: {
            320: { slidesPerView: 2 },
            480: { slidesPerView: 3 },
            768: { slidesPerView: 4 },
            1024: { slidesPerView: 6 }
        }
    });

    /* =========================
       OPEN FULLSCREEN
       ========================= */

    window.openFullscreenSlider = function (startIndex = 0) {

        if (!fullscreenSlider) {
            fullscreenSlider = new Swiper('.fullscreen-slider', {
                loop: true,
                spaceBetween: 10,
                initialSlide: startIndex,
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev'
                },
                keyboard: {
                    enabled: true
                },
                effect: 'slide',
                speed: 300
            });
        } else {
            // при loop используем slideToLoop
            fullscreenSlider.slideToLoop(startIndex, 0);
        }

        fullscreenModal.show();
    };

    /* =========================
       ESC close
       ========================= */

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && fullscreenModalEl.classList.contains('show')) {
            fullscreenModal.hide();
        }
    });

    /* =========================
       FIX resize when modal opens
       ========================= */

    fullscreenModalEl.addEventListener('shown.bs.modal', function () {
        if (fullscreenSlider) {
            fullscreenSlider.update();
        }
    });

});
