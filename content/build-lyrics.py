#!/usr/bin/env python3
"""Build the /lyrics/ pages from content/lyrics.json.

    python3 content/build-lyrics.py

Writes lyrics/index.html, lyrics/<slug>/index.html for every song, and the
lyrics block of sitemap.xml. The pages are plain static HTML like the rest of
the site; re-run this after any edit to lyrics.json and commit the output.
"""
import json
import re
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.emilyadadeboateng.com"
CSS_V = "1"        # bump when assets/css/lyrics.css changes
SITE_CSS_V = "13"  # keep in step with index.html

data = json.loads((ROOT / "content" / "lyrics.json").read_text(encoding="utf-8"))
songs = data["songs"]


def e(s):
    return escape(s, quote=True)


def meta_line(s):
    return f"{s['release']} · {s['year']}"


def picture(cover, alt, cls="", eager=False):
    load = "" if eager else ' loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (
        f'<picture{c}>'
        f'<source srcset="/assets/img/{cover}-480.webp 480w, /assets/img/{cover}-960.webp 960w" sizes="180px" type="image/webp">'
        f'<img src="/assets/img/{cover}-480.jpg" alt="{e(alt)}" width="480" height="480"{load}>'
        f'</picture>'
    )


def plain_lines(song):
    """Full lyric text (repeats expanded to a label) for structured data."""
    out = []
    for sec in song["sections"]:
        out.append(f"[{sec['label']}]")
        for ln in sec.get("lines", []):
            out.append(ln if isinstance(ln, str) else f"{ln['t']} ({ln['note']})")
        out.append("")
    return "\n".join(out).strip()


def first_line(song):
    if song.get("hook"):
        return song["hook"]
    for sec in song["sections"]:
        for ln in sec.get("lines", []):
            return ln if isinstance(ln, str) else ln["t"]
    return ""


HEADER = """<a class="skip" href="#lyrics">Skip to lyrics</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="/">
      <img src="/assets/img/logo-mark.png" alt="" width="34" height="34">
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
      <a href="/#book">Book Emily</a>
    </nav>

    <a class="btn header-cta" href="/#book">Book Emily</a>

    <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="nav" aria-label="Open menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
        <path d="M4 7h16M4 12h16M4 17h16"/>
      </svg>
    </button>
  </div>
</header>"""

FOOTER = """<footer class="site-footer footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="brand" href="/">
          <img src="/assets/img/logo-mark.png" alt="" width="34" height="34">
          <span class="brand__name">Emily Adade Boateng<span class="brand__sub">Gospel Ministry</span></span>
        </a>
        <p>Ghanaian gospel singer. Praise, worship and outreach — in prisons, on campuses, and in orphanages.</p>
      </div>
      <div>
        <h4>Music</h4>
        <ul>
          <li><a href="/#listen">Listen</a></li>
          <li><a href="/#music">Discography</a></li>
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
        </ul>
      </div>
      <div>
        <h4>Bookings</h4>
        <ul>
          <li><a href="https://wa.me/233244239155" target="_blank" rel="noopener">WhatsApp enquiry</a></li>
          <li><a href="tel:+233244239155">+233 24 423 9155</a></li>
          <li><a href="mailto:abrahamadade@techspringgh.com">abrahamadade@techspringgh.com</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bar">
      <span>&copy; <span id="year">2026</span> Emily Adade Boateng. All rights reserved.</span>
      <span>Ghana</span>
    </div>
  </div>
</footer>"""

SCRIPT = """<script>
  document.getElementById('year').textContent = new Date().getFullYear();
  (() => {
    const nav = document.getElementById('nav');
    const toggle = document.getElementById('navToggle');
    toggle.addEventListener('click', () => {
      const open = nav.dataset.open === 'true';
      nav.dataset.open = String(!open);
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
    });
  })();
  // Reading / Projector view. The choice is remembered on this device only.
  (() => {
    const bar = document.getElementById('viewToggle');
    if (!bar) return;
    const btns = [...bar.querySelectorAll('button')];
    const set = (mode, save) => {
      document.body.dataset.view = mode;
      btns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.view === mode)));
      if (save) { try { localStorage.setItem('lyricsView', mode); } catch (_) {} }
    };
    let saved = 'reading';
    try { saved = localStorage.getItem('lyricsView') || 'reading'; } catch (_) {}
    set(saved === 'projector' ? 'projector' : 'reading', false);
    btns.forEach(b => b.addEventListener('click', () => set(b.dataset.view, true)));
    bar.hidden = false;
  })();
</script>"""


