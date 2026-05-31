// ============================================
// Event Management System - Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initAnimations();
    initCounters();
    initAlerts();
});

// ---- Navbar scroll effect ----
function initNavbar() {
    const navbar = document.querySelector('.navbar-custom');
    if (!navbar) return;
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
    });
}

// ---- Scroll animations ----
function initAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// ---- Animated counters ----
function initCounters() {
    const counters = document.querySelectorAll('.counter');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                const duration = 2000;
                const step = target / (duration / 16);
                let current = 0;
                const timer = setInterval(() => {
                    current += step;
                    if (current >= target) {
                        counter.textContent = target.toLocaleString();
                        clearInterval(timer);
                    } else {
                        counter.textContent = Math.floor(current).toLocaleString();
                    }
                }, 16);
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));
}

// ---- Auto-dismiss alerts ----
function initAlerts() {
    const alerts = document.querySelectorAll('.alert-auto-dismiss');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        }, 4000);
    });
}

// ---- Search events ----
function searchEvents() {
    const query = document.getElementById('eventSearch').value.toLowerCase();
    const cards = document.querySelectorAll('.event-card-item');
    cards.forEach(card => {
        const name = card.getAttribute('data-name').toLowerCase();
        const type = card.getAttribute('data-type').toLowerCase();
        card.style.display = (name.includes(query) || type.includes(query)) ? '' : 'none';
    });
}

// ---- Filter events by type ----
function filterEvents(type) {
    const cards = document.querySelectorAll('.event-card-item');
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    cards.forEach(card => {
        if (type === 'All' || card.getAttribute('data-type') === type) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

// ---- Confirm delete ----
function confirmDelete(url, name) {
    if (confirm(`Are you sure you want to delete "${name}"?`)) {
        window.location.href = url;
    }
}
