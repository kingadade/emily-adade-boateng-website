#!/usr/bin/env python3
"""Build the press kit (/press/) and the 404 page.

    python3 content/build-pages.py

Both share the header and footer in site_parts.py with the lyrics pages.
Everything on the press page restates facts already published on the home
page; when one changes, change both.
"""
import json
from html import escape
from pathlib import Path

from site_parts import FONTS, FOOTER, ICONS, NAV_JS, SITE, SITE_CSS_V, header

ROOT = Path(__file__).resolve().parent.parent
PRESS_CSS_V = "1"   # bump when assets/css/press.css changes


def head(title, desc, path, extra=""):
    url = SITE + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc, quote=True)}">
{extra}<meta property="og:site_name" content="Emily Adade Boateng">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(desc, quote=True)}">
<meta property="og:image" content="{SITE}/assets/img/og-emily.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{ICONS}
<meta name="theme-color" content="#17100c">
{FONTS}
<link rel="stylesheet" href="/assets/css/site.css?v={SITE_CSS_V}">
<link rel="stylesheet" href="/assets/css/press.css?v={PRESS_CSS_V}">
"""


TAIL = f"""
{FOOTER}

<script>
{NAV_JS}</script>
<script src="/assets/js/stats.js?v=1" defer></script>
</body>
</html>
"""

# ------------------------------------------------------------------ press
SHORT_BIO = ("Emily Adade Boateng is a Ghanaian gospel singer and songwriter from the Western Region. "
             "Born in 2012, she began recording at eleven and has since released three albums, two EPs and "
             "five singles. She won Best New Artiste of the Year and Gospel Song of the Year at the 2025 "
             "Western Music Awards, and Discovery of the Year at the 2026 Western Gospel Awards.")

LONG_BIO = [
    "Emily Adade Boateng was born in 2012 in Ghana’s Western Region and started recording at eleven. "
    "Her debut album, King of Glory, arrived in 2024, followed the same year by the Aseda EP, whose title "
    "track features Joyce Blessing. Ahead of Ghana’s December 2024 elections she released Peace with Selina "
    "Boateng, a plea for a calm nation that was referenced in Parliament during the election season.",
    "Miracle Working God (June 2025) and Nyame Prɛkopɛ (January 2026) made it three albums before her "
    "fourteenth birthday. At the 2025 Western Music Awards she won both Best New Artiste of the Year and "
    "Gospel Song of the Year, the latter for Aseda. In March 2026 she signed with PM Entertainment Consult "
    "as the Takoradi company’s first gospel artiste. The single Defender followed in July 2026, and in "
    "October she released On My Way, a five-song EP on which she wrote every song. On 14 November 2026 she was "
    "named Discovery of the Year at the 6th Western Gospel Awards.",
    "Emily writes her own songs and sings in Twi and English, moving between praise, worship and "
    "jazz-inflected arrangements. Beyond the stage she ministers in prisons, on school and university "
    "campuses, and in orphanages.",
]

FACTS = [
    ("Name", "Emily Adade Boateng"),
    ("Born", "2012, Western Region, Ghana"),
    ("Genre", "Gospel: praise and worship"),
    ("Sings in", "Twi (Akan) and English"),
    ("Label", "PM Entertainment Consult, Takoradi (since March 2026)"),
    ("Catalogue", "3 albums, 2 EPs and 5 singles: 42 recordings"),
    ("Latest release", "On My Way EP, 24 October 2026"),
    ("Awards", "Discovery of the Year, Western Gospel Awards 2026. Best New Artiste of the Year and Gospel Song of the Year, Western Music Awards 2025"),
    ("Ministry", "Prisons, school and university campuses, orphanages"),
]

RELEASES = [
    ("On My Way", "EP", "October 2026", "5", "/on-my-way/"),
    ("Defender", "Single", "July 2026", "1", "https://open.spotify.com/album/4XTpzAGIGcVGCMWWrAfo3B"),
    ("Nyame Prɛkopɛ", "Album", "January 2026", "10", "https://open.spotify.com/album/1z0zzwwpvwiNJ9J3ilv8rL"),
    ("Glory", "Single", "December 2025", "1", "https://open.spotify.com/album/5Jmyarma5MGjElxlv3dlc4"),
    ("Miracle Working God", "Album", "June 2025", "9", "https://open.spotify.com/album/1lkyyStEdkiuli4FEUPpP6"),
    ("Fakye (feat. Ablin Adade Boateng)", "Single", "February 2025", "1", "https://open.spotify.com/album/0qSgE2I9456bZYfwHi7Bgo"),
    ("Yɛn Boafo", "Single", "February 2025", "1", "https://open.spotify.com/album/21K1D4r36O5UQ5QELLXZLp"),
    ("Aseda (title track feat. Joyce Blessing)", "EP", "October 2024", "5", "https://open.spotify.com/album/6W8DQtYXuHJEnigbdHZkeo"),
    ("Peace (feat. Selina Boateng)", "Single", "August 2024", "1", "https://open.spotify.com/album/4HZLkjyIjhLWmNBK5IGQ7v"),
    ("King of Glory", "Album", "July 2024", "8", "https://open.spotify.com/album/16MdiLe7zG8T2OGCrmBe6P"),
]

# (file stem, caption, pixel size) — the full-size JPEG is the download.
PHOTOS = [
    ("wga-portrait", "With the Discovery of the Year trophy", "960 × 1280"),
    ("wga-trophy", "At the Western Gospel Awards", "960 × 1280"),
    ("press-02", "Studio portrait", "1350 × 1800"),
    ("press-04", "Studio portrait, blue", "1350 × 1800"),
    ("stage-02", "Live on stage", "1200 × 1800"),
    ("award-trophies", "With both Western Music Awards", "1200 × 1800"),
    ("award-team", "With her team at the awards", "2200 × 1466"),
    ("cover-on-my-way", "On My Way EP cover", "1600 × 1600"),
]

VIDEOS = [
    ("Discovery of the Year: the award presentation, Western Gospel Awards 2026", "pMVCAKFzgTU"),
    ("On stage with Joyce Blessing, Western Gospel Awards 2026", "q0t7DZgmY4I"),
    ("On My Way (official music video)", "VZae3haI7IY"),
    ("Defender (official video)", "eByEmMEnzOM"),
    ("Aseda feat. Joyce Blessing (official music video)", "Wl-ExQuOiQY"),
    ("Never Be the Same (live performance)", "YlrOa2hJaHg"),
]

COVERAGE = [
    ("MyJoyOnline", "12-year-old Emily Adade Boateng stuns with gospel music",
     "https://www.myjoyonline.com/12-year-old-emily-adade-boateng-stuns-with-gospel-music/"),
    ("Ghana Music", "Emily Adade Boateng: Ghana’s 12-year-old gospel prodigy",
     "https://ghanamusic.com/bloggers/2025/07/11/emily-adade-boateng-ghanas-12-year-old-gospel-prodigy/"),
    ("Modern Ghana", "The 12-year-old Ghanaian gospel gem",
     "https://www.modernghana.com/entertainment/81247/the-12-year-old-ghanaian-gospel-gem-rewriting.html"),
    ("YFM Ghana", "PM Entertainment Consult signs its first gospel artiste",
     "https://yfmghana.com/pm-entertainment-consult-signs-its-first-gospel-artiste-emily-adade-boateng/"),
]


# The press page adds one script: copy a biography as plain paragraphs.
PRESS_TAIL = TAIL.replace("</script>\n<script src", '''  // Copy a biography to the clipboard as plain paragraphs.
  document.querySelectorAll('.pk-copy').forEach(btn => btn.addEventListener('click', async () => {
    const text = [...document.getElementById(btn.dataset.copy).querySelectorAll('p')].map(p => p.textContent.trim()).join('\\n\\n');
    try { await navigator.clipboard.writeText(text); btn.textContent = 'Copied'; }
    catch (_) { btn.textContent = 'Select and copy'; }
    setTimeout(() => { btn.textContent = 'Copy'; }, 2200);
  }));
</script>
<script src''', 1)


def press_page():
    title = "Press Kit — Emily Adade Boateng"
    desc = ("Press kit for Emily Adade Boateng, Ghanaian gospel singer: biography, quick facts, awards, "
            "discography, press photos to download, videos and booking contacts.")
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Emily Adade Boateng", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Press kit", "item": SITE + "/press/"}]}
    page = {"@context": "https://schema.org", "@type": "AboutPage", "name": title, "url": SITE + "/press/",
            "description": desc,
            "about": {"@type": "MusicGroup", "@id": SITE + "/#artist", "name": "Emily Adade Boateng", "url": SITE + "/"}}
    extra = (f'<link rel="canonical" href="{SITE}/press/">\n'
             f'<meta property="og:type" content="website">\n<meta property="og:url" content="{SITE}/press/">\n')
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (page, crumbs))

    facts = "\n".join(f"          <div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>" for k, v in FACTS)
    long_bio = "\n".join(f"            <p>{escape(p)}</p>" for p in LONG_BIO)
    ext = ' target="_blank" rel="noopener"'
    rows = "\n".join(
        f'            <tr><th scope="row">{escape(t)}</th><td>{k}</td><td>{d}</td><td>{n}</td>'
        f'<td><a href="{u}"{"" if u.startswith("/") else ext}>Listen</a></td></tr>'
        for t, k, d, n, u in RELEASES)
    photos = "\n".join(
        f'''          <figure class="pk-photo">
            <picture><source srcset="/assets/img/{f}-480.webp" type="image/webp"><img src="/assets/img/{f}-480.jpg" alt="{escape(c, quote=True)}: Emily Adade Boateng" loading="lazy" decoding="async" width="480" height="{h}"></picture>
            <figcaption><span>{escape(c)}<small>JPEG · {size} px</small></span>
              <a class="pk-dl" href="/assets/img/{f}.jpg" download="emily-adade-boateng-{f}.jpg" data-track="press-photo-{f}">Download</a></figcaption>
          </figure>'''
        for (f, c, size), h in ((p, _thumb_h(p[2])) for p in PHOTOS))
    videos = "\n".join(
        f'            <li><a href="https://www.youtube.com/watch?v={v}" target="_blank" rel="noopener">{escape(t)}</a></li>'
        for t, v in VIDEOS)
    coverage = "\n".join(
        f'            <li><a href="{u}" target="_blank" rel="noopener">{escape(h)}</a> <span>{escape(o)}</span></li>'
        for o, h, u in COVERAGE)

    return f"""{head(title, desc, "/press/", extra)}{ld}
