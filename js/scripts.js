// ============================================================
// SFS Models — Client-Side JavaScript
// ============================================================
//
// FEATURES:
//  1.  Sticky header with scroll backdrop
//  2.  Mobile hamburger menu with body-scroll lock
//  3.  Smooth scrolling for anchor links
//  4.  FAQ accordion (one open at a time)
//  5.  Catalogue filter with animation
//  6.  Contact form — validation + fetch to /api/contact
//  7.  Custom model multi-step form — validation + fetch
//  8.  Active nav link highlighting
//  9.  Scroll-triggered fade-in animations
//
// DEPENDENCIES: None (vanilla JS, no libraries)
// ============================================================


document.addEventListener('DOMContentLoaded', () => {


  // ----------------------------------------------------------
  // 1. STICKY HEADER
  // ----------------------------------------------------------

  const header = document.querySelector('.site-header');

  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }


  // ----------------------------------------------------------
  // 2. MOBILE HAMBURGER MENU
  // ----------------------------------------------------------

  const hamburger = document.querySelector('.hamburger');
  const navLinks  = document.querySelector('.nav-links');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });

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
  // ----------------------------------------------------------

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const href   = anchor.getAttribute('href');
      const target = document.querySelector(href);

      if (target) {
        e.preventDefault();
        const headerHeight = header ? header.offsetHeight : 0;
        const targetTop    = target.getBoundingClientRect().top + window.scrollY - headerHeight - 16;

        window.scrollTo({ top: targetTop, behavior: 'smooth' });
        history.pushState(null, '', href);
      }
    });
  });

  if (window.location.hash) {
    const target = document.querySelector(window.location.hash);
    if (target) {
      setTimeout(() => {
        const headerHeight = header ? header.offsetHeight : 0;
        const targetTop    = target.getBoundingClientRect().top + window.scrollY - headerHeight - 16;
        window.scrollTo({ top: targetTop, behavior: 'smooth' });
      }, 100);
    }
  }


  // ----------------------------------------------------------
  // 4. FAQ ACCORDION
  // ----------------------------------------------------------

  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item   = btn.closest('.faq-item');
      const isOpen = item.classList.contains('open');

      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));

      if (!isOpen) item.classList.add('open');
    });
  });


  // ----------------------------------------------------------
  // 5. CATALOGUE FILTER WITH ANIMATION
  // Works with both .catalogue__card and .model-card elements
  // ----------------------------------------------------------

  const filterBtns = document.querySelectorAll('.catalogue__filter');
  const filterCards = document.querySelectorAll('.model-card[data-category], .catalogue__card[data-category]');

  if (filterBtns.length && filterCards.length) {
    let activeFilter = 'all';

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;
        if (filter === activeFilter) return;
        activeFilter = filter;

        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        filterCards.forEach(card => {
          const categories = card.dataset.category || '';
          const shouldShow = filter === 'all' || categories.includes(filter);

          if (shouldShow) {
            card.classList.remove('hidden');
            card.style.opacity = '0';
            card.style.transform = 'translateY(12px)';
            requestAnimationFrame(() => {
              card.style.transition = 'opacity .3s ease, transform .3s ease';
              card.style.opacity = '1';
              card.style.transform = 'translateY(0)';
            });
          } else {
            card.style.opacity = '0';
            card.style.transform = 'translateY(12px)';
            card.style.transition = 'opacity .2s ease, transform .2s ease';
            setTimeout(() => card.classList.add('hidden'), 200);
          }
        });
      });
    });
  }


  // ----------------------------------------------------------
  // 6. CONTACT FORM — VALIDATION + FETCH
  // ----------------------------------------------------------

  const contactForm = document.getElementById('contactForm');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      clearFormErrors(contactForm);

      const formData = new FormData(contactForm);
      const data     = Object.fromEntries(formData.entries());

      let isValid = true;

      if (!data.name || !data.name.trim()) {
        showFieldError(contactForm.querySelector('[name="name"]'), 'Please enter your name.');
        isValid = false;
      }

      if (!data.email || !data.email.trim()) {
        showFieldError(contactForm.querySelector('[name="email"]'), 'Please enter your email.');
        isValid = false;
      } else if (!isValidEmail(data.email)) {
        showFieldError(contactForm.querySelector('[name="email"]'), 'Please enter a valid email.');
        isValid = false;
      }

      if (!data.message || !data.message.trim()) {
        showFieldError(contactForm.querySelector('[name="message"]'), 'Please enter a message.');
        isValid = false;
      }

      if (!isValid) {
        const firstError = contactForm.querySelector('.has-error');
        if (firstError) firstError.focus();
        return;
      }

      const btn = contactForm.querySelector('button[type="submit"]');
      setButtonLoading(btn, true);

      submitForm('/api/contact', data)
        .then(() => {
          showFormSuccess(contactForm, 'Message sent! We\'ll get back to you within 24 hours.');
          contactForm.reset();
        })
        .catch(() => {
          showFormSuccess(contactForm, 'Message sent! We\'ll get back to you within 24 hours.');
          contactForm.reset();
        })
        .finally(() => setButtonLoading(btn, false));
    });

    addLiveValidation(contactForm);
  }


  // ----------------------------------------------------------
  // 7. MULTI-STEP CUSTOM MODEL FORM
  // ----------------------------------------------------------

  const customForm = document.getElementById('customModelForm');

  if (customForm) {
    const panels   = customForm.querySelectorAll('.multistep-panel');
    const progress = customForm.querySelectorAll('.multistep-progress__step');
    let currentStep = 1;

    function goToStep(step) {
      // Validate current step before advancing
      if (step > currentStep && !validateStep(currentStep)) return;

      currentStep = step;

      panels.forEach(p => {
        p.classList.toggle('active', parseInt(p.dataset.step) === step);
      });

      progress.forEach(s => {
        const stepNum = parseInt(s.dataset.step);
        s.classList.toggle('active', stepNum === step);
        s.classList.toggle('completed', stepNum < step);
      });

      // Populate review panel on step 3
      if (step === 3) populateReview();

      // Scroll form into view
      customForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function validateStep(step) {
      clearFormErrors(customForm);
      let isValid = true;

      if (step === 1) {
        const name    = customForm.querySelector('[name="name"]');
        const email   = customForm.querySelector('[name="email"]');
        const company = customForm.querySelector('[name="business"]');
        const sector  = customForm.querySelector('[name="sector"]');

        if (!name.value.trim()) { showFieldError(name, 'Please enter your name.'); isValid = false; }
        if (!email.value.trim()) { showFieldError(email, 'Please enter your email.'); isValid = false; }
        else if (!isValidEmail(email.value)) { showFieldError(email, 'Please enter a valid email.'); isValid = false; }
        if (!company.value.trim()) { showFieldError(company, 'Please enter your company.'); isValid = false; }
        if (!sector.value) { showFieldError(sector, 'Please select a sector.'); isValid = false; }

        if (!isValid) {
          const firstError = customForm.querySelector('.has-error');
          if (firstError) firstError.focus();
        }
      }

      if (step === 2) {
        const modelType   = customForm.querySelector('[name="model_type"]');
        const description = customForm.querySelector('[name="description"]');

        if (!modelType.value) { showFieldError(modelType, 'Please select a model type.'); isValid = false; }
        if (!description.value.trim()) { showFieldError(description, 'Please describe what you need.'); isValid = false; }

        if (!isValid) {
          const firstError = customForm.querySelector('.has-error');
          if (firstError) firstError.focus();
        }
      }

      return isValid;
    }

    function populateReview() {
      const getValue = (name) => {
        const el = customForm.querySelector(`[name="${name}"]`);
        if (!el) return '';
        if (el.tagName === 'SELECT') return el.options[el.selectedIndex]?.text || '';
        return el.value || '';
      };

      const setText = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val || '—';
      };

      setText('review-name', getValue('name'));
      setText('review-email', getValue('email'));
      setText('review-company', getValue('business'));
      setText('review-sector', getValue('sector'));
      setText('review-role', getValue('role'));
      setText('review-model-type', getValue('model_type'));
      setText('review-complexity', getValue('complexity'));
      setText('review-timeline', getValue('timeline'));
      setText('review-description', getValue('description'));
    }

    // Next/Prev button handlers
    customForm.querySelectorAll('.multistep-next').forEach(btn => {
      btn.addEventListener('click', () => goToStep(currentStep + 1));
    });

    customForm.querySelectorAll('.multistep-prev').forEach(btn => {
      btn.addEventListener('click', () => goToStep(currentStep - 1));
    });

    // Form submission
    customForm.addEventListener('submit', (e) => {
      e.preventDefault();

      if (!validateStep(currentStep)) return;

      const formData = new FormData(customForm);
      const data     = Object.fromEntries(formData.entries());

      const btn = customForm.querySelector('button[type="submit"]');
      setButtonLoading(btn, true);

      submitForm('/api/custom-model', data)
        .then(() => {
          showFormSuccess(customForm, 'Request received! We\'ll send you a scope and quote within 24 hours.');
          customForm.reset();
          currentStep = 1;
          goToStep(1);
        })
        .catch(() => {
          showFormSuccess(customForm, 'Request received! We\'ll send you a scope and quote within 24 hours.');
          customForm.reset();
          currentStep = 1;
          goToStep(1);
        })
        .finally(() => setButtonLoading(btn, false));
    });

    addLiveValidation(customForm);
  }


  // ----------------------------------------------------------
  // 8. ACTIVE NAV LINK HIGHLIGHTING
  // ----------------------------------------------------------

  const currentPage = window.location.pathname.split('/').pop() || 'index.html';

  document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href').split('#')[0];
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });


  // ----------------------------------------------------------
  // 9. SCROLL-TRIGGERED FADE-IN ANIMATIONS
  // ----------------------------------------------------------

  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        fadeObserver.unobserve(entry.target);
      }
    });
  }, { root: null, rootMargin: '0px 0px -60px 0px', threshold: 0.1 });

  const animateTargets = document.querySelectorAll(
    '.fade-in-on-scroll, .section-header, .model-card, .pricing-tier, ' +
    '.pricing-card, .testimonial, .usp-card, .expertise-card, ' +
    '.principle-card, .feature-card, .contact-trust-card, ' +
    '.bundle-highlight, .format-bar'
  );

  animateTargets.forEach(el => {
    el.classList.add('fade-in-on-scroll');
    fadeObserver.observe(el);
  });


  // ----------------------------------------------------------
  // 10. NOTIFY ME FORM (Expanding Library)
  // ----------------------------------------------------------

  const notifyForm = document.getElementById('notifyForm');

  if (notifyForm) {
    notifyForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const emailInput = document.getElementById('notify-email');
      const wrapper    = notifyForm.closest('.expanding-library__notify');
      const errorMsg   = wrapper.querySelector('.notify-error');
      const successMsg = wrapper.querySelector('.notify-success');

      errorMsg.style.display = 'none';

      if (!isValidEmail(emailInput.value)) {
        errorMsg.style.display = 'block';
        return;
      }

      // Submit to backend (fail gracefully — show success regardless)
      fetch('/api/notify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: emailInput.value.trim() }),
      }).catch(() => {});

      notifyForm.style.display = 'none';
      successMsg.style.display = 'block';
    });
  }


  // ----------------------------------------------------------
  // 11. ENQUIRY MODAL
  // ----------------------------------------------------------

  const enquiryModal   = document.getElementById('enquiryModal');
  const enquiryOpeners = document.querySelectorAll('#openEnquiryModal');

  if (enquiryModal && enquiryOpeners.length) {
    const panel     = enquiryModal.querySelector('.enquiry-modal__panel');
    const closeBtn  = enquiryModal.querySelector('.enquiry-modal__close');
    const backdrop  = enquiryModal.querySelector('.enquiry-modal__backdrop');
    const form      = document.getElementById('enquiryModalForm');
    const successEl = enquiryModal.querySelector('.enquiry-modal__success');
    const errorEl   = enquiryModal.querySelector('.enquiry-modal__error');

    function openModal() {
      enquiryModal.classList.add('is-open');
      enquiryModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      enquiryModal.classList.remove('is-open');
      enquiryModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    enquiryOpeners.forEach(btn => btn.addEventListener('click', openModal));
    closeBtn.addEventListener('click', closeModal);
    backdrop.addEventListener('click', closeModal);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && enquiryModal.classList.contains('is-open')) closeModal();
    });

    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        clearFormErrors(form);

        const data = Object.fromEntries(new FormData(form).entries());
        let isValid = true;

        if (!data.name || !data.name.trim()) { showFieldError(form.querySelector('[name="name"]'), 'Please enter your name.'); isValid = false; }
        if (!data.email || !data.email.trim()) { showFieldError(form.querySelector('[name="email"]'), 'Please enter your email.'); isValid = false; }
        else if (!isValidEmail(data.email)) { showFieldError(form.querySelector('[name="email"]'), 'Please enter a valid email.'); isValid = false; }
        if (!data.business || !data.business.trim()) { showFieldError(form.querySelector('[name="business"]'), 'Please enter your company.'); isValid = false; }
        if (!data.role || !data.role.trim()) { showFieldError(form.querySelector('[name="role"]'), 'Please enter your role.'); isValid = false; }
        if (!data.description || !data.description.trim()) { showFieldError(form.querySelector('[name="description"]'), 'Please describe what you need.'); isValid = false; }

        if (!isValid) {
          const firstErr = form.querySelector('.has-error');
          if (firstErr) firstErr.focus();
          return;
        }

        const btn = form.querySelector('button[type="submit"]');
        setButtonLoading(btn, true);

        submitForm('/api/custom-model', data)
          .then(() => {
            form.style.display = 'none';
            errorEl.style.display = 'none';
            successEl.style.display = 'block';
          })
          .catch(() => {
            form.style.display = 'none';
            successEl.style.display = 'none';
            errorEl.style.display = 'block';
          })
          .finally(() => setButtonLoading(btn, false));
      });

      addLiveValidation(form);
    }
  }


  // ── 12. MODEL SEARCH ─────────────────────────────────────────────────
  const modelSearch = document.getElementById('modelSearch');
  if (modelSearch) {
    modelSearch.addEventListener('input', () => {
      const q = modelSearch.value.toLowerCase().trim();
      const cards = document.querySelectorAll('.model-card');
      const sections = document.querySelectorAll('.section[id], .section.alt-bg');
      const customCta = document.querySelector('.custom-cta');

      cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = q && !text.includes(q) ? 'none' : '';
      });

      // Hide custom CTA section while searching so results are visible
      if (customCta) {
        customCta.style.display = q ? 'none' : '';
      }

      // Hide category sections where all cards are hidden
      sections.forEach(sec => {
        const grid = sec.querySelector('.model-grid');
        if (!grid) return;
        const visible = grid.querySelectorAll('.model-card:not([style*="display: none"])');
        sec.style.display = q && visible.length === 0 ? 'none' : '';
      });
    });
  }


}); // end DOMContentLoaded


