#!/usr/bin/env python3
"""
One-shot palette swap for Year 3 animations — dark-navy/indigo → V1 warm-light.

Scope:
  - CSS custom property DEFINITIONS only (e.g. `--bg: #0f172a` → `--bg: #FFF9F2`).
  - Specific known hardcoded button-state backgrounds (`.correct{background:#166534}`).
  - Feedback text icons (`✓`/`✗`/`❌`/`✅` → V1 language).

Out of scope (deliberately untouched):
  - Canvas JS colours (ctx.fillStyle = '#fbbf24' etc) — simulator visuals stay as-authored.
  - Raw hex literals in property values that aren't recognised button-state cases.

Safe to re-run: idempotent.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Y3 = ROOT / "animations" / "year-3"

# --- Token value map: OLD hex → NEW hex (V1 Visual Standard) ------------------
TOKEN_MAP = {
    "#0f172a": "#FFF9F2",   # --bg
    "#1e293b": "#FFFFFF",   # --surface
    "#273344": "#F5EEE3",   # --surface2 (variant)
    "#334155": "#F5EEE3",   # --surface2
    "#475569": "#E8DCC7",   # --border
    "#818cf8": "#4A5FDB",   # --primary (indigo)
    "#fbbf24": "#4A5FDB",   # --primary (amber in some files)
    "#38bdf8": "#FF8A3D",   # --accent
    "#4ade80": "#1FA66A",   # --success
    "#34d399": "#1FA66A",   # --success (variant)
    "#f87171": "#D8452B",   # --error
    "#f1f5f9": "#1E1E2A",   # --text (dark→light theme inversion)
    "#e2e8f0": "#1E1E2A",   # --text (variant)
    "#94a3b8": "#5A5566",   # --text-muted
}

# --- Known hardcoded button-state backgrounds ---------------------------------
# These weren't token-driven in the originals, so we map them directly.
LITERAL_MAP = {
    "#166534": "#1FA66A",   # dark-green success bg → success token value
    "#991b1b": "#D8452B",   # dark-red error bg
    "#7f1d1d": "#D8452B",   # dark-red error bg (variant)
}

# --- On-success/on-error text colour fixes -----------------------------------
# Old dark-mode code used `color:#0f172a` on success/error bg (dark text on
# bright button). In the new light palette, white text is required for AA
# contrast on both #1FA66A (green) and #D8452B (red).
# Accent (#FF8A3D orange) still wants dark ink — we leave those alone.
ON_COLOUR_PATTERNS = [
    # `background:var(--success);color:#0f172a` (any whitespace variant)
    (
        re.compile(
            r"(background\s*:\s*var\(--success\)[^;}]*;?\s*color\s*:\s*)#0f172a\b",
            re.IGNORECASE,
        ),
        r"\1#FFFFFF",
    ),
    (
        re.compile(
            r"(background\s*:\s*var\(--error\)[^;}]*;?\s*color\s*:\s*)#0f172a\b",
            re.IGNORECASE,
        ),
        r"\1#FFFFFF",
    ),
    # Reverse order: `color:#0f172a;background:var(--success)`
    (
        re.compile(
            r"(color\s*:\s*)#0f172a(\s*;?\s*background\s*:\s*var\(--success\))",
            re.IGNORECASE,
        ),
        r"\1#FFFFFF\2",
    ),
    (
        re.compile(
            r"(color\s*:\s*)#0f172a(\s*;?\s*background\s*:\s*var\(--error\))",
            re.IGNORECASE,
        ),
        r"\1#FFFFFF\2",
    ),
]

# --- Feedback icon replacements (JS string literals) --------------------------
FEEDBACK_MAP = {
    "'✓ Correct!'": "'Correct!'",
    "'✗ Answer: '": "'Answer: '",
    "'✅ '":         "'",
    "'❌ Not quite. '": "'Not quite. '",
    "'✅'":          "'✓'",
    "'❌'":          "'○'",
}


def swap_css_tokens(text: str) -> tuple[str, int]:
    """Replace `--<name>: #oldhex` with `--<name>: #newhex`. Token defs only."""
    count = 0
    for old_hex, new_hex in TOKEN_MAP.items():
        # Pattern: `--foo:#hex` or `--foo: #hex` (whitespace tolerant).
        pattern = re.compile(
            r"(--[\w-]+\s*:\s*)" + re.escape(old_hex) + r"(?![\w])",
            re.IGNORECASE,
        )
        new_text, n = pattern.subn(lambda m: m.group(1) + new_hex, text)
        if n:
            text = new_text
            count += n
    return text, count


def swap_button_state_literals(text: str) -> tuple[str, int]:
    """Replace specific dark-mode button backgrounds with V1 palette values."""
    count = 0
    for old_hex, new_hex in LITERAL_MAP.items():
        pattern = re.compile(re.escape(old_hex), re.IGNORECASE)
        new_text, n = pattern.subn(new_hex, text)
        if n:
            text = new_text
            count += n
    return text, count


def swap_feedback_icons(text: str) -> tuple[str, int]:
    """Harmonise feedback text to V1 standard (check/circle-pause semantics)."""
    count = 0
    for old, new in FEEDBACK_MAP.items():
        if old in text:
            text = text.replace(old, new)
            count += 1
    return text, count


def swap_on_colour_text(text: str) -> tuple[str, int]:
    """Fix `color:#0f172a` on success/error backgrounds → `color:#FFFFFF`."""
    count = 0
    for pattern, replacement in ON_COLOUR_PATTERNS:
        new_text, n = pattern.subn(replacement, text)
        if n:
            text = new_text
            count += n
    return text, count


def process(path: Path) -> dict:
    original = path.read_text(encoding="utf-8")
    text = original

    text, c_tokens = swap_css_tokens(text)
    text, c_lits   = swap_button_state_literals(text)
    text, c_fbs    = swap_feedback_icons(text)
    text, c_onfg   = swap_on_colour_text(text)

    changed = text != original
    if changed:
        path.write_text(text, encoding="utf-8")

    return {
        "file": str(path.relative_to(ROOT)),
        "changed": changed,
        "tokens": c_tokens,
        "literals": c_lits,
        "feedback": c_fbs,
        "on_fg": c_onfg,
    }


def main() -> int:
    if not Y3.exists():
        print(f"ERROR: {Y3} does not exist", file=sys.stderr)
        return 1

    files = sorted(Y3.rglob("*.html"))
    if not files:
        print(f"No files under {Y3}", file=sys.stderr)
        return 1

    print(f"Processing {len(files)} file(s)")
    print(f"{'File':<60} {'tok':>4} {'lit':>4} {'fb':>4} {'fg':>4} {'chg':>5}")
    print("-" * 90)

    totals = {"tokens": 0, "literals": 0, "feedback": 0, "on_fg": 0, "changed": 0}
    for path in files:
        r = process(path)
        print(
            f"{r['file']:<60} {r['tokens']:>4} {r['literals']:>4} "
            f"{r['feedback']:>4} {r['on_fg']:>4} {('YES' if r['changed'] else '-'):>5}"
        )
        totals["tokens"]   += r["tokens"]
        totals["literals"] += r["literals"]
        totals["feedback"] += r["feedback"]
        totals["on_fg"]    += r["on_fg"]
        totals["changed"]  += int(r["changed"])

    print("-" * 90)
    print(
        f"{'TOTAL':<60} {totals['tokens']:>4} {totals['literals']:>4} "
        f"{totals['feedback']:>4} {totals['on_fg']:>4} {totals['changed']:>5}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
