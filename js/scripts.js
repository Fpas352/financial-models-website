// ============================================================
// Banking Models Store — Client-Side JavaScript
// ============================================================
//
// FILE: js/scripts.js
//
// FEATURES:
//  1.  Sticky header with scroll shadow
//  2.  Mobile hamburger menu with body-scroll lock
//  3.  Smooth scrolling for all anchor links
//  4.  FAQ accordion (one open at a time)
//  5.  Tab switching (generic, for future use)
//  6.  Catalogue filter with animation
//  7.  Contact form — validation + success message
//  8.  Custom model form — validation + success message
//  9.  Pricing toggle (wired for future use)
// 10.  Active nav link highlighting
// 11.  Scroll-triggered fade-in animations
//
// DEPENDENCIES: None (vanilla JS, no libraries)
// ============================================================


document.addEventListener('DOMContentLoaded', () => {


  // ----------------------------------------------------------
  // 1. STICKY HEADER
  // Adds .scrolled class when page scrolls past 40px.
  // CSS uses this for shadow + opaque background.
  // ----------------------------------------------------------

  const header = document.querySelector('.site-header');

  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // Run once on load in case page is already scrolled
  }


  // ----------------------------------------------------------
  // 2. MOBILE HAMBURGER MENU
  // Toggles .open on nav-links, sets aria-expanded,
  // and locks body scroll when menu is open.
  // Closes when a link is tapped or area outside is clicked.
  // ----------------------------------------------------------

  const hamburger = document.querySelector('.hamburger');
  const navLinks  = document.querySelector('.nav-links');

  if (hamburger && navLinks) {
    // Toggle menu open/close
    hamburger.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close menu when any nav link is clicked
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });

    // Close menu when clicking outside of it
    document.addEventListener('click', (e) => {
      if (navLinks.classList.contains('open') &&
          !navLinks.contains(e.target) &&
          !hamburger.contains(e.target)) {
        navLinks.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
  }


  // ----------------------------------------------------------
  // 3. SMOOTH SCROLLING FOR ANCHOR LINKS
  // Intercepts clicks on any link starting with # and smoothly
  // scrolls to the target. Accounts for fixed header height.
  // Also handles cross-page anchors (e.g. pricing.html#faq)
  // by letting the browser navigate normally.
  // ----------------------------------------------------------

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const href   = anchor.getAttribute('href');
      const target = document.querySelector(href);

      if (target) {
        e.preventDefault();

        // Calculate offset to account for sticky header
        const headerHeight = header ? header.offsetHeight : 0;
        const targetTop    = target.getBoundingClientRect().top + window.scrollY - headerHeight - 16;

        window.scrollTo({
          top:      targetTop,
          behavior: 'smooth'
        });

        // Update URL hash without jumping
        history.pushState(null, '', href);
      }
    });
  });

  // Handle hash in URL on page load (e.g. arriving from pricing.html#faq)
  if (window.location.hash) {
    const target = document.querySelector(window.location.hash);
    if (target) {
      // Small delay to let the page render first
      setTimeout(() => {
        const headerHeight = header ? header.offsetHeight : 0;
        const targetTop    = target.getBoundingClientRect().top + window.scrollY - headerHeight - 16;
        window.scrollTo({ top: targetTop, behavior: 'smooth' });
      }, 100);
    }
  }


  // ----------------------------------------------------------
  // 4. FAQ ACCORDION
  // Only one item open at a time. Clicking an open item
  // closes it. The .open class drives a CSS max-height
  // animation on .faq-answer.
  // ----------------------------------------------------------

  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item   = btn.closest('.faq-item');
      const isOpen = item.classList.contains('open');

      // Close all items first
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));

      // Toggle the clicked item (open if it was closed)
      if (!isOpen) item.classList.add('open');
    });
  });


  // ----------------------------------------------------------
  // 5. TAB SWITCHING
  // Generic tab component. Each .tab-btn has a data-tab
  // attribute matching a .tab-panel ID. Clicking deactivates
  // all siblings and activates the matching panel.
  // ----------------------------------------------------------

  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabGroup = btn.closest('.tabs-container');
      if (!tabGroup) return;

      tabGroup.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      tabGroup.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const panel = tabGroup.querySelector(`#${btn.dataset.tab}`);
      if (panel) panel.classList.add('active');
    });
  });


  // ----------------------------------------------------------
  // 6. CATALOGUE FILTER WITH ANIMATION
  // Filters .catalogue__card elements by data-category.
  // "all" shows every card. Other filters match against
  // space-separated values in each card's data-category.
  // Adds a fade transition when cards appear/disappear.
  // ----------------------------------------------------------

  const filterBtns     = document.querySelectorAll('.catalogue__filter');
  const catalogueCards = document.querySelectorAll('.catalogue__card');

  if (filterBtns.length && catalogueCards.length) {

    // Track the active filter for keyboard accessibility
    let activeFilter = 'all';

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;

        // Skip if already active
        if (filter === activeFilter) return;
        activeFilter = filter;

        // Update active button styling
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Filter cards with a fade effect
        catalogueCards.forEach(card => {
          const categories = card.dataset.category || '';
          const shouldShow = filter === 'all' || categories.includes(filter);

          if (shouldShow) {
            card.classList.remove('hidden');
            card.style.opacity = '0';
            card.style.transform = 'translateY(12px)';

            // Trigger reflow, then animate in
            requestAnimationFrame(() => {
              card.style.transition = 'opacity .3s ease, transform .3s ease';
              card.style.opacity = '1';
              card.style.transform = 'translateY(0)';
            });
          } else {
            card.style.opacity = '0';
            card.style.transform = 'translateY(12px)';
            card.style.transition = 'opacity .2s ease, transform .2s ease';

            // Hide after the fade-out completes
            setTimeout(() => card.classList.add('hidden'), 200);
          }
        });

        // Update the visible count (optional UI feedback)
        updateFilterCount(filter);
      });
    });
  }

  /**
   * Updates a filter count indicator if one exists.
   * Looks for an element with class .catalogue__count.
   * @param {string} filter - The active filter value
   */
  function updateFilterCount(filter) {
    const countEl = document.querySelector('.catalogue__count');
    if (!countEl) return;

    const visible = document.querySelectorAll('.catalogue__card:not(.hidden)').length;
    const total   = document.querySelectorAll('.catalogue__card').length;
    countEl.textContent = filter === 'all'
      ? `Showing all ${total} models`
      : `Showing ${visible} of ${total} models`;
  }


  // ----------------------------------------------------------
  // 7. CONTACT FORM — VALIDATION + SUCCESS MESSAGE
  //
  // Validates required fields with inline error messages,
  // shows a loading state on submit, then displays a
  // success message. In production, replace the setTimeout
  // with a fetch() call to /api/contact.
  // ----------------------------------------------------------

  const contactForm = document.getElementById('contactForm');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      // Clear previous errors
      clearFormErrors(contactForm);

      // Collect form data
      const formData = new FormData(contactForm);
      const data     = Object.fromEntries(formData.entries());

      // --- Validate required fields ---
      let isValid = true;

      if (!data.name || !data.name.trim()) {
        showFieldError('name', 'Please enter your full name.');
        isValid = false;
      }

      if (!data.email || !data.email.trim()) {
        showFieldError('email', 'Please enter your email address.');
        isValid = false;
      } else if (!isValidEmail(data.email)) {
        showFieldError('email', 'Please enter a valid email address.');
        isValid = false;
      }

      if (!data.message || !data.message.trim()) {
        showFieldError('message', 'Please enter a message.');
        isValid = false;
      }

      if (!isValid) {
        // Focus the first invalid field
        const firstError = contactForm.querySelector('.field-error');
        if (firstError) {
          const fieldId = firstError.dataset.for;
          const field   = document.getElementById(fieldId);
          if (field) field.focus();
        }
        return;
      }

      // --- Submit ---
      const btn          = contactForm.querySelector('button[type="submit"]');
      const originalHTML = btn.innerHTML;
      btn.innerHTML      = '<span class="spinner"></span> Sending...';
      btn.disabled       = true;

      // Simulated submission — replace with:
      //   fetch('/api/contact', {
      //     method: 'POST',
      //     headers: { 'Content-Type': 'application/json' },
      //     body: JSON.stringify(data),
      //   })
      //   .then(res => res.json())
      //   .then(result => { ... })
      //   .catch(err => { ... })

      setTimeout(() => {
        showFormSuccess(contactForm, 'Message sent! We\'ll get back to you within 24 hours.');
        contactForm.reset();
        btn.innerHTML = originalHTML;
        btn.disabled  = false;
      }, 1200);
    });

    // Live validation: clear error when user starts typing
    contactForm.querySelectorAll('input, textarea, select').forEach(field => {
      field.addEventListener('input', () => {
        clearFieldError(field.id);
      });
    });
  }


  // ----------------------------------------------------------
  // 8. CUSTOM MODEL FORM — VALIDATION + SUCCESS MESSAGE
  //
  // Same pattern as contact form. Validates business name,
  // sector, and description. Shows file name when selected.
  // ----------------------------------------------------------

  const customForm = document.getElementById('customModelForm');

  if (customForm) {
    customForm.addEventListener('submit', (e) => {
      e.preventDefault();

      // Clear previous errors
      clearFormErrors(customForm);

      // Collect form data
      const formData = new FormData(customForm);
      const data     = Object.fromEntries(formData.entries());

      // --- Validate required fields ---
      let isValid = true;

      if (!data.business || !data.business.trim()) {
        showFieldError('custom-business', 'Please enter your business name.');
        isValid = false;
      }

      if (!data.sector) {
        showFieldError('custom-sector', 'Please select your sector.');
        isValid = false;
      }

      if (!data.description || !data.description.trim()) {
        showFieldError('custom-description', 'Please describe what you need.');
        isValid = false;
      }

      if (!isValid) {
        const firstError = customForm.querySelector('.field-error');
        if (firstError) {
          const fieldId = firstError.dataset.for;
          const field   = document.getElementById(fieldId);
          if (field) field.focus();
        }
        return;
      }

      // --- Submit ---
      const btn          = customForm.querySelector('button[type="submit"]');
      const originalHTML = btn.innerHTML;
      btn.innerHTML      = '<span class="spinner"></span> Sending...';
      btn.disabled       = true;

      // Simulated submission
      setTimeout(() => {
        showFormSuccess(customForm, 'Request received! We\'ll send you a scope and quote within 24 hours.');
        customForm.reset();
        btn.innerHTML = originalHTML;
        btn.disabled  = false;

        // Reset file input label
        const textEl = customForm.querySelector('.custom-request__file-text');
        if (textEl) textEl.textContent = 'Attach a brief or reference file (optional)';
      }, 1200);
    });

    // Live validation: clear error on input
    customForm.querySelectorAll('input, textarea, select').forEach(field => {
      field.addEventListener('input', () => {
        clearFieldError(field.id);
      });
    });

    // Show filename when a file is selected
    const fileInput = customForm.querySelector('input[type="file"]');
    if (fileInput) {
      fileInput.addEventListener('change', () => {
        const textEl = customForm.querySelector('.custom-request__file-text');
        if (!textEl) return;
        textEl.textContent = fileInput.files.length
          ? fileInput.files[0].name
          : 'Attach a brief or reference file (optional)';
      });
    }
  }


  // ----------------------------------------------------------
  // 9. PRICING TOGGLE (Monthly / Annual)
  // Not currently in the UI but wired for future use.
  // Expects a checkbox #billingToggle and elements with
  // data-monthly / data-annual attributes.
  // ----------------------------------------------------------

  const billingToggle = document.getElementById('billingToggle');

  if (billingToggle) {
    billingToggle.addEventListener('change', () => {
      const isAnnual = billingToggle.checked;

      document.querySelectorAll('[data-monthly]').forEach(el => {
        el.textContent = isAnnual ? el.dataset.annual : el.dataset.monthly;
      });

      document.querySelectorAll('.billing-label').forEach(el => {
        el.classList.toggle('active', el.dataset.billing === (isAnnual ? 'annual' : 'monthly'));
      });
    });
  }


  // ----------------------------------------------------------
  // 10. ACTIVE NAV LINK HIGHLIGHTING
  // Compares the current page filename to each nav link's
  // href and adds the .active class to the matching link.
  // ----------------------------------------------------------

  const currentPage = window.location.pathname.split('/').pop() || 'index.html';

  document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href').split('#')[0]; // Strip hash
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });


  // ----------------------------------------------------------
  // 11. SCROLL-TRIGGERED FADE-IN ANIMATIONS
  // Elements with .fade-in-on-scroll get animated when they
  // enter the viewport. Uses IntersectionObserver for
  // performance — no scroll event listeners.
  // Also auto-applies to key section elements.
  // ----------------------------------------------------------

  const observerOptions = {
    root:       null,
    rootMargin: '0px 0px -60px 0px', // Trigger slightly before fully visible
    threshold:  0.1
  };

  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        fadeObserver.unobserve(entry.target); // Only animate once
      }
    });
  }, observerOptions);

  // Select elements to animate on scroll
  const animateTargets = document.querySelectorAll(
    '.fade-in-on-scroll, .section-header, .model-card, .pricing-tier, ' +
    '.testimonial, .audience-card, .feature-card, .step, ' +
    '.benefits__feature-item, .contact-trust-card, .contact-faq-card, ' +
    '.consultation__card'
  );

  animateTargets.forEach(el => {
    el.classList.add('fade-in-on-scroll');
    fadeObserver.observe(el);
  });


}); // end DOMContentLoaded


