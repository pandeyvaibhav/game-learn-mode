#!/usr/bin/env python3
"""
One-shot seed for curriculum/status.csv from current filesystem state.

Walks content/ and animations/, matches pairs, reads the X6 protected
manifest for validation status, and writes one CSV row per topic.

Re-running is safe — overwrites the CSV with the current filesystem truth.

See doc/architecture.md §3.2 for the CSV schema.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
ANIMS = ROOT / "animations"
CSV_OUT = ROOT / "curriculum" / "status.csv"
MANIFEST = ROOT / "tools" / "protected-exemplars.json"

# Which Y3 Science topics are the exploded view per curriculum.md (v2)
# and which perspective each belongs to. Used to populate the perspective
# and concept columns for Y3 Science only; everything else is flagged as
# "v1-unassigned" until migrated.
Y3_SCIENCE_CONCEPT_PERSPECTIVE = {
    # Plants
    "plants-functions-y3":   ("plants", "identify"),
    "plant-growth-needs":    ("plants", "sort"),
    "plant-lifecycle":       ("plants", "sequence"),
    "water-transport":       ("plants", "apply"),
    # Rocks & Fossils
    "rocks-fossils":         ("rocks-fossils", "identify"),
    "rock-properties-sort":  ("rocks-fossils", "sort"),
    "fossil-formation":      ("rocks-fossils", "sequence"),
    "soil-composition":      ("rocks-fossils", "compose"),
    # Forces & Magnets
    "forces-magnets":        ("forces-magnets", "identify"),
    "push-pull-sort":        ("forces-magnets", "sort"),
    "friction-surfaces":     ("forces-magnets", "apply"),
    "magnet-distance-experiment": ("forces-magnets", "sequence"),
    # Light & Shadows
    "light-shadows":         ("light-shadows", "identify"),
    "opaque-transparent-sort": ("light-shadows", "sort"),
    "shadow-change":         ("light-shadows", "sequence"),
    "light-safety":          ("light-shadows", "apply"),
}


def sha256_lf(path: Path) -> str:
    raw = path.read_bytes()
    normalised = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalised).hexdigest()


def load_protected_map() -> dict[str, dict]:
    """Map slug -> entry dict from the protected-exemplars manifest."""
    if not MANIFEST.exists():
        return {}
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {e["slug"]: e for e in data.get("protected", [])}


def main() -> int:
    protected = load_protected_map()

    # Discover every content .md under content/year-*/ and every animation .html.
    rows_by_key: dict[tuple[int, str, str], dict] = {}

    for md in sorted(CONTENT.rglob("year-*/**/*.md")):
        rel = md.relative_to(ROOT).as_posix()
        parts = rel.split("/")
        # content/year-3/science/slug.md
        if len(parts) != 4:
            continue
        year = int(parts[1].removeprefix("year-"))
        subject = parts[2]
        slug = parts[3].removesuffix(".md")
        key = (year, subject, slug)
        rows_by_key[key] = {
            "year": year,
            "subject": subject,
            "slug": slug,
            "content_path": rel,
            "animation_path": None,
        }

    for html in sorted(ANIMS.rglob("year-*/**/*.html")):
        rel = html.relative_to(ROOT).as_posix()
        parts = rel.split("/")
        if len(parts) != 4:
            continue
        year = int(parts[1].removeprefix("year-"))
        subject = parts[2]
        slug = parts[3].removesuffix(".html")
        key = (year, subject, slug)
        rows_by_key.setdefault(key, {
            "year": year,
            "subject": subject,
            "slug": slug,
            "content_path": None,
            "animation_path": None,
        })
        rows_by_key[key]["animation_path"] = rel

    # Also seed the planned-but-not-yet-built Y3 Science perspective topics.
    # These rows have content_status=todo + animation_status=todo so the
    # orchestrator knows to produce them.
    for slug, (concept, perspective) in Y3_SCIENCE_CONCEPT_PERSPECTIVE.items():
        key = (3, "science", slug)
        if key not in rows_by_key:
            rows_by_key[key] = {
                "year": 3,
                "subject": "science",
                "slug": slug,
                "content_path": None,
                "animation_path": None,
            }

    # Build CSV rows
    csv_rows = []
    for (year, subject, slug), meta in sorted(rows_by_key.items()):
        content_path = meta.get("content_path") or f"content/year-{year}/{subject}/{slug}.md"
        animation_path = meta.get("animation_path") or f"animations/year-{year}/{subject}/{slug}.html"

        content_exists = (ROOT / content_path).exists()
        animation_exists = (ROOT / animation_path).exists()

        content_status = "done" if content_exists else "todo"
        animation_status = "done" if animation_exists else "todo"

        content_sha = sha256_lf(ROOT / content_path) if content_exists else ""
        animation_sha = sha256_lf(ROOT / animation_path) if animation_exists else ""

        is_protected = slug in protected
        validated_date = protected[slug].get("validated_date", "") if is_protected else ""

        # Concept + perspective
        if (year, subject) == (3, "science") and slug in Y3_SCIENCE_CONCEPT_PERSPECTIVE:
            concept, perspective = Y3_SCIENCE_CONCEPT_PERSPECTIVE[slug]
        else:
            # Pre-v2 flat rows — concept defaults to slug, perspective blank.
            concept = slug
            perspective = ""

        csv_rows.append({
            "year": year,
            "subject": subject,
            "concept": concept,
            "perspective": perspective,
            "slug": slug,
            "content_status": content_status,
            "animation_status": animation_status,
            "protected": "yes" if is_protected else "no",
            "validated_with_child": validated_date,
            "last_reviewed": "",
            "content_sha": content_sha,
            "animation_sha": animation_sha,
        })

    # Write
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(csv_rows[0].keys())
    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    # Summary
    total = len(csv_rows)
    done_both = sum(1 for r in csv_rows if r["content_status"] == "done" and r["animation_status"] == "done")
    todo_any = sum(1 for r in csv_rows if r["content_status"] == "todo" or r["animation_status"] == "todo")
    protected_count = sum(1 for r in csv_rows if r["protected"] == "yes")

    print(f"Wrote {CSV_OUT.relative_to(ROOT)}")
    print(f"  total rows:         {total}")
    print(f"  done (both files):  {done_both}")
    print(f"  todo (any file):    {todo_any}")
    print(f"  protected:          {protected_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
