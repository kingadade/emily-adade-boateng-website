"""Header, footer and head links shared by the generated sub-pages
(/lyrics/, /press/, 404). The home page and /on-my-way/ are written by hand
and carry their own copies: change the menu here AND there.
"""

SITE = "https://www.emilyadadeboateng.com"
SITE_CSS_V = "15"  # keep in step with index.html

ICONS = """<link rel="icon" type="image/png" sizes="48x48" href="/assets/img/favicon-48.png">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/favicon-192.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">"""

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">"""

_HEADER = """<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="/">
      <img src="/assets/img/logo-emily.png" alt="" width="48" height="30">
      <span class="brand__name">Emily Adade Boateng
        <span class="brand__sub">Gospel Ministry</span>
      </span>
    </a>

    <nav class="nav" id="nav" aria-label="Primary">
      <a href="/#listen">Listen</a>
      <a href="/#music">Music</a>
      <a href="/#watch">Watch</a>
      <a href="/#awards">Awards</a>
      <a href="/#story">Story</a>
      <a href="/#ministry">Ministry</a>
      <a href="/#events">Events</a>
      <a href="/lyrics/"{lyrics_current}>Lyrics</a>
      <a class="nav__book" href="/#book">Book Emily</a>
    </nav>

    <a class="btn header-cta" href="/#book">Book Emily</a>

    <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="nav" aria-label="Open menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
        <path d="M4 7h16M4 12h16M4 17h16"/>
      </svg>
    </button>
  </div>
</header>"""


def header(current=""):
    """The site header. current="lyrics" underlines Lyrics in the menu."""
    return _HEADER.replace("{lyrics_current}", ' aria-current="page"' if current == "lyrics" else "")


FOOTER = """<footer class="site-footer footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="brand" href="/">
          <img src="/assets/img/logo-emily.png" alt="" width="48" height="30">
          <span class="brand__name">Emily Adade Boateng<span class="brand__sub">Gospel Ministry</span></span>
        </a>
        <p>Ghanaian gospel singer. Praise, worship and outreach — in prisons, on campuses, and in orphanages.</p>
      </div>
      <div>
        <h4>Music</h4>
        <ul>
          <li><a href="/#listen">Listen</a></li>
          <li><a href="/#music">Discography</a></li>
          <li><a href="/on-my-way/">On My Way EP</a></li>
          <li><a href="/lyrics/">Lyrics</a></li>
          <li><a href="/#watch">Videos</a></li>
        </ul>
      </div>
      <div>
        <h4>About</h4>
        <ul>
          <li><a href="/#story">Her story</a></li>
          <li><a href="/#awards">Awards</a></li>
          <li><a href="/#ministry">Ministry</a></li>
          <li><a href="/#events">Events</a></li>
          <li><a href="/press/">Press kit</a></li>
        </ul>
      </div>
      <div>
        <h4>Bookings</h4>
        <ul>
          <li><a href="/#book">Booking request</a></li>
          <li><a href="https://wa.me/233244239155" target="_blank" rel="noopener">WhatsApp enquiry</a></li>
          <li><a href="tel:+233244239155">+233 24 423 9155</a></li>
          <li><a href="mailto:abrahamadade@techspringgh.com">abrahamadade@techspringgh.com</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bar">
      <span>&copy; <span id="year">2026</span> Emily Adade Boateng. All rights reserved.</span>
      <span>Western Region, Ghana</span>
    </div>
  </div>
</footer>"""

# Footer year and the phone menu (open, close, Escape, tap outside).
NAV_JS = """  document.getElementById('year').textContent = new Date().getFullYear();
  (() => {
    const nav = document.getElementById('nav');
    const toggle = document.getElementById('navToggle');
    const setNav = open => {
      nav.dataset.open = String(open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    toggle.addEventListener('click', () => setNav(nav.dataset.open !== 'true'));
    document.addEventListener('keydown', ev => {
      if (ev.key === 'Escape' && nav.dataset.open === 'true') { setNav(false); toggle.focus(); }
    });
    document.addEventListener('click', ev => {
      if (nav.dataset.open === 'true' && !nav.contains(ev.target) && !toggle.contains(ev.target)) setNav(false);
    });
  })();
"""
