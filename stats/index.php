<?php
// Visitor dashboard for emilyadadeboateng.com — /stats/. Password protected.
// Reads the monthly logs written by /hit.php. Times are GMT (Ghana time).

require dirname(__DIR__) . '/stats-lib.php';

// bcrypt hash of the dashboard password (the password itself is kept off the repo).
const STATS_HASH = '$2y$12$S3PzwtJvbw6aZGAZzFjVOumWB0SQSA89qzGn7oYdM7CoQWOlNgjrS';

session_set_cookie_params(['httponly' => true, 'secure' => !empty($_SERVER['HTTPS']), 'samesite' => 'Lax', 'path' => '/stats/']);
session_start();
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex, nofollow');

$error = '';
if (isset($_POST['password'])) {
    if (password_verify((string)$_POST['password'], STATS_HASH)) {
        session_regenerate_id(true);
        $_SESSION['ok'] = true;
        header('Location: ./'); exit;
    }
    sleep(1);
    $error = 'Wrong password.';
}
if (isset($_GET['logout'])) { $_SESSION = []; session_destroy(); header('Location: ./'); exit; }

$h = fn($s) => htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8');

function page_open(string $title): void { ?>
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title><?= htmlspecialchars($title) ?></title>
<style>
  :root { --ink:#17100c; --ink-3:#2e2018; --gold:#d9a441; --cream:#f6efe4; --dim:#cbbba6; --mute:#9a8975; --line:rgba(246,239,228,.12); }
  * { box-sizing: border-box; margin: 0; }
  body { background: var(--ink); color: var(--cream); font: 15px/1.5 Inter, system-ui, -apple-system, sans-serif; padding: 24px 16px 48px; }
  .wrap { max-width: 960px; margin: 0 auto; }
  h1 { font-size: 1.5rem; margin-bottom: .25rem; }
  h2 { font-size: .78rem; letter-spacing: .12em; text-transform: uppercase; color: var(--mute); margin: 2rem 0 .6rem; }
  .sub { color: var(--mute); font-size: .88rem; }
  .bar { display: flex; flex-wrap: wrap; gap: .5rem; align-items: center; justify-content: space-between; margin: 1.25rem 0; }
  .tabs { display: flex; gap: 4px; padding: 4px; background: var(--ink-3); border-radius: 100px; }
  .tabs a { padding: .45rem .9rem; border-radius: 100px; color: var(--dim); text-decoration: none; font-weight: 600; font-size: .88rem; }
  .tabs a[aria-current] { background: var(--gold); color: #221507; }
  .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: .75rem; }
  .kpi { background: var(--ink-3); border-radius: 12px; padding: 1rem; }
  .kpi b { display: block; font-size: 1.9rem; line-height: 1.1; font-variant-numeric: tabular-nums; }
  .kpi span { color: var(--dim); font-size: .85rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0 1.5rem; }
  table { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
  th, td { text-align: left; padding: .5rem .25rem; border-bottom: 1px solid var(--line); vertical-align: top; }
  th { color: var(--mute); font-weight: 600; font-size: .8rem; }
  td.n, th.n { text-align: right; white-space: nowrap; }
  td { overflow-wrap: anywhere; }
  .empty { color: var(--mute); padding: .5rem .25rem; }
  a.out { color: var(--dim); font-size: .88rem; }
  form.login { max-width: 320px; margin: 15vh auto 0; display: flex; flex-direction: column; gap: .75rem; }
  input, button { font: inherit; padding: .75rem 1rem; border-radius: 8px; border: 1px solid var(--line); background: var(--ink-3); color: var(--cream); }
  button { background: var(--gold); color: #221507; font-weight: 700; border: 0; cursor: pointer; }
  .err { color: #f19a8f; }
</style>
</head>
<body>
<div class="wrap">
<?php }

if (empty($_SESSION['ok'])) {
    page_open('Site visitors — sign in'); ?>
  <form class="login" method="post">
    <h1>Site visitors</h1>
    <p class="sub">emilyadadeboateng.com</p>
    <input type="password" name="password" placeholder="Password" autocomplete="current-password" required autofocus aria-label="Password">
    <?php if ($error): ?><p class="err"><?= $h($error) ?></p><?php endif; ?>
    <button type="submit">Open dashboard</button>
  </form>
</div></body></html>
<?php exit; }

// --- load ----------------------------------------------------------------
$ranges = ['today' => 'Today', '7' => '7 days', '30' => '30 days', 'all' => 'All time'];
$range = isset($ranges[$_GET['r'] ?? '']) ? $_GET['r'] : '7';
$today = gmdate('Y-m-d');
$from = $range === 'today' ? $today
    : ($range === 'all' ? '0000-00-00' : gmdate('Y-m-d', strtotime('-' . ((int)$range - 1) . ' days')));

$dir = stats_dir();
$files = glob($dir . '/*.log') ?: [];
sort($files);
$rows = [];
foreach ($files as $f) {
    if ($range !== 'all' && basename($f, '.log') < substr($from, 0, 7)) continue;
    foreach (file($f, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $r = json_decode($line, true);
        if (is_array($r) && ($r['d'] ?? '') >= $from) $rows[] = $r;
    }
}

// --- aggregate -----------------------------------------------------------
$EP = '/on-my-way/';
$names = [
    'spotify' => 'Spotify', 'open.spotify.com' => 'Spotify', 'boomplay' => 'Boomplay', 'boomplay.com' => 'Boomplay',
    'audiomack' => 'Audiomack', 'audiomack.com' => 'Audiomack', 'apple' => 'Apple Music', 'music.apple.com' => 'Apple Music',
    'youtube' => 'YouTube', 'youtube.com' => 'YouTube', 'wa.me' => 'WhatsApp chat', 'share-whatsapp' => 'Shared on WhatsApp',
    'share-native' => 'Shared (phone share button)', 'share-copy' => 'Copied the link', 'voteezy.com' => 'Vote (voteezy)',
];
$pageName = function ($p) use ($EP) {
    if ($p === '/' || $p === '/index.html') return 'Home';
    if ($p === $EP) return 'On My Way EP page';
    if ($p === '/lyrics/') return 'Lyrics index';
    if (strpos($p, '/lyrics/') === 0) return 'Lyrics: ' . ucwords(str_replace('-', ' ', trim(substr($p, 8), '/')));
    return $p;
};

$visitors = []; $views = 0; $epViews = 0; $epVisitors = []; $taps = 0; $epTaps = 0; $mobile = 0;
$days = []; $pages = []; $sources = []; $tapRows = [];
foreach ($rows as $r) {
    $vk = $r['d'] . $r['v'];
    $d = &$days[$r['d']];
    $d ??= ['v' => [], 'views' => 0, 'ep' => 0, 'taps' => 0];
    if ($r['e'] === 'view') {
        $views++;
        $visitors[$vk] = true; $d['v'][$vk] = true; $d['views']++;
        if (!empty($r['m'])) $mobile++;
        if ($r['p'] === $EP) { $epViews++; $epVisitors[$vk] = true; $d['ep']++; }
        $pg = &$pages[$pageName($r['p'])]; $pg ??= ['views' => 0, 'v' => []]; $pg['views']++; $pg['v'][$vk] = true; unset($pg);
        $src = $r['s'] !== '' ? 'Link tag: ' . $r['s'] : ($r['r'] !== '' ? $r['r'] : 'Direct, WhatsApp or apps');
        $sources[$src] = ($sources[$src] ?? 0) + 1;
    } else {
        $taps++; $d['taps']++;
        if ($r['p'] === $EP) $epTaps++;
        $key = ($names[$r['k']] ?? $r['k']) . '|' . $pageName($r['p']);
        $tapRows[$key] = ($tapRows[$key] ?? 0) + 1;
    }
    unset($d);
}
krsort($days);
uasort($pages, fn($a, $b) => $b['views'] <=> $a['views']);
arsort($sources); arsort($tapRows);
$fmt = fn($n) => number_format($n);

// --- render --------------------------------------------------------------
page_open('Site visitors'); ?>
  <h1>Site visitors</h1>
  <p class="sub">emilyadadeboateng.com · Ghana time (GMT) · updated <?= gmdate('j M Y, H:i') ?></p>
  <div class="bar">
    <nav class="tabs" aria-label="Period">
      <?php foreach ($ranges as $k => $label): ?>
        <a href="?r=<?= $k ?>"<?= $k === $range ? ' aria-current="page"' : '' ?>><?= $label ?></a>
      <?php endforeach; ?>
    </nav>
    <a class="out" href="?logout=1">Sign out</a>
  </div>

  <div class="kpis">
    <div class="kpi"><b><?= $fmt(count($visitors)) ?></b><span>Visitors</span></div>
    <div class="kpi"><b><?= $fmt($views) ?></b><span>Page views</span></div>
    <div class="kpi"><b><?= $fmt(count($epVisitors)) ?></b><span>Visitors to the EP page</span></div>
    <div class="kpi"><b><?= $fmt($epTaps) ?></b><span>Stream / share taps on the EP page</span></div>
  </div>
  <p class="sub" style="margin-top:.6rem">A visitor is one phone or computer per day. <?= $views ? round($mobile * 100 / $views) : 0 ?>% of views were on phones.</p>

  <h2>Day by day</h2>
  <table>
    <tr><th>Day</th><th class="n">Visitors</th><th class="n">Views</th><th class="n">EP page</th><th class="n">Taps</th></tr>
    <?php foreach ($days as $day => $d): ?>
      <tr><td><?= $h(gmdate('D j M', strtotime($day))) ?></td><td class="n"><?= $fmt(count($d['v'])) ?></td><td class="n"><?= $fmt($d['views']) ?></td><td class="n"><?= $fmt($d['ep']) ?></td><td class="n"><?= $fmt($d['taps']) ?></td></tr>
    <?php endforeach; if (!$days): ?><tr><td class="empty" colspan="5">No visits recorded in this period yet.</td></tr><?php endif; ?>
  </table>

  <div class="grid">
    <div>
      <h2>Buttons tapped</h2>
      <table>
        <tr><th>Button</th><th>On page</th><th class="n">Taps</th></tr>
        <?php foreach ($tapRows as $key => $n): [$btn, $pg] = explode('|', $key, 2); ?>
          <tr><td><?= $h($btn) ?></td><td><?= $h($pg) ?></td><td class="n"><?= $fmt($n) ?></td></tr>
        <?php endforeach; if (!$tapRows): ?><tr><td class="empty" colspan="3">None yet.</td></tr><?php endif; ?>
      </table>
    </div>
    <div>
      <h2>Where visitors came from</h2>
      <table>
        <tr><th>Source</th><th class="n">Views</th></tr>
        <?php foreach (array_slice($sources, 0, 15, true) as $src => $n): ?>
          <tr><td><?= $h($src) ?></td><td class="n"><?= $fmt($n) ?></td></tr>
        <?php endforeach; if (!$sources): ?><tr><td class="empty" colspan="2">None yet.</td></tr><?php endif; ?>
      </table>
      <p class="sub" style="margin-top:.5rem">"Link tag: ep" = arrived through emilyadadeboateng.com/ep (the QR code or the short link).</p>
    </div>
  </div>

  <h2>Pages</h2>
  <table>
    <tr><th>Page</th><th class="n">Visitors</th><th class="n">Views</th></tr>
    <?php foreach ($pages as $name => $p): ?>
      <tr><td><?= $h($name) ?></td><td class="n"><?= $fmt(count($p['v'])) ?></td><td class="n"><?= $fmt($p['views']) ?></td></tr>
    <?php endforeach; if (!$pages): ?><tr><td class="empty" colspan="3">None yet.</td></tr><?php endif; ?>
  </table>
</div>
</body>
</html>
