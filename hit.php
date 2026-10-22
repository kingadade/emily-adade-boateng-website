<?php
// Visitor counter for emilyadadeboateng.com. The page script (assets/js/stats.js)
// posts one small JSON body per page view and per tracked tap. Nothing personal
// is kept: no cookies, no IP addresses — only a daily-rotating hash that lets
// the dashboard count the same phone once per day.

require __DIR__ . '/stats-lib.php';

header('Cache-Control: no-store');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit; }

$raw = file_get_contents('php://input', false, null, 0, 2048);
$in = json_decode($raw ?: '', true);
if (!is_array($in)) { http_response_code(400); exit; }

$ua = $_SERVER['HTTP_USER_AGENT'] ?? '';
if ($ua === '' || preg_match('/bot|crawl|spider|slurp|preview|headless|lighthouse|facebookexternalhit|whatsapp|curl|wget|python/i', $ua)) {
    http_response_code(204); exit;
}

$event = ($in['e'] ?? '') === 'click' ? 'click' : 'view';
$clean = fn($v, $n) => substr(preg_replace('/[^a-zA-Z0-9\-_.\/: ]/', '', (string)($v ?? '')), 0, $n);

$refHost = '';
if (!empty($in['r'])) {
    $h = parse_url((string)$in['r'], PHP_URL_HOST);
    if ($h && !preg_match('/(^|\.)emilyadadeboateng\.com$/i', $h)) $refHost = preg_replace('/^www\./', '', strtolower($h));
}

// Behind Hostinger's CDN the visitor's address arrives in a forwarding header.
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['HTTP_X_REAL_IP'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
$ip = trim(explode(',', $ip)[0]);

$dir = stats_dir();
$day = gmdate('Y-m-d');
$visitor = substr(hash('sha256', stats_secret($dir) . $day . $ip . $ua), 0, 12);

$row = [
    't' => time(),
    'd' => $day,
    'v' => $visitor,
    'e' => $event,
    'p' => $clean($in['p'] ?? '/', 120) ?: '/',
    'k' => $event === 'click' ? $clean($in['k'] ?? '', 60) : '',
    'r' => substr($refHost, 0, 80),
    's' => $clean($in['s'] ?? '', 40),
    'm' => preg_match('/Mobi|Android|iPhone/i', $ua) ? 1 : 0,
];

$file = $dir . '/' . gmdate('Y-m') . '.log';
if (!is_file($file) || filesize($file) < 50 * 1024 * 1024) {
    file_put_contents($file, json_encode($row) . "\n", FILE_APPEND | LOCK_EX);
}
http_response_code(204);
