# Pipeline Run Report
Date: 2025-07-26
Scope: year=3 --force --content-only

## Phase 1 — Content & Animations
- Topics processed: 19
- Content files written: 19
- Animation files written: 19 (child-baseline.css injected)
- Skipped (already existed): 0 (--force flag: all overwritten)
- Safety review (S1) — passes / fails / blocked: 19/0/0 (content) + 19/0/0 (animations)
- Factual review (S2) — passes / fails / blocked: 19/0/0
- Topics blocked by reviewers: none
- Errors: none

## Phase 2 — App Build
- UI Designer: skipped (--content-only)
- App Generator: skipped (--content-only)
- App entry point: app/index.html

## How to run the app
```
cd c:\VP\GH\game-learn-mode
python -m http.server 8080
open http://localhost:8080/app/
```

## Year 3 File Tree (19 topics)

### Computing (2 topics)
- content/year-3/computing/sequences-selection.md | animations/year-3/computing/sequences-selection.html
- content/year-3/computing/data-information-y3.md | animations/year-3/computing/data-information-y3.html

### English (4 topics)
- content/year-3/english/conjunctions-clauses.md | animations/year-3/english/conjunctions-clauses.html
- content/year-3/english/narrative-writing-y3.md | animations/year-3/english/narrative-writing-y3.html
- content/year-3/english/poetry-imagery-y3.md | animations/year-3/english/poetry-imagery-y3.html
- content/year-3/english/report-writing-y3.md | animations/year-3/english/report-writing-y3.html

### Geography (2 topics)
- content/year-3/geography/volcanoes-earthquakes.md | animations/year-3/geography/volcanoes-earthquakes.html
- content/year-3/geography/mountains-y3.md | animations/year-3/geography/mountains-y3.html

### History (2 topics)
- content/year-3/history/stone-age-iron-age.md | animations/year-3/history/stone-age-iron-age.html
- content/year-3/history/ancient-egypt.md | animations/year-3/history/ancient-egypt.html

### Maths (5 topics)
- content/year-3/maths/place-value-1000.md | animations/year-3/maths/place-value-1000.html
- content/year-3/maths/multiplication-division-y3.md | animations/year-3/maths/multiplication-division-y3.html
- content/year-3/maths/fractions-y3.md | animations/year-3/maths/fractions-y3.html
- content/year-3/maths/perimeter-y3.md | animations/year-3/maths/perimeter-y3.html
- content/year-3/maths/statistics-bar-charts.md | animations/year-3/maths/statistics-bar-charts.html

### Science (4 topics)
- content/year-3/science/rocks-fossils.md | animations/year-3/science/rocks-fossils.html
- content/year-3/science/light-shadows.md | animations/year-3/science/light-shadows.html
- content/year-3/science/forces-magnets.md | animations/year-3/science/forces-magnets.html
- content/year-3/science/plants-functions-y3.md | animations/year-3/science/plants-functions-y3.html

## Review Summary

### S1 — Content Safety (content files)
All 19 content files reviewed against safety-policy.md §§1-11. No banned topics (§2), tone appropriate (§3), examples from approved contexts (§4), vocabulary year-appropriate (§5), Sources present (§9). **All PASS.**

### S2 — Factual Accuracy (content files)
All 19 content files verified against UK National Curriculum and standard KS2 references. Key concepts, facts, dates, and scientific terminology confirmed accurate. **All PASS.**

### S1 — Content Safety (animation files)
All 19 animation files reviewed. No banned imagery (§6), no external URLs (§7), no PII collection (§8), no localStorage/sessionStorage, prefers-reduced-motion respected, child-baseline.css inlined. **All PASS.**

## Content Changes Applied
- 6 content files fully rewritten to match agent templates (computing ×2, english ×4, geography ×2)
- 13 content files had Sources section appended
- 19 animation files had child-baseline.css rules injected (tap targets, font sizes, focus styles, motion safety, readability)

To regenerate a specific year/subject:
```
@orchestrator year=2 subject=maths
```

To force-overwrite existing files:
```
@orchestrator --force
```
