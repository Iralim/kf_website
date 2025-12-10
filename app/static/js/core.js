document.addEventListener("DOMContentLoaded", () => {
    
    // ===========================
    // AOS INITIALIZATION
    // ===========================
    if (window.AOS) {
        AOS.init({
            offset: 50,
            delay: 0,
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            anchorPlacement: 'center-bottom',
            startEvent: 'DOMContentLoaded',
            disable: false,
            throttleDelay: 99,
            disableMutationObserver: false,
            debounceDelay: 50
        });
        
        // Перезапуск после полной загрузки страницы
        window.addEventListener('load', () => {
            if (AOS.refreshHard) {
                AOS.refreshHard();
            }
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
    
    if (navbar) {
        updateNavbar();
        window.addEventListener('scroll', updateNavbar);
    }
    
    // ===========================
    // CLOSE BURGER MENU ON LINK CLICK
    // ===========================
    document.querySelectorAll('.navbar-nav .nav-link').forEach((link) => {
        link.addEventListener('click', () => {
            const navbarCollapse = document.getElementById('navbarNav');
            
            if (!navbarCollapse) return;
            
            // Bootstrap 5
            if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
                const collapseInstance = bootstrap.Collapse.getInstance(navbarCollapse);
                if (collapseInstance) {
                    collapseInstance.hide();
                }
            }
            // Bootstrap 4 (для обратной совместимости)
            else if (typeof $ !== 'undefined' && $.fn.collapse) {
                $(navbarCollapse).collapse('hide');
            }
        });
    });
});