# Pipeline Run Report
Date: 2025-01-28
Scope: year=3

## Phase 1 — Content & Animations
- Topics processed: 19
- Content files written: 19
- Animation files written: 18
- Skipped (already existed): 1 (animations/year-3/science/light-shadows.html — animation pre-existed, content still generated)
- Errors: none

## Phase 2 — App Build
- UI Designer: skipped (scope filter active)
- App Generator: skipped (scope filter active)

## How to run the app
```
cd c:\VP\GH\game-learn-mode
python -m http.server 8080
open http://localhost:8080/app/
```

## File Tree
```
content/year-3/maths/place-value-1000.md
content/year-3/maths/multiplication-division-y3.md
content/year-3/maths/fractions-y3.md
content/year-3/maths/perimeter-y3.md
content/year-3/maths/statistics-bar-charts.md
content/year-3/english/narrative-writing-y3.md
content/year-3/english/poetry-imagery-y3.md
content/year-3/english/report-writing-y3.md
content/year-3/english/conjunctions-clauses.md
content/year-3/science/rocks-fossils.md
content/year-3/science/light-shadows.md
content/year-3/science/forces-magnets.md
content/year-3/science/plants-functions-y3.md
content/year-3/history/stone-age-iron-age.md
content/year-3/history/ancient-egypt.md
content/year-3/geography/volcanoes-earthquakes.md
content/year-3/geography/mountains-y3.md
content/year-3/computing/sequences-selection.md
content/year-3/computing/data-information-y3.md
animations/year-3/maths/place-value-1000.html
animations/year-3/maths/multiplication-division-y3.html
animations/year-3/maths/fractions-y3.html
animations/year-3/maths/perimeter-y3.html
animations/year-3/maths/statistics-bar-charts.html
animations/year-3/english/narrative-writing-y3.html
animations/year-3/english/poetry-imagery-y3.html
animations/year-3/english/report-writing-y3.html
animations/year-3/english/conjunctions-clauses.html
animations/year-3/science/rocks-fossils.html
animations/year-3/science/light-shadows.html (pre-existing)
animations/year-3/science/forces-magnets.html
animations/year-3/science/plants-functions-y3.html
animations/year-3/history/stone-age-iron-age.html
animations/year-3/history/ancient-egypt.html
animations/year-3/geography/volcanoes-earthquakes.html
animations/year-3/geography/mountains-y3.html
animations/year-3/computing/sequences-selection.html
animations/year-3/computing/data-information-y3.html
```

---

## Latest Run
Date: *(not yet run — seed files only)*
Scope: Seed / reference files

## Results
- Topics in curriculum: 96
- Content files written: 1 (seed)
- Animation files written: 2 (seed)
- Skipped (already existed): 0
- Errors: none

## Seed Files Generated

| File | Type | Status |
|---|---|---|
| `content/year-1/maths/counting-to-100.md` | Lesson content | ✅ seed |
| `animations/year-1/maths/counting-to-100.html` | Interactive animation | ✅ seed |
| `animations/year-3/science/light-shadows.html` | Interactive animation | ✅ seed |

## To Run the Full Pipeline

Open Claude Code and invoke the orchestrator agent:

```
@orchestrator generate all content
```

To regenerate a specific year/subject:
```
@orchestrator year=2 subject=maths
```

To force-overwrite existing files:
```
@orchestrator --force
```
