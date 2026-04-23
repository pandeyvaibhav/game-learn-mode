#!/usr/bin/env python3
"""
Sync script — regenerates BOTH

  - curriculum/status.csv   (production matrix — architecture.md §3.2)
  - app/curriculum.json     (topic list the app shell reads)

from current filesystem state.

Walks content/ and animations/, parses YAML frontmatter from each
content.md for topic title + key concepts, reads the X6 protected
manifest for validation status, and writes both artefacts.

Re-running is safe — both outputs are regenerated from the filesystem.
Run this after every new-topic commit so the app shell picks up the
new topics without a manual edit to app/curriculum.json.

Runbook §6 build loop references this command.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
ANIMS = ROOT / "animations"
CSV_OUT = ROOT / "curriculum" / "status.csv"
JSON_OUT = ROOT / "app" / "curriculum.json"
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


# Minimal YAML-frontmatter parser — avoids a PyYAML dependency.
# Only handles the shape our content.md files use:
#   ---
#   year: 3
#   topic: Parts of a Plant
#   key_concepts: [flower, leaves, stem]
#   age_range: "7-8"
#   ---
_FM_LINE = re.compile(r'^(?P<k>[a-zA-Z_][\w-]*)\s*:\s*(?P<v>.*?)\s*$')
_ARRAY = re.compile(r'^\[\s*(.*?)\s*\]\s*$')


def parse_frontmatter(path: Path) -> dict:
    """Return the first YAML frontmatter block of `path` as a flat dict.
    Values are strings, except `key_concepts` which becomes a list of
    strings. Returns {} if the file doesn't start with a `---` fence."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out: dict = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = _FM_LINE.match(line)
        if not m:
            continue
        key = m.group("k")
        val = m.group("v")
        # Trim surrounding quotes if present
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        # Parse array-shaped values like [a, b, c] — only used for
        # key_concepts today.
        arr = _ARRAY.match(val)
        if arr:
            inner = arr.group(1).strip()
            if inner:
                items = [
                    s.strip().strip('"').strip("'")
                    for s in inner.split(",")
                ]
                out[key] = [s for s in items if s]
            else:
                out[key] = []
        else:
            out[key] = val
    return out


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

    # Also regenerate app/curriculum.json for the app shell.
    emit_app_curriculum_json(csv_rows)
    return 0


# --- App curriculum.json sync ------------------------------------

# Subject labels + emojis preserved from the existing app/curriculum.json.
# These rarely change; hard-coded so the sync script doesn't need to
# preserve them by reading+merging the existing JSON.
SUBJECT_META = {
    "maths":     {"label": "Maths",     "emoji": "➗"},   # ➗
    "english":   {"label": "English",   "emoji": "\U0001F4D6"}, # 📖
    "science":   {"label": "Science",   "emoji": "\U0001F52C"}, # 🔬
    "history":   {"label": "History",   "emoji": "\U0001F3DB️"}, # 🏛️
    "geography": {"label": "Geography", "emoji": "\U0001F30D"}, # 🌍
    "computing": {"label": "Computing", "emoji": "\U0001F4BB"}, # 💻
}
AGE_RANGE_BY_YEAR = {1: "5-6", 2: "6-7", 3: "7-8", 4: "8-9", 5: "9-10", 6: "10-11"}

# Subject display order within a year
SUBJECT_ORDER = ["maths", "english", "science", "history", "geography", "computing"]

# Perspective ordering inside a concept (so 'identify' comes first, etc.)
PERSPECTIVE_ORDER = {"identify": 0, "sort": 1, "sequence": 2, "compose": 3, "apply": 4, "": 99}


def emit_app_curriculum_json(csv_rows: list[dict]) -> None:
    """Regenerate app/curriculum.json from the same filesystem scan.

    Only topics where BOTH content_status and animation_status are 'done'
    are surfaced to the app (the app only shows what's shippable).
    Todo rows stay in status.csv as the work queue but don't reach the
    app shell.

    Topic metadata (title, key_concepts) comes from the content.md's
    YAML frontmatter. Concept + perspective come from the same CSV row.
    """
    # Group done rows by year -> subject -> list of topics.
    grouped: dict[int, dict[str, list[dict]]] = {}
    for row in csv_rows:
        if row["content_status"] != "done" or row["animation_status"] != "done":
            continue
        year = int(row["year"])
        subject = row["subject"]
        slug = row["slug"]

        # Read the content.md's frontmatter for title + key_concepts.
        content_path = ROOT / "content" / f"year-{year}" / subject / f"{slug}.md"
        fm = parse_frontmatter(content_path)

        title = fm.get("topic") or slug
        key_concepts = fm.get("key_concepts") or []
        if isinstance(key_concepts, str):
            # Shouldn't happen with our parser, but guard anyway.
            key_concepts = [s.strip() for s in key_concepts.split(",") if s.strip()]

        topic_obj: dict = {
            "title": title,
            "slug": slug,
            "key_concepts": key_concepts,
        }
        # Only include concept + perspective if explicitly labelled
        # (Y3 Science for now; others are v1 flat — skip these fields
        # so app.js doesn't need to handle empty strings).
        if row["perspective"]:
            topic_obj["concept"] = row["concept"]
            topic_obj["perspective"] = row["perspective"]

        grouped.setdefault(year, {}).setdefault(subject, []).append(topic_obj)

    # Sort topics within each subject: by (concept, perspective-order, slug).
    # So "plants-identify" < "plants-sort" < "plants-sequence" < "rocks-identify".
    def topic_sort_key(t: dict) -> tuple:
        return (
            t.get("concept", t["slug"]),
            PERSPECTIVE_ORDER.get(t.get("perspective", ""), 99),
            t["slug"],
        )

    # Assemble the final JSON in the shape app.js expects.
    years_out = []
    for year in sorted(grouped.keys()):
        subjects_out = []
        for subject_name in SUBJECT_ORDER:
            if subject_name not in grouped[year]:
                continue
            topics = sorted(grouped[year][subject_name], key=topic_sort_key)
            meta = SUBJECT_META.get(subject_name, {"label": subject_name.title(), "emoji": ""})
            subjects_out.append({
                "name": subject_name,
                "label": meta["label"],
                "emoji": meta["emoji"],
                "topics": topics,
            })
        years_out.append({
            "year": year,
            "age_range": AGE_RANGE_BY_YEAR.get(year, ""),
            "subjects": subjects_out,
        })

    payload = {"years": years_out}

    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    with JSON_OUT.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total_topics = sum(len(s["topics"]) for y in years_out for s in y["subjects"])
    print(f"Wrote {JSON_OUT.relative_to(ROOT)}")
    print(f"  years:   {len(years_out)}")
    print(f"  topics:  {total_topics}")


if __name__ == "__main__":
    raise SystemExit(main())
