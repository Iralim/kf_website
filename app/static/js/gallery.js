document.addEventListener("DOMContentLoaded", function() {

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

});