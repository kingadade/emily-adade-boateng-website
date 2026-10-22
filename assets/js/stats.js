// Visitor counter: one beacon per page view, one per tracked tap. No cookies.
// Collected by /hit.php, read at /stats/.
(() => {
  const send = (e, k) => {
    const body = JSON.stringify({
      e, k: k || '', p: location.pathname, r: document.referrer,
      s: new URLSearchParams(location.search).get('src') || '',
    });
    try {
      if (!navigator.sendBeacon || !navigator.sendBeacon('/hit.php', body)) {
        fetch('/hit.php', { method: 'POST', body, keepalive: true }).catch(() => {});
      }
    } catch (_) {}
  };

  send('view');

  // Tracked: anything marked data-platform / data-track, video play buttons,
  // and every link that leaves the site (labelled by its host).
  document.addEventListener('click', ev => {
    const el = ev.target.closest('[data-platform], [data-track], button[data-id], a[href]');
    if (!el) return;
    let k = el.dataset.platform || el.dataset.track;
    if (!k && el.matches('button[data-id]')) k = 'video-' + el.dataset.id;
    if (!k && el.host && el.host !== location.host && /^https?:/.test(el.protocol)) k = el.hostname.replace(/^www\./, '');
    if (k) send('click', k);
  }, { capture: true });
})();