</head>
<body class="pk-body">

<a class="skip-link" href="#main">Skip to content</a>
{header()}

<main id="main">
  <section class="pk-hero">
    <div class="wrap pk-hero__inner">
      <div>
        <span class="eyebrow">Press kit</span>
        <h1>Emily Adade Boateng</h1>
        <p class="lede">Ghanaian gospel singer and songwriter. Everything a journalist, presenter or event organiser needs, in one place.</p>
        <div class="btn-row">
          <a class="btn" href="#photos">Download photos</a>
          <a class="btn btn--ghost" href="#contact">Booking and interviews</a>
        </div>
        <nav class="pk-toc" aria-label="On this page">
          <a href="#facts">Quick facts</a><a href="#bio">Biography</a><a href="#awards">Awards</a><a href="#music">Discography</a><a href="#photos">Photos</a><a href="#videos">Videos</a><a href="#coverage">Coverage</a><a href="#contact">Contact</a>
        </nav>
      </div>
      <picture class="pk-hero__photo">
        <source srcset="/assets/img/press-02-480.webp 480w, /assets/img/press-02-960.webp 960w" sizes="(min-width: 900px) 380px, 70vw" type="image/webp">
        <img src="/assets/img/press-02-960.jpg" alt="Emily Adade Boateng at a studio microphone" width="960" height="1280" fetchpriority="high">
      </picture>
    </div>
  </section>

  <section class="pk-section" id="facts">
    <div class="wrap">
      <h2>Quick facts</h2>
      <dl class="pk-facts">
{facts}
      </dl>
    </div>
  </section>

  <section class="pk-section pk-section--alt" id="bio">
    <div class="wrap pk-bios">
      <div class="pk-bio">
        <div class="pk-bio__head"><h2>Short biography</h2><button class="pk-copy" type="button" data-copy="bioShort" data-track="press-copy-short">Copy</button></div>
        <div class="pk-bio__text" id="bioShort">
            <p>{escape(SHORT_BIO)}</p>
        </div>
      </div>
      <div class="pk-bio">
        <div class="pk-bio__head"><h2>Full biography</h2><button class="pk-copy" type="button" data-copy="bioLong" data-track="press-copy-long">Copy</button></div>
        <div class="pk-bio__text" id="bioLong">
{long_bio}
        </div>
      </div>
    </div>
  </section>

  <section class="pk-section" id="awards">
    <div class="wrap">
      <h2>Awards</h2>
      <ul class="pk-awards">
        <li><strong>Winner</strong><span>Discovery of the Year</span><small>Western Gospel Awards, 6th edition, 14 November 2026. Nominated in five categories.</small></li>
        <li><strong>Winner</strong><span>Best New Artiste of the Year</span><small>Western Music Awards 2025</small></li>
        <li><strong>Winner</strong><span>Gospel Song of the Year, for “Aseda” feat. Joyce Blessing</span><small>Western Music Awards 2025</small></li>
      </ul>
    </div>
  </section>

  <section class="pk-section pk-section--alt" id="music">
    <div class="wrap">
      <h2>Discography</h2>
      <div class="pk-tablewrap">
        <table class="pk-table">
          <thead><tr><th scope="col">Release</th><th scope="col">Type</th><th scope="col">Released</th><th scope="col">Tracks</th><th scope="col"><span class="sr-only">Link</span></th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
      <p class="pk-note">Every song title is on the <a href="/#tracks">complete tracklist</a>, and the words to many of them are on the <a href="/lyrics/">lyrics pages</a>.</p>
    </div>
  </section>

  <section class="pk-section" id="photos">
    <div class="wrap">
      <h2>Press photos</h2>
      <p class="pk-note">Free to use in coverage of Emily and her music. Tap Download for the full-size file.</p>
      <div class="pk-photos">
{photos}
      </div>
    </div>
  </section>

  <section class="pk-section pk-section--alt" id="videos">
    <div class="wrap pk-two">
      <div>
        <h2>Videos</h2>
        <ul class="pk-links">
{videos}
        </ul>
        <p class="pk-note">More on <a href="https://www.youtube.com/@EmilyAdadeBoateng" target="_blank" rel="noopener">her YouTube channel</a>.</p>
      </div>
      <div id="coverage">
        <h2>Coverage</h2>
        <ul class="pk-links pk-links--press">
{coverage}
        </ul>
      </div>
    </div>
  </section>

  <section class="pk-section pk-contact" id="contact">
    <div class="wrap pk-two">
      <div>
        <h2>Booking and interviews</h2>
        <p>Emily is fourteen. Bookings, interviews and all correspondence are arranged through her family and management.</p>
        <div class="btn-row">
          <a class="btn" href="https://wa.me/233244239155?text=Hello%2C%20I%27m%20writing%20about%20Emily%20Adade%20Boateng." target="_blank" rel="noopener" data-track="press-whatsapp">WhatsApp +233 24 423 9155</a>
          <a class="btn btn--ghost" href="mailto:abrahamadade@techspringgh.com?subject=Press%20enquiry%20%E2%80%94%20Emily%20Adade%20Boateng" data-track="press-email">Email the team</a>
        </div>
        <p class="pk-note">To invite Emily to an event, the <a href="/#book">booking form</a> is the quickest route.</p>
      </div>
      <div>
        <h2>Follow and listen</h2>
        <ul class="pk-links">
          <li><a href="https://www.youtube.com/@EmilyAdadeBoateng" target="_blank" rel="noopener">YouTube</a> <span>@EmilyAdadeBoateng</span></li>
          <li><a href="https://www.instagram.com/emily_adade/" target="_blank" rel="noopener">Instagram</a> <span>@emily_adade</span></li>
          <li><a href="https://www.tiktok.com/@emily.adade" target="_blank" rel="noopener">TikTok</a> <span>@emily.adade</span></li>
          <li><a href="https://web.facebook.com/profile.php?id=61560611640434" target="_blank" rel="noopener">Facebook</a></li>
          <li><a href="https://open.spotify.com/artist/1znF2dfvSmw74C5HMTlSIS" target="_blank" rel="noopener">Spotify</a></li>
          <li><a href="https://music.apple.com/artist/emily-adade-boateng/1755930781" target="_blank" rel="noopener">Apple Music</a></li>
          <li><a href="https://www.boomplay.com/artists/EQJGmN_DTD4Iiv9CwY_0a1t4" target="_blank" rel="noopener">Boomplay</a></li>
          <li><a href="https://audiomack.com/emilyadade" target="_blank" rel="noopener">Audiomack</a></li>
        </ul>
      </div>
    </div>
  </section>
