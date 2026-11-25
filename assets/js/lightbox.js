// Click-to-enlarge lightbox for images inside post content.
(function () {
  var imgs = Array.prototype.filter.call(
    document.querySelectorAll('.entry-content img'),
    function (img) {
      return !img.classList.contains('in-text') && !img.closest('a');
    }
  );
  if (!imgs.length) return;

  var overlay = document.createElement('div');
  overlay.className = 'lightbox';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Enlarged image');
  overlay.hidden = true;

  var closeBtn = document.createElement('button');
  closeBtn.type = 'button';
  closeBtn.className = 'lightbox-close';
  closeBtn.setAttribute('aria-label', 'Close image');
  closeBtn.innerHTML = '&times;';

  var full = document.createElement('img');
  full.className = 'lightbox-img';
  full.alt = '';

  overlay.appendChild(closeBtn);
  overlay.appendChild(full);
  document.body.appendChild(overlay);

  var opener = null;

  function open(img) {
    opener = img;
    // Use the original file, not the responsive srcset variant.
    full.src = img.getAttribute('src');
    full.alt = img.alt || '';
    overlay.hidden = false;
    overlay.scrollTop = 0;
    document.documentElement.classList.add('lightbox-open');
    closeBtn.focus();
  }

  function close() {
    overlay.hidden = true;
    full.removeAttribute('src');
    document.documentElement.classList.remove('lightbox-open');
    if (opener) opener.focus();
    opener = null;
  }

  imgs.forEach(function (img) {
    img.classList.add('zoomable');
    img.tabIndex = 0;
    img.setAttribute('role', 'button');
    img.addEventListener('click', function () { open(img); });
    img.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        open(img);
      }
    });
  });

  overlay.addEventListener('click', close);
  closeBtn.addEventListener('click', close);

  document.addEventListener('keydown', function (e) {
    if (overlay.hidden) return;
    if (e.key === 'Escape') {
      close();
    } else if (e.key === 'Tab') {
      // Only the close button is focusable inside the dialog: keep focus there.
      e.preventDefault();
      closeBtn.focus();
    }
  });
})();
