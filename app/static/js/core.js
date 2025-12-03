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

    function updateNavbar() {
        if (!navbar) return;

        if (window.scrollY > 50) {
            navbar.style.padding = '8px 0';
            navbar.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.padding = '15px 0';
            navbar.style.boxShadow = 'none';
        }
    }

    updateNavbar();

    window.addEventListener('scroll', updateNavbar);


    // ===========================
    // CLOSE BURGER ON LINK CLICK
    // ===========================
    document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
        link.addEventListener('click', function () {
            let navbar = document.getElementById('navbarNav');
            let bsCollapse = bootstrap.Collapse.getInstance(navbar);

            if (bsCollapse) {
                bsCollapse.hide();
            }
        });
    });
});
