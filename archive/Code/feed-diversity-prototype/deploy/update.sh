#!/usr/bin/env bash
# Redeploys the live feed-diversity-prototype service on this VM
# (ClaudeDiscord) from the latest main. Paths are hardcoded to this
# server's specific layout, not meant to be generic - see deploy/README.md
# for the one-time setup this assumes already happened (venv, .env,
# systemd unit).
#
# Usage: bash deploy/update.sh   (run from anywhere, paths below are absolute)
set -euo pipefail

SRC=/home/team13/feed-diversity-src
LIVE=/home/team13/feed-diversity

git -C "$SRC" pull --ff-only origin main

# .env/venv/__pycache__ live only in $LIVE, never in the repo - excluded so
# a plain rsync --delete doesn't wipe secrets or force a venv rebuild every
# deploy.
rsync -a --delete \
  --exclude '.env' --exclude 'venv' --exclude '__pycache__' --exclude '.pytest_cache' \
  "$SRC/Code/feed-diversity-prototype/" "$LIVE/"

"$LIVE/venv/bin/pip" install -q -r "$LIVE/requirements.txt"

sudo systemctl restart feed-diversity
sudo systemctl status feed-diversity --no-pager
