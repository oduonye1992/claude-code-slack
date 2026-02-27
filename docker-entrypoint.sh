#!/bin/sh
set -e

# Fix ownership of mounted volumes so the scout user can write to them.
# Runs as root briefly, then drops privileges via gosu/su-exec.
chown -R scout:scout /app/data 2>/dev/null || true

exec gosu scout "$@"
