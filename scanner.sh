#!/usr/bin/env bash

ROOT="${1:-.}"
MODE="${2:-full}"
MAX_KB=300

ROOT=$(realpath "$ROOT")
OUT="$ROOT/_scan_output/context.md"
mkdir -p "$(dirname "$OUT")"

echo "Scanning project..."

# Patterns à ignorer
skip() { echo "$1" | grep -qE "node_modules|\.git|\.venv|__pycache__|dist|build"; }

# Extensions valides
valid() {
    local name; name=$(basename "$1")
    echo "$name" | grep -qiE "\.(py|js|ts|json|yml|yaml|md|txt|toml|env|sql|conf)$" && return 0
    echo "$name" | grep -qiE "docker|requirements|package|readme|env" && return 0
    return 1
}

{
    echo "# AGT CONTEXT"
    echo ""
    echo "## PROJECT TREE"
    echo '```'
    find "$ROOT" | while read -r f; do
        skip "$f" || echo "${f#"$ROOT"}"
    done
    echo '```'
    echo ""

    echo "## FILES"
    find "$ROOT" -type f | while read -r f; do
        skip "$f" && continue
        valid "$f" || continue
        size=$(du -k "$f" | cut -f1)
        echo "- $f (${size} KB)"
    done

    echo ""
    echo "## CODE CONTEXT"
    echo ""

    if [[ "$MODE" == "full" ]]; then
        find "$ROOT" -type f | while read -r f; do
            skip "$f" && continue
            valid "$f" || continue
            size=$(du -k "$f" | cut -f1)
            (( size >= MAX_KB )) && continue

            echo "===== FILE START: $f ====="
            echo '```'
            cat "$f" 2>/dev/null || echo "[UNREADABLE]"
            echo '```'
            echo "===== FILE END ====="
            echo ""
        done
    fi

    total=$(find "$ROOT" -type f | while read -r f; do skip "$f" || valid "$f" && echo x; done | wc -l)
    echo "## SUMMARY"
    echo "- Total files: $total"

} > "$OUT"

echo "Done. Output: $OUT"