// ============================================================
// HELPER FUNCTIONS
// ============================================================


/**
 * Validates an email address format.
 * Catches common errors like missing @, missing domain, etc.
 * @param {string} email
 * @returns {boolean}
 */
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.trim());
}


/**
 * Shows an inline error message below a form field.
 * Creates a .field-error element and adds .has-error to the field.
 * @param {string} fieldId - The id of the input/select/textarea
 * @param {string} message - The error message to display
 */
function showFieldError(fieldId, message) {
  const field = document.getElementById(fieldId);
  if (!field) return;

  // Add error styling to the field
  field.classList.add('has-error');

  // Create error message element (if not already present)
  const existingError = field.parentElement.querySelector(`.field-error[data-for="${fieldId}"]`);
  if (existingError) {
    existingError.textContent = message;
    return;
  }

  const errorEl = document.createElement('span');
  errorEl.className   = 'field-error';
  errorEl.dataset.for = fieldId;
  errorEl.textContent = message;

  // Insert after the field
  field.parentElement.insertBefore(errorEl, field.nextSibling);
}


/**
 * Clears the error message and styling for a single field.
 * @param {string} fieldId - The id of the field to clear
 */
function clearFieldError(fieldId) {
  const field = document.getElementById(fieldId);
  if (!field) return;

  field.classList.remove('has-error');

  const errorEl = field.parentElement.querySelector(`.field-error[data-for="${fieldId}"]`);
  if (errorEl) errorEl.remove();
}