def head(title, desc, url, image, image_alt, jsonld):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Emily Adade Boateng">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:image:alt" content="{e(image_alt)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/logo-mark.png">
<meta name="theme-color" content="#7d1219">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={SITE_CSS_V}">
<link rel="stylesheet" href="/assets/css/lyrics.css?v={CSS_V}">
<script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=2)}
</script>
</head>"""


def song_list(current_slug):
    items = []
    for s in songs:
        cur = ' aria-current="page"' if s["slug"] == current_slug else ""
        items.append(
            f'<li><a href="/lyrics/{s["slug"]}/"{cur}>'
            f'<span class="lyr-list__t">{e(s["title"])}</span>'
            f'<span class="lyr-list__m">{e(meta_line(s))}</span></a></li>'
        )
    return "\n          ".join(items)


def render_sections(song):
    out = []
    for sec in song["sections"]:
        badge = ""
        if sec.get("x2"):
            badge = '<span class="lyr-x2" aria-label="sung twice">×2</span>'
        if sec.get("repeat"):
            badge = '<span class="lyr-repeat">repeat</span>'
        lang = f' lang="{sec["lang"]}"' if sec.get("lang") else ""
        body = ""
        if sec.get("lines"):
            lines = []
            for ln in sec["lines"]:
                if isinstance(ln, str):
                    lines.append(f"<p>{e(ln)}</p>")
                else:
                    lines.append(f'<p>{e(ln["t"])} <span class="lyr-note">{e(ln["note"])}</span></p>')
            body = f'\n        <div class="lyr-lines"{lang}>\n          ' + "\n          ".join(lines) + "\n        </div>"
        cls = "lyr-sec lyr-sec--repeat" if sec.get("repeat") else "lyr-sec"
        out.append(f'      <section class="{cls}">\n        <h2 class="lyr-sec__label">{e(sec["label"])}{badge}</h2>{body}\n      </section>')
    return "\n".join(out)


def song_page(i, s):
    url = f"{SITE}/lyrics/{s['slug']}/"
    img = f"{SITE}/assets/img/{s['cover']}.jpg"
    title = f"{s['title']} Lyrics — Emily Adade Boateng"
    desc = f"Lyrics to “{s['title']}” by Emily Adade Boateng, from {('the ' + s['year'] + ' single') if s['release'] == 'Single' else ('the album ' + s['release'] + ' (' + s['year'] + ')')}. “{first_line(s)}…”"
    rec = {"@type": "MusicRecording", "name": s["title"],
           "byArtist": {"@type": "MusicGroup", "name": "Emily Adade Boateng", "url": SITE + "/"}}
    if s["release"] != "Single":
        rec["inAlbum"] = {"@type": "MusicAlbum", "name": s["release"]}
    if s.get("video"):
        rec["video"] = {"@type": "VideoObject", "name": f"{s['title']} — official video",
                        "embedUrl": f"https://www.youtube-nocookie.com/embed/{s['video']}",
                        "thumbnailUrl": f"https://i.ytimg.com/vi/{s['video']}/maxresdefault.jpg"}
    jsonld = {
        "@context": "https://schema.org", "@type": "MusicComposition",
        "name": s["title"], "url": url,
        "inLanguage": ["ak", "en"] if s.get("akan") else "en",
        "lyrics": {"@type": "CreativeWork", "text": plain_lines(s)},
        "recordedAs": rec,
    }
    prev_s = songs[i - 1] if i > 0 else None
    next_s = songs[i + 1] if i + 1 < len(songs) else None
    pager = []
    if prev_s:
        pager.append(f'<a class="lyr-pager__prev" href="/lyrics/{prev_s["slug"]}/"><small>Previous</small>{e(prev_s["title"])}</a>')
    else:
        pager.append('<span></span>')
    if next_s:
        pager.append(f'<a class="lyr-pager__next" href="/lyrics/{next_s["slug"]}/"><small>Next</small>{e(next_s["title"])}</a>')
    else:
        pager.append('<span></span>')
    notice = ""
    if s.get("akan"):
        notice = '\n      <p class="lyr-notice">Sung in Akan. An English translation is coming — Emily and the family are writing it line by line.</p>'
    watch = ""
    if s.get("video"):
        watch = f'\n          <a class="btn" href="https://www.youtube.com/watch?v={s["video"]}" target="_blank" rel="noopener">Watch the official video</a>'

    return f"""{head(title, desc, url, img, f"{s['title']} — cover art", jsonld)}
<body class="lyr-body" data-view="reading">

{HEADER}

