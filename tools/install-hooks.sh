#!/bin/sh
#
# Installs X6 git hooks into .git/hooks.
# Run this once per clone.

set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
SRC="$REPO_ROOT/tools/hooks"
DST="$REPO_ROOT/.git/hooks"

if [ ! -d "$SRC" ]; then
    echo "ERROR: $SRC not found"
    exit 1
fi

mkdir -p "$DST"

for hook in "$SRC"/*; do
    name=$(basename "$hook")
    cp "$hook" "$DST/$name"
    chmod +x "$DST/$name"
    echo "installed: $DST/$name"
done

echo
echo "Done. X6 exemplar guard is active for this clone."
echo "Test: python tools/guard_exemplar.py verify"