/**
 * Clears all error messages and styling within a form.
 * @param {HTMLFormElement} form
 */
function clearFormErrors(form) {
  form.querySelectorAll('.has-error').forEach(el => el.classList.remove('has-error'));
  form.querySelectorAll('.field-error').forEach(el => el.remove());

  // Also remove any existing success message
  const success = form.parentElement.querySelector('.form-success');
  if (success) success.remove();
}


/**
 * Shows a success message above the form after submission.
 * Auto-dismisses after 6 seconds with a fade-out.
 * @param {HTMLFormElement} form
 * @param {string} message
 */
function showFormSuccess(form, message) {
  // Remove any existing success message
  const existing = form.parentElement.querySelector('.form-success');
  if (existing) existing.remove();

  // Create success banner
  const el = document.createElement('div');
  el.className = 'form-success';
  el.innerHTML = `
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
      <circle cx="10" cy="10" r="10" fill="#22c55e"/>
      <path d="M6 10.5l2.5 2.5 5.5-5.5" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <span>${message}</span>
  `;

  // Insert before the form
  form.parentElement.insertBefore(el, form);

  // Scroll the success message into view
  el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  // Auto-dismiss after 6 seconds
  setTimeout(() => {
    el.style.opacity    = '0';
    el.style.transform  = 'translateY(-8px)';
    el.style.transition = 'opacity .4s ease, transform .4s ease';
    setTimeout(() => el.remove(), 400);
  }, 6000);
}


