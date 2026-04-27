// Aurora - Particle Effects and Animations

// Particle Animation System
class ParticleSystem {
    constructor(containerId, particleCount = 50) {
        this.container = document.getElementById(containerId);
        this.particleCount = particleCount;
        this.particles = [];
        this.init();
    }

    init() {
        if (!this.container) return;

        for (let i = 0; i < this.particleCount; i++) {
            this.createParticle();
        }

        this.animate();
    }

    createParticle() {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random positioning
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        
        // Random animation timing
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
        
        // Random size variation
        const size = Math.random() * 2 + 1;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        
        this.container.appendChild(particle);
        this.particles.push(particle);
    }

    animate() {
        // Additional animation logic can be added here
        // Currently using CSS animations
    }
}

// Smooth Scroll Navigation
class SmoothScroll {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
}

// Scroll Animation Observer
class ScrollAnimator {
    constructor(selector = '.card, .feature-highlight', threshold = 0.1) {
        this.selector = selector;
        this.threshold = threshold;
        this.init();
    }

    init() {
        const observerOptions = {
            threshold: this.threshold,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll(this.selector).forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    }
}

// Typing Effect for Hero Text
class TypingEffect {
    constructor(elementId, text, speed = 50) {
        this.element = document.getElementById(elementId);
        this.text = text;
        this.speed = speed;
        this.init();
    }

    init() {
        if (!this.element) return;

        let i = 0;
        this.element.textContent = '';
        
        const type = () => {
            if (i < this.text.length) {
                this.element.textContent += this.text.charAt(i);
                i++;
                setTimeout(type, this.speed);
            }
        };

        type();
    }
}

// Mouse Parallax Effect
class MouseParallax {
    constructor(selector = '.hero', intensity = 0.05) {
        this.selector = selector;
        this.intensity = intensity;
        this.init();
    }

    init() {
        const element = document.querySelector(this.selector);
        if (!element) return;

        document.addEventListener('mousemove', (e) => {
            const x = (window.innerWidth - e.pageX * this.intensity) / 100;
            const y = (window.innerHeight - e.pageY * this.intensity) / 100;
            
            element.style.transform = `translateX(${x}px) translateY(${y}px)`;
        });
    }
}

// Glow Effect on Mouse Move
class GlowEffect {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('mousemove', (e) => {
            const cards = document.querySelectorAll('.card');
            
            cards.forEach(card => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });
        });
    }
}

// Initialize All Effects
document.addEventListener('DOMContentLoaded', () => {
    // Particle System
    new ParticleSystem('particles', 50);
    
    // Smooth Scroll
    new SmoothScroll();
    
    // Scroll Animations
    new ScrollAnimator('.card, .feature-highlight', 0.1);
    
    // Optional: Uncomment for additional effects
    // new MouseParallax('.hero', 0.02);
    // new GlowEffect();
    
    console.log('Aurora Effects Initialized');
});
