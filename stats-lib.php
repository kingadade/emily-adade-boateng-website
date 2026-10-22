<?php
// Shared by hit.php and stats/index.php. Not a page of its own.
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'stats-lib.php') { http_response_code(404); exit; }

// Data lives outside the web root where the host allows it, so a git
// re-deploy never touches it; otherwise in a locked folder inside it.
function stats_dir(): string {
    foreach ([dirname(__DIR__) . '/emily-stats', __DIR__ . '/.stats-data'] as $d) {
        if (is_dir($d) || @mkdir($d, 0750, true)) {
            if (is_writable($d)) {
                if (!is_file($d . '/.htaccess')) @file_put_contents($d . '/.htaccess', "Require all denied\nDeny from all\n");
                return $d;
            }
        }
    }
    http_response_code(500); exit;
}

function stats_secret(string $dir): string {
    $f = $dir . '/secret.txt';
    if (!is_file($f)) file_put_contents($f, bin2hex(random_bytes(16)), LOCK_EX);
    return trim((string)file_get_contents($f));
}