/**
 * Shows a floating notification toast in the top-right corner.
 * Auto-dismisses after 4 seconds. Only one visible at a time.
 * @param {string} message
 * @param {string} type - 'success' or 'error'
 */
function showNotification(message, type) {
  const existing = document.querySelector('.notification');
  if (existing) existing.remove();

  const el = document.createElement('div');
  el.className = `notification notification-${type}`;
  el.textContent = message;

  Object.assign(el.style, {
    position:     'fixed',
    top:          '80px',
    right:        '24px',
    padding:      '14px 24px',
    borderRadius: '10px',
    fontSize:     '.9rem',
    fontWeight:   '600',
    zIndex:       '9999',
    animation:    'slideIn .3s ease',
    background:   type === 'success' ? '#22c55e' : '#ef4444',
    color:        '#fff',
    boxShadow:    '0 4px 20px rgba(0,0,0,.15)',
    maxWidth:     '400px',
  });

  document.body.appendChild(el);

  setTimeout(() => {
    el.style.opacity    = '0';
    el.style.transition = 'opacity .3s ease';
    setTimeout(() => el.remove(), 300);
  }, 4000);
}


// ============================================================
// INJECTED STYLES
// Minimal CSS injected via JS for components that are
// created dynamically (errors, success messages, animations).
// Keeps the main CSS file focused on layout and theme.
// ============================================================