<main>
  <div class="lyr-hero">
    <div class="wrap lyr-hero__inner">
      {picture(s['cover'], f"{s['title']} cover art", "lyr-hero__art", eager=True)}
      <div class="lyr-hero__text">
        <a class="lyr-back" href="/lyrics/">← All lyrics</a>
        <span class="eyebrow">Lyrics · {e(meta_line(s))}</span>
        <h1>{e(s['title'])}</h1>
        <p class="lyr-sub">{e(s['sub'])}</p>
      </div>
    </div>
  </div>

  <div class="lyr-page">
    <div class="wrap lyr-layout">
      <article class="lyr-main" id="lyrics" aria-label="{e(s['title'])} lyrics">
      <div class="lyr-view" id="viewToggle" role="group" aria-label="Display" hidden>
        <button type="button" data-view="reading" aria-pressed="true">Reading</button>
        <button type="button" data-view="projector" aria-pressed="false">Projector</button>
      </div>{notice}
{render_sections(s)}
      <nav class="lyr-pager" aria-label="More songs">
        {pager[0]}
        {pager[1]}
      </nav>
      </article>

      <aside class="lyr-aside">
        <nav class="lyr-card lyr-list" aria-label="All lyrics">
          <h2 class="lyr-card__h">All lyrics · {len(songs)} songs</h2>
          <ul>
          {song_list(s['slug'])}
          </ul>
        </nav>
        <div class="lyr-card lyr-card--dark">
          <h2 class="lyr-card__h">Listen</h2>{watch}
          <div class="lyr-stream">
            <a href="https://open.spotify.com/artist/1znF2dfvSmw74C5HMTlSIS" target="_blank" rel="noopener">Spotify</a>
            <a href="https://www.youtube.com/@EmilyAdadeBoateng" target="_blank" rel="noopener">YouTube</a>
            <a href="https://audiomack.com/search?q=emily%20adade%20boateng" target="_blank" rel="noopener">Audiomack</a>
          </div>
        </div>
        <div class="lyr-card">
          <h2 class="lyr-card__h">For worship teams</h2>
          <p>Singing this in church? Switch to Projector view for a screen-ready page — or invite Emily to lead it herself.</p>
          <a class="lyr-cardlink" href="/#book">Invite Emily to sing →</a>
        </div>
      </aside>
    </div>
  </div>
</main>

{FOOTER}

{SCRIPT}
</body>
</html>
"""


def index_page():
    url = f"{SITE}/lyrics/"
    groups = []
    order = []
    for s in songs:
        key = "Singles" if s["release"] == "Single" else s["release"]
        if key not in order:
            order.append(key)
    for key in order:
        cards = []
        for s in songs:
            if ("Singles" if s["release"] == "Single" else s["release"]) != key:
                continue
            cards.append(
                f'<li><a class="lyr-tile" href="/lyrics/{s["slug"]}/">'
                f'{picture(s["cover"], "")}'
                f'<span class="lyr-tile__text"><span class="lyr-tile__t">{e(s["title"])}</span>'
                f'<span class="lyr-tile__m">{e(meta_line(s))}</span>'
                f'<span class="lyr-tile__l">“{e(first_line(s))}”</span></span></a></li>'
            )
        groups.append(
            f'    <section class="lyr-group">\n      <h2 class="lyr-group__h">{e(key)}</h2>\n'
            f'      <ul class="lyr-tiles">\n        ' + "\n        ".join(cards) + "\n      </ul>\n    </section>"
        )
    jsonld = {"@context": "https://schema.org", "@type": "CollectionPage",
              "name": "Lyrics — Emily Adade Boateng", "url": url,
              "hasPart": [{"@type": "MusicComposition", "name": s["title"],
                           "url": f"{SITE}/lyrics/{s['slug']}/"} for s in songs]}
    return f"""{head("Lyrics — Emily Adade Boateng", "Lyrics to Emily Adade Boateng’s songs — Defender, Glory, Onyankopɔn, Never Be the Same, Mighty Rock and more. In Akan and English, ready for worship teams.", url, f"{SITE}/assets/img/cover-nyame-prekope.jpg", "Nyame Prɛkopɛ album cover", jsonld)}
<body class="lyr-body lyr-body--index">

{HEADER}

<main id="lyrics">
  <div class="lyr-hero">
    <div class="wrap lyr-hero__inner">
      <div class="lyr-hero__text">
        <a class="lyr-back" href="/#tracks">← The complete tracklist</a>
        <span class="eyebrow">Lyrics</span>
        <h1>Sing along.</h1>
        <p class="lyr-sub">The words to {len(songs)} of Emily’s songs, in Akan and English. More are on the way.</p>
      </div>
    </div>
  </div>

  <div class="lyr-page">
    <div class="wrap lyr-index">
{chr(10).join(groups)}
    </div>
  </div>
</main>

{FOOTER}

{SCRIPT}
</body>
</html>
"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


write(ROOT / "lyrics" / "index.html", index_page())
for i, s in enumerate(songs):
    write(ROOT / "lyrics" / s["slug"] / "index.html", song_page(i, s))

# Sitemap: replace everything between the lyrics markers.
today = date.today().isoformat()
urls = [f"{SITE}/lyrics/"] + [f"{SITE}/lyrics/{s['slug']}/" for s in songs]
block = "\n".join(
    f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{'0.7' if u.endswith('/lyrics/') else '0.6'}</priority>\n  </url>"
    for u in urls)
sm_path = ROOT / "sitemap.xml"
sm = sm_path.read_text(encoding="utf-8")
marked = f"  <!-- lyrics:start (generated by content/build-lyrics.py) -->\n{block}\n  <!-- lyrics:end -->\n"
if "<!-- lyrics:start" in sm:
    sm = re.sub(r"  <!-- lyrics:start.*?<!-- lyrics:end -->\n", lambda _: marked, sm, flags=re.S)
else:
    sm = sm.replace("</urlset>", marked + "</urlset>")
sm_path.write_text(sm, encoding="utf-8")
print("updated sitemap.xml")