</main>
{PRESS_TAIL}"""


def _thumb_h(size):
    w, h = (int(x) for x in size.split(" × "))
    return round(480 * h / w)


# ------------------------------------------------------------------ 404
def not_found():
    return f"""{head("Page not found — Emily Adade Boateng", "That page is not here. Find Emily Adade Boateng’s music, videos, lyrics and booking details from the home page.", "/404.html", '<meta name="robots" content="noindex">' + chr(10))}</head>
<body class="pk-body">

<a class="skip-link" href="#main">Skip to content</a>
{header()}

<main id="main">
  <section class="pk-hero nf">
    <div class="wrap">
      <span class="eyebrow">Page not found</span>
      <h1>That page isn’t here.</h1>
      <p class="lede">It may have moved when the site was rebuilt. Everything is one tap away:</p>
      <div class="btn-row">
        <a class="btn" href="/">Home</a>
        <a class="btn btn--ghost" href="/on-my-way/">New EP: On My Way</a>
        <a class="btn btn--ghost" href="/#music">Music</a>
        <a class="btn btn--ghost" href="/lyrics/">Lyrics</a>
        <a class="btn btn--ghost" href="/#book">Book Emily</a>
      </div>
    </div>
  </section>
</main>
{TAIL}"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


write(ROOT / "press" / "index.html", press_page())
write(ROOT / "404.html", not_found())
