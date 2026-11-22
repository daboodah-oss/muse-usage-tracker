# muse-usage-tracker
Muse subscription usage tracker dashboard (auto-updated hourly)

> **Status: frozen 2026-11-22.** This page is a snapshot (final build:
> 15,488 samples through Nov 22, 2026, 4:37 PM ET). Its per-cycle history
> moved to the unified dashboard (daboodah-oss/assistant-usage), which now
> carries a cycle-history table for every lane; Muse sampling continues
> there on the 15-minute lane. The full 5-minute collector log is archived
> at `data/usage_log.csv` in this repo. The collector and hourly refresh
> jobs are disabled, not deleted, so the page can be revived by
> re-enabling them.

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
caching, so the worker was retired — `sw.js` was served as a stub that
deleted the old caches and unregistered itself on clients that still
had it; after 30+ days served, the stub was deleted on 2026-11-15.

## Publishing

An hourly cron on Budzilla's VM rebuilds the dashboard and publishes it
as `index.html`. Publishing is a real git push
(`tools/push_dashboard_git.py`; the live copy sits in the tracker
workspace): a transport clone at `~/workspace/muse-usage-tracker-clone`
re-syncs to `main`, takes the rebuilt file, commits, and pushes. Auth
is a repo-scoped deploy key (`~/.ssh/muse_tracker_deploy`; repo
Settings -> Deploy keys, "Budzilla VM muse tracker pusher") reaching
ssh.github.com:443 through the VM egress proxy's HTTP CONNECT tunnel.
This replaced `gh.py push-file` on 2026-11-15 — the Contents API
re-uploaded the whole ~763 KB page every hour and caps files at 1 MB.
