/* Anime News Hub - Main JavaScript */

// ===== Alpine.js Component Initialization =====
document.addEventListener('alpine:init', () => {

  // Search Component
  Alpine.data('searchComponent', () => ({
    open: false,
    query: '',
    loading: false,

    toggle() {
      this.open = !this.open;
      if (this.open) {
        this.$nextTick(() => {
          const input = this.$refs.searchInput;
          if (input) input.focus();
        });
      }
    },

    close() {
      this.open = false;
      this.query = '';
    },

    handleEscape(e) {
      if (e.key === 'Escape') {
        this.close();
      }
    }
  }));

  // Category Filter Component
  Alpine.data('categoryFilter', (initialCategory = 'all') => ({
    activeCategory: initialCategory,

    setCategory(category) {
      this.activeCategory = category;
    },

    isActive(category) {
      return this.activeCategory === category;
    }
  }));

  // Mobile Menu Component
  Alpine.data('mobileMenu', () => ({
    open: false,

    toggle() {
      this.open = !this.open;
      // Prevent body scroll when menu is open
      document.body.style.overflow = this.open ? 'hidden' : '';
    },

    close() {
      this.open = false;
      document.body.style.overflow = '';
    }
  }));

  // Image Lazy Load Component
  Alpine.data('lazyImage', () => ({
    loaded: false,
    error: false,

    onLoad() {
      this.loaded = true;
    },

    onError() {
      this.error = true;
      this.loaded = true;
    }
  }));

  // Scroll to Top Component
  Alpine.data('scrollToTop', () => ({
    visible: false,

    init() {
      window.addEventListener('scroll', () => {
        this.visible = window.scrollY > 500;
      });
    },

    scrollTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  }));
});

// ===== HTMX Event Handlers =====

// Add loading state before HTMX request
document.body.addEventListener('htmx:beforeRequest', (event) => {
  const target = event.detail.target;
  if (target) {
    target.classList.add('htmx-loading');
  }
});

// Remove loading state after HTMX request completes
document.body.addEventListener('htmx:afterRequest', (event) => {
  const target = event.detail.target;
  if (target) {
    target.classList.remove('htmx-loading');
  }
});

// Handle HTMX errors gracefully
document.body.addEventListener('htmx:responseError', (event) => {
  console.error('HTMX Error:', event.detail.error);
  // Could show a toast notification here
});

// Reinitialize animations after HTMX swaps content
document.body.addEventListener('htmx:afterSwap', (event) => {
  // Add stagger animation to new content
  const newCards = event.detail.target.querySelectorAll('.card');
  newCards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.05}s`;
    card.classList.add('animate-fade-in-up');
  });
});

// ===== View Transitions API Support =====
if (document.startViewTransition) {
  document.body.addEventListener('htmx:beforeSwap', (event) => {
    // Use View Transitions API if available
    if (event.detail.shouldSwap) {
      event.detail.isSwapped = true;
      document.startViewTransition(() => {
        event.detail.target.innerHTML = event.detail.serverResponse;
      });
    }
  });
}

// ===== Keyboard Navigation =====
document.addEventListener('keydown', (e) => {
  // Focus search on "/" key
  if (e.key === '/' && !isInputFocused()) {
    e.preventDefault();
    const searchInput = document.querySelector('.navbar__search-input');
    if (searchInput) {
      searchInput.focus();
    }
  }

  // Close search on Escape
  if (e.key === 'Escape') {
    const searchInput = document.querySelector('.navbar__search-input');
    if (searchInput && document.activeElement === searchInput) {
      searchInput.blur();
    }
  }
});

function isInputFocused() {
  const activeElement = document.activeElement;
  return activeElement.tagName === 'INPUT' ||
         activeElement.tagName === 'TEXTAREA' ||
         activeElement.isContentEditable;
}

// ===== Intersection Observer for Animations =====
const observeAnimations = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fade-in-up');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  document.querySelectorAll('.card').forEach(card => {
    observer.observe(card);
  });
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  observeAnimations();
});

// Reinitialize after HTMX content swap
document.body.addEventListener('htmx:afterSettle', () => {
  observeAnimations();
});

// ===== Console Branding =====
console.log(
  '%c Anime News Hub ',
  'background: linear-gradient(135deg, #ff6b9d 0%, #9d4edd 100%); color: white; padding: 10px 20px; font-size: 16px; font-weight: bold; border-radius: 4px;'
);
