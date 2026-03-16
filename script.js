// Basic page transition and animation logic
document.addEventListener('DOMContentLoaded', () => {
    // Reveal main content
    const main = document.querySelector('main');
    if (main) {
        main.style.opacity = '0';
        main.style.transform = 'translateY(20px)';
        main.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';

        setTimeout(() => {
            main.style.opacity = '1';
            main.style.transform = 'translateY(0)';
        }, 100);
    }

    // Nav Link Hover effect (Optional enhancement)
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            if (!link.classList.contains('active')) {
                link.style.color = 'var(--text-white)';
            }
        });
        link.addEventListener('mouseleave', () => {
            if (!link.classList.contains('active')) {
                link.style.color = 'var(--text-slate)';
            }
        });
    });

    // Intersection Observer for active navigation links (Scroll Spy)
    const sectionObserverOptions = {
        threshold: 0.1,
        rootMargin: "-150px 0px -70% 0px" // Trigger when section is near the top
    };

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                const activeNavLink = document.querySelector(`.nav-links a[href="#${id}"]`);
                
                if (activeNavLink) {
                    navLinks.forEach(link => link.classList.remove('active'));
                    activeNavLink.classList.add('active');
                }
            }
        });
    }, sectionObserverOptions);

    const sections = document.querySelectorAll('section[id]');
    sections.forEach(section => sectionObserver.observe(section));

    // Handle all internal anchor links for "perfect" smooth scrolling
    const allLinks = document.querySelectorAll('a[href^="#"]');
    allLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const hash = link.getAttribute('href');
            if (hash === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(hash);
            if (target) {
                // Ensure mobile menu closes if open
                const mobileToggle = document.querySelector('.mobile-toggle');
                const navLinksContainer = document.querySelector('.nav-links');
                if (mobileToggle && mobileToggle.classList.contains('active')) {
                    mobileToggle.classList.remove('active');
                    navLinksContainer.classList.remove('active');
                    document.body.style.overflow = 'initial';
                }

                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update URL hash without jumping
                history.pushState(null, null, hash);
            }
        });
    });

    // Reveal Observer for scroll animations
    const revealObserverOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -10% 0px'
    };

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                revealObserver.unobserve(entry.target);
            }
        });
    }, revealObserverOptions);

    const revealElements = document.querySelectorAll('.reveal');
    revealElements.forEach(el => revealObserver.observe(el));

    // Handle initial fragment if present on load
    if (window.location.hash) {
        const targetSection = document.querySelector(window.location.hash);
        if (targetSection) {
            setTimeout(() => {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }, 600);
        }
    }

    // Mobile Menu Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinksContainer = document.querySelector('.nav-links');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            mobileToggle.classList.toggle('active');
            navLinksContainer.classList.toggle('active');
            document.body.style.overflow = navLinksContainer.classList.contains('active') ? 'hidden' : 'initial';
        });
    }
});
