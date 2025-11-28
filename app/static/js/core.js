document.addEventListener("DOMContentLoaded", function () {

    // ===========================
    // AOS INIT
    // ===========================
    if (window.AOS) {
        AOS.init({
            duration: 800,
            once: true,
            offset: 100
        });
    }

    // ===========================
    // BACK TO TOP BUTTON
    // ===========================
    const backToTopButton = document.querySelector('.back-to-top');

    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            backToTopButton.classList.toggle('active', window.scrollY > 300);
        });

        backToTopButton.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ===========================
    // NAVBAR SCROLL EFFECT
    // ===========================
    const navbar = document.querySelector('.navbar');

    if (navbar) {
        window.addEventListener('scroll', () => {
            const isScrolled = window.scrollY > 50;

            navbar.classList.toggle('scrolled', isScrolled);
        });
    }

});
