#!/usr/bin/env python3
"""Push the rebuilt Muse usage dashboard to daboodah-oss/muse-usage-tracker
via real git.

Replaces the old gh.py push-file upload (Contents API, whole file every
run, hard 1 MB ceiling — the dashboard HTML is ~763 KB and growing).
Git transport sends only the changed bytes.

The clone at ~/workspace/muse-usage-tracker-clone is a transport
vehicle only: the file build_dashboard.py writes
(files/usage-dashboard.html) is the source of truth. Each run re-syncs
the clone to origin/main, copies the dashboard in as index.html,
commits if it changed, and pushes — retrying the whole sequence on a
non-fast-forward rejection.

Auth: a repo-scoped deploy key (write, this repo only) at
~/.ssh/muse_tracker_deploy, used via the clone's core.sshCommand.
This VM's egress proxy resets direct SSH, so the key talks to
ssh.github.com:443 through an HTTP CONNECT tunnel (ssh_proxy.py,
kept with the assistant-usage muse lane's scripts, reads the proxy
address/credentials from the HTTPS_PROXY environment variable).
Same pattern as the assistant-usage muse lane — see that repo's
lanes/muse/README.md.
"""
import os
import shutil
import subprocess
import sys
import time

HOME = os.path.expanduser("~")
SRC = os.path.join(HOME, "workspace", "goals", "muse-usage-tracker-2",
                   "files", "usage-dashboard.html")
CLONE = os.path.join(HOME, "workspace", "muse-usage-tracker-clone")
DST = os.path.join(CLONE, "index.html")
ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0")


def git(*args):
    return subprocess.run(["git", "-C", CLONE, *args],
                          capture_output=True, text=True, timeout=120, env=ENV)


def main():
    if not os.path.isdir(os.path.join(CLONE, ".git")):
        print(f"pusher: clone missing at {CLONE}", file=sys.stderr)
        return 1
    if not os.path.exists(SRC):
        print(f"pusher: source HTML missing at {SRC}", file=sys.stderr)
        return 1
    for attempt in range(1, 4):
        r = git("fetch", "origin", "main")
        if r.returncode != 0:
            print(f"pusher: fetch failed: {r.stderr.strip()[:200]}", file=sys.stderr)
            return 1
        git("reset", "--hard", "origin/main")
        shutil.copyfile(SRC, DST)
        git("add", "index.html")
        if not git("status", "--porcelain").stdout.strip():
            print("pusher: unchanged, nothing to push")
            return 0
        r = git("commit", "-m", "Usage dashboard (auto)")
        if r.returncode != 0:
            print(f"pusher: commit failed: {r.stderr.strip()[:200]}", file=sys.stderr)
            return 1
        r = git("push", "origin", "main")
        if r.returncode == 0:
            sha = git("rev-parse", "--short", "HEAD").stdout.strip()
            print(f"pusher: pushed {sha}")
            return 0
        print(f"pusher: push attempt {attempt} rejected, retrying",
              file=sys.stderr)
        time.sleep(5)
    print("pusher: push failed after 3 attempts", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
