#!/usr/bin/env bash
# Rebuild the calendar (HTML, ICS, PNGs) and the PDF playbook.
# Run from anywhere; needs python3, pandoc, node + playwright (Chromium).
set -euo pipefail
cd "$(dirname "$0")/.."

python3 build/calendar.py
node build/render.js calendar

# The print HTML sits next to the markdown so image paths resolve as written.
pandoc LAUNCH_PLAYBOOK.md -f gfm -t html5 --standalone \
  --lua-filter build/pdf-filter.lua \
  --metadata pagetitle="Launch & Marketing Playbook" \
  --css build/playbook.css \
  -o .playbook-print.html

node build/render.js pdf
rm -f .playbook-print.html