const injectedStyles = document.createElement('style');
injectedStyles.textContent = `

  /* Notification slide-in animation */
  @keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to   { transform: translateX(0);    opacity: 1; }
  }

  /* Form field error state */
  .has-error {
    border-color: #ef4444 !important;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, .15) !important;
  }

  /* Inline error message below fields */
  .field-error {
    display: block;
    color: #ef4444;
    font-size: .8rem;
    font-weight: 500;
    margin-top: 4px;
    animation: fadeInError .2s ease;
  }

  @keyframes fadeInError {
    from { opacity: 0; transform: translateY(-4px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  /* Success message banner above form */
  .form-success {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 1px solid #bbf7d0;
    border-radius: 10px;
    color: #166534;
    font-size: .95rem;
    font-weight: 600;
    margin-bottom: 20px;
    animation: fadeInSuccess .4s ease;
  }

  .form-success svg {
    flex-shrink: 0;
  }

  @keyframes fadeInSuccess {
    from { opacity: 0; transform: translateY(-8px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  /* Loading spinner for submit buttons */
  .spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255,255,255,.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin .6s linear infinite;
    vertical-align: middle;
    margin-right: 6px;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  /* Scroll-triggered fade-in animation */
  .fade-in-on-scroll {
    opacity: 0;
    transform: translateY(24px);
    transition: opacity .6s ease, transform .6s ease;
  }

  .fade-in-on-scroll.is-visible {
    opacity: 1;
    transform: translateY(0);
  }

  /* Staggered delays for grid children */
  .fade-in-on-scroll:nth-child(2) { transition-delay: .08s; }
  .fade-in-on-scroll:nth-child(3) { transition-delay: .16s; }
  .fade-in-on-scroll:nth-child(4) { transition-delay: .24s; }
  .fade-in-on-scroll:nth-child(5) { transition-delay: .32s; }
  .fade-in-on-scroll:nth-child(6) { transition-delay: .40s; }
`;

document.head.appendChild(injectedStyles);
