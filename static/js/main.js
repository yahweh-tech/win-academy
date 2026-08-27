/**
 * WIN PROFESSIONAL ACADEMY - Main Javascript
 * Handles mobile navigation, dynamic animations, alert dismissals, and form UX.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Navigation Drawer Toggle
  const mobileToggle = document.getElementById('mobileNavToggle');
  const navMenu = document.getElementById('navMenu');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      navMenu.classList.toggle('open');
      const icon = mobileToggle.querySelector('i');
      if (icon) {
        if (navMenu.classList.contains('open')) {
          icon.classList.remove('fa-bars');
          icon.classList.add('fa-times');
        } else {
          icon.classList.remove('fa-times');
          icon.classList.add('fa-bars');
        }
      }
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!navMenu.contains(e.target) && !mobileToggle.contains(e.target)) {
        navMenu.classList.remove('open');
        const icon = mobileToggle.querySelector('i');
        if (icon) {
          icon.classList.remove('fa-times');
          icon.classList.add('fa-bars');
        }
      }
    });
  }

  // Auto-dismiss alert messages after 6 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach((alert) => {
    const closeBtn = alert.querySelector('.alert-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
      });
    }

    setTimeout(() => {
      if (alert && alert.parentElement) {
        alert.style.transition = 'opacity 0.5s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
      }
    }, 7000);
  });
});
