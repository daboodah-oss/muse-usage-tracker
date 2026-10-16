# muse-usage-tracker
Muse subscription usage tracker dashboard (auto-updated hourly)

## Installed app

The page is installable as a web app. In `manifest.webmanifest`,
`theme_color` and `background_color` are both `#0f1420` — the dashboard
page's own background colour — so the installed app's chrome and splash
screen match the page. The manifest deliberately has no `id`: the site
is served from the shared host `daboodah-oss.github.io`, where a relative
`id` would resolve against the host root, and adding any `id` would
change the app's identity for copies already installed. The maskable
icon (`icons/icon-maskable-512.png`) is generated from
`icons/icon-512.png` by `tools/make_maskable.py`. There is no service
worker: the page has no install button and nothing that needs offline
caching, so the worker was retired — `sw.js` is a stub that deletes the
old caches and unregisters itself on clients that still have it. The
stub must stay served for at least 30 days after this lands; after that,
`sw.js` can be deleted.
