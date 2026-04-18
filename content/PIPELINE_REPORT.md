# Pipeline Run Report

## Latest Run
Date: 2025-07-27
Scope: year=1 --force --content-only

### Phase 1 — Content & Animations
- Topics processed: 21
- Content files written: 21 (all regenerated with fresh examples, questions, fun facts)
- Animation files written: 21 (quiz games with 10 questions each, age 5-6 appropriate)
- Skipped (already existed): 0 (--force flag: all overwritten)
- Safety review (S1) — passes / fails / blocked: 21/0/0 (content) + 21/0/0 (animations)
- Factual review (S2) — passes / fails / blocked: 21/0/0
- Playability review (S10) — passes / fails / blocked: 21/0/0
- Topics blocked by reviewers: none
- Errors: none

### Phase 2 — App Build
- UI Designer: skipped (--content-only)
- App Generator: skipped (--content-only)
- App entry point: app/index.html

### How to run the app
```
cd c:\VP\GH\game-learn-mode
python -m http.server 3000
open http://localhost:3000/app/
```

### Year 1 File Tree (21 topics)

#### Maths (6 topics)
- content/year-1/maths/counting-to-100.md | animations/year-1/maths/counting-to-100.html
- content/year-1/maths/addition-subtraction.md | animations/year-1/maths/addition-subtraction.html
- content/year-1/maths/shapes-2d-3d.md | animations/year-1/maths/shapes-2d-3d.html
- content/year-1/maths/measurement-length.md | animations/year-1/maths/measurement-length.html
- content/year-1/maths/measurement-weight.md | animations/year-1/maths/measurement-weight.html
- content/year-1/maths/ordinal-numbers.md | animations/year-1/maths/ordinal-numbers.html

#### English (5 topics)
- content/year-1/english/phonics-phase3.md | animations/year-1/english/phonics-phase3.html
- content/year-1/english/phonics-phase4.md | animations/year-1/english/phonics-phase4.html
- content/year-1/english/sentence-writing.md | animations/year-1/english/sentence-writing.html
- content/year-1/english/rhyme-poetry.md | animations/year-1/english/rhyme-poetry.html
- content/year-1/english/storytelling.md | animations/year-1/english/storytelling.html

#### Science (4 topics)
- content/year-1/science/animals-including-humans.md | animations/year-1/science/animals-including-humans.html
- content/year-1/science/seasonal-changes.md | animations/year-1/science/seasonal-changes.html
- content/year-1/science/everyday-materials.md | animations/year-1/science/everyday-materials.html
- content/year-1/science/plants-year1.md | animations/year-1/science/plants-year1.html

#### History (2 topics)
- content/year-1/history/changes-living-memory.md | animations/year-1/history/changes-living-memory.html
- content/year-1/history/significant-historical-events-y1.md | animations/year-1/history/significant-historical-events-y1.html

#### Geography (2 topics)
- content/year-1/geography/local-area.md | animations/year-1/geography/local-area.html
- content/year-1/geography/hot-cold-places.md | animations/year-1/geography/hot-cold-places.html

#### Computing (2 topics)
- content/year-1/computing/algorithms-instructions.md | animations/year-1/computing/algorithms-instructions.html
- content/year-1/computing/creating-digital-content-y1.md | animations/year-1/computing/creating-digital-content-y1.html

### Review Summary (Year 1)

#### S1 — Content Safety (content files)
All 21 content files reviewed against safety-policy.md §§1-11. No banned topics (§2), tone appropriate (§3), examples from approved contexts (§4), vocabulary year-appropriate (§5), sources present (§9). **All PASS.**

#### S2 — Factual Accuracy (content files)
All 21 content files verified against UK National Curriculum KS1 references. Key concepts, facts, and vocabulary confirmed accurate for ages 5-6. **All PASS.**

#### S1 — Content Safety (animation files)
All 21 animation files reviewed. No banned imagery (§6), no external URLs (§7), no PII collection (§8), no localStorage/sessionStorage, prefers-reduced-motion respected. **All PASS.**

#### S10 — Playability (animation files)
All 21 animation files reviewed against Year 1 bars: rules ≤3, items ≤8, reading ≤20 words, tap ≥44px.
- P1 rules count: all ≤3 ✅
- P2 on-screen items: all ≤8 (max 4 option buttons per question) ✅
- P3 reading load: all ≤20 words ✅
- P4 obvious first action: clear primary control on load ✅
- P5 tap size: min-height 44px on .opt-btn (56px on primary buttons) ✅
- P6 instructions: ≤2 lines ✅
- P7 kindness: ✓/✗ symbols, encouraging completion messages ✅

---

## Previous Run
Date: 2025-07-27
Scope: year=3 --force --content-only

### Phase 1 — Content & Animations
- Topics processed: 19
- Content files written: 19 (all regenerated with fresh examples, questions, fun facts)
- Animation files written: 19 (quiz QUESTIONS arrays regenerated with new questions)
- Skipped (already existed): 0 (--force flag: all overwritten)
- Safety review (S1) — passes / fails / blocked: 19/0/0 (content) + 19/0/0 (animations)
- Factual review (S2) — passes / fails / blocked: 19/0/0
- Playability review (S10) — passes / fails / blocked: 19/0/0
- Topics blocked by reviewers: none
- Errors: none

### Phase 2 — App Build
- UI Designer: skipped (--content-only)
- App Generator: skipped (--content-only)
- App entry point: app/index.html

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
All 19 animation files reviewed. No banned imagery (§6), no external URLs (§7), no PII collection (§8), no localStorage/sessionStorage, prefers-reduced-motion respected, child-baseline.css inlined. One fix applied: light-shadows.html `announce('Wrong.')` changed to `announce('Not quite.')` for P7 kindness compliance. **All PASS.**

### S10 — Playability (animation files)
All 19 animation files reviewed against Year 3 bars: rules ≤3, items ≤8, reading ≤25 words, tap ≥44px.
- P1 rules count: all ≤3 ✅
- P2 on-screen items: all ≤8 (max 4 option buttons per question) ✅
- P3 reading load: all ≤25 words ✅
- P4 obvious first action: clear primary control on load ✅
- P5 tap size: min-height 44px on .opt-btn (56px on primary buttons) ✅
- P6 instructions: ≤2 lines ✅
- P7 kindness: ✓/✗ symbols, "Correct!", "Answer:", encouraging completion messages ✅
- P8 clarity: text + colour feedback on all paths ✅
- P9 failure state: no blocking game-over; child can always continue ✅
- P10 time-to-interaction: immediate, no splash screens ✅
- P11 motion: prefers-reduced-motion guards on all animations ✅
- P12 reward loop: bounce animation + score tick on correct answers ✅
**All PASS.**

## Content Changes Applied (this run)
- 19 content .md files: intro paragraphs, examples, practice questions, and fun facts regenerated with fresh wording
- 18 animation .html files: QUESTIONS arrays replaced with new quiz items (multiplication-division-y3.html generates questions dynamically from times tables)
- 1 animation fix: light-shadows.html wrong-answer announcement softened from "Wrong" to "Not quite"

To regenerate a specific year/subject:
```
@orchestrator year=2 subject=maths
```

To force-overwrite existing files:
```
@orchestrator --force
```
