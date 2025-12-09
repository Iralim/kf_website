document.addEventListener("DOMContentLoaded", function () {

    // ===========================
    // AOS INIT
    // ===========================
if (window.AOS) {
    AOS.init({
        // Основные настройки
        offset: 50,                   // Уменьшил с 120px - начинать раньше
        delay: 0,
        duration: 800,                // Немного дольше для плавности
        easing: 'ease-out-cubic',     // Более плавное easing
        once: true,
        
        // КРИТИЧЕСКО ВАЖНО для вашей проблемы:
        anchorPlacement: 'center-bottom', // Когда ЦЕНТР элемента касается НИЗА окна
        
        // Дополнительные настройки
        startEvent: 'DOMContentLoaded',
        disable: false,
        throttleDelay: 99,
        
        // Оптимизация производительности
        disableMutationObserver: false,
        debounceDelay: 50
    });
    
    // ДОПОЛНИТЕЛЬНО: Перезапуск после полной загрузки страницы
    window.addEventListener('load', function() {
        AOS.refreshHard(); // Форсированный пересчет позиций
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