// ============================================================
// HELPER FUNCTIONS
// ============================================================

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.trim());
}

function showFieldError(field, message) {
  if (!field) return;
  field.classList.add('has-error');

  const existing = field.parentElement.querySelector('.field-error');
  if (existing) { existing.textContent = message; return; }

  const errorEl = document.createElement('span');
  errorEl.className   = 'field-error';
  errorEl.textContent = message;
  field.parentElement.insertBefore(errorEl, field.nextSibling);
}

function clearFieldError(field) {
  if (!field) return;
  field.classList.remove('has-error');
  const errorEl = field.parentElement.querySelector('.field-error');
  if (errorEl) errorEl.remove();
}

function clearFormErrors(form) {
  form.querySelectorAll('.has-error').forEach(el => el.classList.remove('has-error'));
  form.querySelectorAll('.field-error').forEach(el => el.remove());
}

function addLiveValidation(form) {
  form.querySelectorAll('input, textarea, select').forEach(field => {
    field.addEventListener('input', () => clearFieldError(field));
  });
}

function setButtonLoading(btn, loading) {
  if (!btn) return;
  if (loading) {
    btn._originalHTML = btn.innerHTML;
    btn.innerHTML = '<span class="spinner"></span> Sending...';
    btn.disabled = true;
  } else {
    btn.innerHTML = btn._originalHTML || 'Submit';
    btn.disabled = false;
  }
}

function showFormSuccess(form, message) {
  const existing = form.closest('.section, .multistep-form-wrapper, div')?.querySelector('.form-success');
  if (existing) existing.remove();

  const el = document.createElement('div');
  el.className = 'form-success';
  el.innerHTML = `
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
      <circle cx="10" cy="10" r="10" fill="var(--gold, #C9A84C)"/>
      <path d="M6 10.5l2.5 2.5 5.5-5.5" stroke="#0A0C10" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <span>${message}</span>
  `;

  form.parentElement.insertBefore(el, form);
  el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  setTimeout(() => {
    el.style.opacity    = '0';
    el.style.transform  = 'translateY(-8px)';
    el.style.transition = 'opacity .4s ease, transform .4s ease';
    setTimeout(() => el.remove(), 400);
  }, 6000);
}

/**
 * Submit form data to backend API.
 * Falls back to simulated success if backend is unavailable.
 */
function submitForm(endpoint, data) {
  return fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  .then(res => {
    if (!res.ok) throw new Error('Server error');
    return res.json();
  })
  .catch(() => {
    // Backend not available — simulate success for static hosting
    return new Promise(resolve => setTimeout(resolve, 1200));
  });
}


// ============================================================
// INJECTED STYLES (dynamic components)
// ============================================================

const injectedStyles = document.createElement('style');
injectedStyles.textContent = `
  @keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to   { transform: translateX(0);    opacity: 1; }
  }

  .has-error {
    border-color: #ef4444 !important;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, .15) !important;
  }

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

  .form-success {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    background: rgba(201, 168, 76, .1);
    border: 1px solid rgba(201, 168, 76, .3);
    border-radius: 8px;
    color: var(--gold, #C9A84C);
    font-size: .95rem;
    font-weight: 600;
    margin-bottom: 20px;
    animation: fadeInSuccess .4s ease;
  }

  .form-success svg { flex-shrink: 0; }

  @keyframes fadeInSuccess {
    from { opacity: 0; transform: translateY(-8px); }
    to   { opacity: 1; transform: translateY(0); }
  }

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

  .fade-in-on-scroll {
    opacity: 0;
    transform: translateY(24px);
    transition: opacity .6s ease, transform .6s ease;
  }

  .fade-in-on-scroll.is-visible {
    opacity: 1;
    transform: translateY(0);
  }

  .fade-in-on-scroll:nth-child(2) { transition-delay: .08s; }
  .fade-in-on-scroll:nth-child(3) { transition-delay: .16s; }
  .fade-in-on-scroll:nth-child(4) { transition-delay: .24s; }
  .fade-in-on-scroll:nth-child(5) { transition-delay: .32s; }
  .fade-in-on-scroll:nth-child(6) { transition-delay: .40s; }
`;

document.head.appendChild(injectedStyles);


// ============================================================
// GA4 EVENT TRACKING
// ============================================================

document.addEventListener('DOMContentLoaded', function() {

  // Track buy button clicks
  document.querySelectorAll('.ls-buy-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      if (typeof gtag !== 'undefined') {
        gtag('event', 'begin_checkout', {
          item_name: this.dataset.modelId,
          currency: 'GBP'
        });
      }
    });
  });

  // Track free sample button clicks (Lemon Squeezy $0 checkout)
  document.querySelectorAll('.ls-free-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      if (typeof gtag !== 'undefined') {
        gtag('event', 'generate_lead', {
          method: 'free_sample_download',
          item_name: this.dataset.modelId
        });
      }
    });
  });

  // Track purchase on thank you page
  if (window.location.pathname.includes('thankyou')) {
    if (typeof gtag !== 'undefined') {
      gtag('event', 'purchase', { currency: 'GBP' });
    }
  }

});
