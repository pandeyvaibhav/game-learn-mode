# Topic Build Runbook — v1

| | |
|---|---|
| **Document** | `doc/topic-build-runbook.md` |
| **Version** | 1.0 |
| **Date** | 2026-04-23 |
| **Authors** | Vaibhav Pandey (Owner) · Claude Opus 4.7 (AI pair) |
| **Audience** | Any coding agent (GitHub Copilot, Claude Code, human contributor) building a topic for this platform. |
| **Reference implementation** | [animations/year-3/science/plants-functions-y3.html](../animations/year-3/science/plants-functions-y3.html) + [content/year-3/science/plants-functions-y3.md](../content/year-3/science/plants-functions-y3.md) — **study these first, they are the pattern.** |
| **Related** | [feature-design-child-visual-standard.md](feature-design-child-visual-standard.md) · [feature-design-animation-system.md](feature-design-animation-system.md) · [.github/agents/_shared/safety-policy.md](../.github/agents/_shared/safety-policy.md) |

---

## 0. Read first

Before you write a single line, open [plants-functions-y3.html](../animations/year-3/science/plants-functions-y3.html) and the paired [content.md](../content/year-3/science/plants-functions-y3.md). That file is the **only** pattern agents follow today. It was validated with a real 7-year-old who engaged with it unprompted. Your deliverable should look like that file with different subject content — *not* like the older quiz-only animations in the same folder.

If your output reads more like a developer's quiz than a child's game, you have missed the target.

---

## 1. The three-part topic model

Every topic ships **two files**:

- `content/year-{N}/{subject}/{slug}.md` — byte-sized verbal description, **≤ 25 lines of body + mandatory `## Sources`**.
- `animations/year-{N}/{subject}/{slug}.html` — one self-contained HTML file with **three visible sections in this order**:

| Section | What it is | Length target |
|---|---|---|
| **(a) Intro card** | 2–3 short paragraphs introducing the topic, bold-highlighting the key words the child will explore. | ≤ 60 words. |
| **(b) Illustration** | Interactive flat-geometric SVG of the topic (a plant, a fraction bar, a volcano, a timeline). Every named element is tappable and reveals a short label on any tap. Exploratory first, not gated behind an exercise. | 1 SVG ≤ 500 lines. |
| **(c) Exercise** | 5 rotating prompts (`Tap the part that…`, `Drag X to Y`, `Which of these is…`). Feedback is kind (check / circle-pause, never harsh ✗ / red flash). Progress dots. Completion card with stars + play-again. | Exactly 5 prompts. |

If the animation doesn't have all three sections, it doesn't match the pattern.

---

## 2. Visual rules (non-negotiable)

Every rule in this section is enforceable by reading the CSS and SVG without running the file. Violating any one of these means the file does not ship.

### 2.1 Palette — V1 Visual Standard tokens only

Use only these hex values (from [feature-design-child-visual-standard.md §4](feature-design-child-visual-standard.md)):

```
--c-bg:        #FFF9F2   warm off-white canvas (NEVER pure white)
--c-surface:   #FFFFFF   cards, raised surfaces
--c-border:    #E8DCC7   hairlines
--c-ink:       #1E1E2A   body text
--c-ink-muted: #5A5566   captions
--c-primary:   #4A5FDB   indigo — child's actions
--c-accent:    #FF8A3D   orange — highlights, mascot warm
--c-success:   #1FA66A   correct
--c-warn:      #E0A020   nearly / hint
--c-error:     #D8452B   not-quite (softened red)
--c-celebrate: #B24EE0   level-up moments
```

**No other hex literals in CSS.** Exceptions only for bespoke illustration colours (soil brown `#8B5A3C`, leaf green `#36C78F`, flower pink `#E76AA5`, pollen `#FFD166`) — define these as `--c-*` tokens at the top of your `<style>` block so they are traceable.

### 2.2 Typography

```
--font-body: ui-rounded, "SF Pro Rounded", "Nunito", "Segoe UI Variable", "Segoe UI", system-ui, sans-serif;
```

Fluid sizes via `clamp()`. Body 17–18px; prompts 19–22px; display 24–32px. No web-font downloads. No letter-spacing tricks.

### 2.3 Motion

Four easings (`--ease-out`, `--ease-in`, `--ease-both`, `--ease-bounce`), five durations (`--d-instant` 80ms, `--d-fast` 180ms, `--d-med` 320ms, `--d-slow` 560ms, `--d-ambient` 2400ms). Everything in a `@media (prefers-reduced-motion: reduce)` block must snap to `0.001ms`. Parity of information, not decoration.

### 2.4 Feedback language

- **Correct** → green `--c-success` + `✓` + text "Correct! — [specific thing]".
- **Not quite** → amber `--c-warn` + `○` (circle-pause, NEVER harsh ✗) + "Not quite — the answer is X."
- **Shame-free**: no "wrong", no "failed", no "incorrect", no red flash, no shake that feels punitive, no sound. When wrong, reveal the correct answer in green as a teaching moment.
- Every feedback must be announced via `aria-live="polite"`.

### 2.5 Tap targets

Every interactive element ≥ 44px (`--tap-min`). Primary controls ≥ 56px (`--tap-primary`). Keyboard operable — `Tab` to reach, `Enter` or `Space` to activate.

### 2.6 Mobile

Max content width 540px. `clamp()` on all font sizes. No horizontal overflow at 360px viewport. No fixed heights that break at small screens.

---

## 3. Content.md shape

```markdown
---
year: {N}
subject: {maths|english|science|history|geography|computing}
topic: {Human title}
slug: {kebab-case-slug}
key_concepts: [comma, separated, list]
age_range: "{e.g. 7-8}"
animation: ../../animations/year-{N}/{subject}/{slug}.html
---

# {Topic title} — Year {N} {Subject}

{Paragraph 1 — what this topic is about, 1–2 sentences, bold-highlight key words.}

{Paragraph 2 — the core idea in plain language, 1–2 sentences.}

{Paragraph 3 — italic pointer to the animation: "Open the game and tap each part to learn — then try the quest!"}

## Sources
- UK National Curriculum — {Subject, Year {N}}: {exact phrase from the curriculum document}
- {One trusted secondary source — BBC Bitesize, Oak Academy, DfE, Royal Society, etc.}
```

**Hard rules:**
- Frontmatter appears **exactly once**. Two `---\n…\n---` fences, never four. Concatenated-document files are a bug; if you see `---` more than twice in a content file, the file is broken and needs a clean rewrite.
- `## Sources` section is mandatory. ≥ 2 citations. Failure mode we already hit: 98/117 content files shipped without Sources and the pipeline claimed they passed §9. Don't be the next one.
- **No key-words tables, no duplicated quiz, no "Learning Checklist" checkboxes, no "Did You Know" trivia unless it belongs to the specific topic narrative.** The animation teaches. The .md contextualises.

---

## 4. Animation.html shape

Take the structure from [plants-functions-y3.html](../animations/year-3/science/plants-functions-y3.html) verbatim. The scaffolding — CSS tokens, section layout, Bix avatar, label-bubble, feedback bar, completion card, postMessage hooks — is reusable across topics. Only three things change per topic:

1. **The illustration SVG** — your new flat-geometric diagram. Parts are `<g class="part" data-part="{name}" role="button" tabindex="0" aria-label="…">`. Each part has a transparent `.hit` rect (≥ 44px tap target) and a `.visual` subgroup (the actual shape).
2. **The `PART_INFO` object** — maps each `data-part` name to a short label string.
3. **The `PROMPTS` array** — five `{ text, answer }` pairs driving the exercise.

Everything else — the shuffle, the quest logic, the feedback/reveal, the play-again flow, the postMessage calls — stays identical. Don't reinvent it; reuse it.

**postMessage contract (required):**
```js
parent.postMessage({ type: 'anim:ready',    topic: '{slug}' }, '*');
parent.postMessage({ type: 'anim:attempt',  topic: '{slug}', part: '{name}', correct: {bool} }, '*');
parent.postMessage({ type: 'anim:complete', topic: '{slug}', score: {n}, total: {n} }, '*');
```

These are the hooks the future `ProgressStore` (backlog P3) will consume. Don't skip them; they cost nothing now and unblock gamification later.

---

## 5. Year 3 topic plan — all 19 topics

Every Year 3 topic gets the full 3-part treatment. Use the archetype + illustration focus + exercise prompts below as the starting point; refine wording to sound natural for a 7-year-old.

**Status key:** ✅ done · 🟡 next · ⚪ queued

### 5.1 Science (4 topics — 1 done, 3 to go)

| Status | Topic (slug) | Archetype | Illustration focus | Exercise prompts (seed) |
|---|---|---|---|---|
| ✅ | `plants-functions-y3` | Tap-to-identify labelled diagram | Plant with visible soil, flower, leaves, stem, roots | "Tap the part that makes seeds" · "…catches sunlight" · "…drinks water" · "…holds the plant up" · "…feeds the roots" |
| 🟡 | `forces-magnets` | Tap-to-identify + simple force | Magnet (red/blue poles) + array of objects (paperclip, wooden block, rubber, iron nail, plastic cup, coin) | "Tap the material the magnet will attract" · "Tap the pole that attracts the other magnet's red end" · "Tap a push force" · "Tap a pull force" · "Tap the non-magnetic object" |
| 🟡 | `light-shadows` | Tap-to-identify + object-moves simulator | Light source on left, object in middle, wall + shadow on right; objects = ball/box/tree/glass | "Tap the light source" · "Tap where the shadow forms" · "Tap the object that makes the darkest shadow" · "Tap the transparent object (almost no shadow)" · "Tap what blocks the light" |
| 🟡 | `rocks-fossils` | Tap-to-identify labelled cross-section | Earth layers — sedimentary bands with a fossil, igneous from lava, metamorphic with swirled pattern | "Tap the rock made from lava" · "Tap the rock that has layers" · "Tap the fossil" · "Tap the oldest layer" · "Tap where a dinosaur bone might be found" |

### 5.2 Maths (5 topics)

| Status | Topic (slug) | Archetype | Illustration focus | Exercise prompts (seed) |
|---|---|---|---|---|
| ⚪ | `fractions-y3` | Fraction-fold | A rectangle (then a circle) split into equal parts; tap cells to shade | "Shade one half" · "Shade one quarter" · "Shade three quarters" · "Which shape shows two thirds?" · "Tap the shape where half is shaded" |
| ⚪ | `multiplication-division-y3` | Array-grouping | Grid of dots that can be highlighted in rows/columns; tap to group | "Tap 3 groups of 4 (=12)" · "Tap 2 × 5" · "Share 12 dots into 3 equal rows" · "Tap 4 groups of 2" · "Tap 5 × 3" |
| ⚪ | `perimeter-y3` | Count-the-sides labelled shape | A rectangle / square / L-shape / triangle with side lengths labelled | "Tap each side to count the perimeter of this rectangle" · "Which shape has perimeter 12 cm?" · "Find the missing side length" · "Which side is shorter?" · "Trace the perimeter with your finger" |
| ⚪ | `place-value-1000` | Base-10 block builder | Hundreds flats + tens rods + ones cubes; tap to build a number | "Build 235" · "How many hundreds in 700?" · "Tap the digit in the tens place of 428" · "Which number is shown?" · "Build the number that is 10 more than 340" |
| ⚪ | `statistics-bar-charts` | Read-a-chart | A real SVG bar chart with 4–5 categories (favourite fruits / weather days / etc.) | "Which is the tallest bar?" · "How many children chose apples?" · "Tap the least popular" · "What is the difference between X and Y?" · "Which two are the same?" |

### 5.3 English (4 topics)

| Status | Topic (slug) | Archetype | Illustration focus | Exercise prompts (seed) |
|---|---|---|---|---|
| ⚪ | `conjunctions-clauses` | Drag-to-match | Two sentence halves on screen + conjunction tokens (and, but, because, or, so) | "Join with the right word: *I wore a coat __ it was cold*" · "Which word shows a reason?" · "Which word shows a contrast?" · "Drag the conjunction that means adding more" · "Complete: *She was tired __ she kept going*" |
| ⚪ | `narrative-writing-y3` | Story-reorder | 5 story-beat cards (setting, characters, problem, action, resolution) as tappable tiles | "Put these story parts in order" · "Which part introduces the problem?" · "Which part is the setting?" · "Tap the beginning" · "Tap the ending" |
| ⚪ | `poetry-imagery-y3` | Tap-the-word | A short 4-line child-friendly poem with certain words visually tappable | "Tap the simile" · "Tap a word that describes a sound" · "Tap a word that paints a picture" · "Tap the rhyming pair" · "Tap the strongest verb" |
| ⚪ | `report-writing-y3` | Fact-vs-opinion sort | 5 statements as tappable tiles + two buckets (Fact / Opinion) | "Sort: *The Earth orbits the Sun*" · "Sort: *Dogs are the best pets*" · "Sort: *Water freezes at 0°C*" · "Sort: *This book is boring*" · "Sort: *London is in England*" |

### 5.4 History (2 topics)

| Status | Topic (slug) | Archetype | Illustration focus | Exercise prompts (seed) |
|---|---|---|---|---|
| ⚪ | `ancient-egypt` | Tap-to-identify cutaway | Pyramid cutaway: outer limestone, burial chamber, sarcophagus, Nile alongside, pharaoh figure, scribe | "Tap the pharaoh" · "Tap where the mummy was placed" · "Tap the river that watered the fields" · "Tap the pyramid's burial chamber" · "Tap the person who wrote things down" |
| ⚪ | `stone-age-iron-age` | Story-reorder timeline | 5 era-cards: hunter-gatherer, farming village, bronze tools, iron tools, hillfort | "Put the eras in order (oldest first)" · "Tap the era where people first farmed" · "Tap when iron tools appeared" · "Tap the hunter-gatherer era" · "Which came first, bronze or iron?" |

### 5.5 Geography (2 topics)

| Status | Topic (slug) | Archetype | Illustration focus | Exercise prompts (seed) |
|---|---|---|---|---|
| ⚪ | `mountains-y3` | Labelled cross-section + slider | Mountain cross-section: foothills, forest zone, tree line, snow line, peak; slider changes altitude highlight | "Tap where trees stop growing" · "Drag the slider to the snow line" · "Tap the foothills" · "Which zone is warmest?" · "Tap the peak" |
| ⚪ | `volcanoes-earthquakes` | Tap-to-identify cutaway | Volcano cutaway: magma chamber, vent, crater, lava flow, ash cloud | "Tap the magma chamber" · "Tap where lava comes out" · "Tap the ash cloud" · "Tap the vent" · "Tap the hottest part" |

### 5.6 Computing (2 topics)

| Status | Topic (slug) | Archetype | Illustration focus | Exercise prompts (seed) |
|---|---|---|---|---|
| ⚪ | `sequences-selection` | Sequence-builder | 5 step-tiles for a real task (make a sandwich / get dressed / cross road safely); drag to reorder | "Put the steps to make a sandwich in order" · "Which step comes first?" · "Tap the missing step" · "Tap the last step" · "Put the bedtime routine in order" |
| ⚪ | `data-information-y3` | Tap-to-classify | Mixed tiles (numbers, words, a chart, a word list, a raw measurement, a conclusion); two buckets: Data / Information | "Tap the raw data" · "Tap the information (data with meaning)" · "Sort: 23, 19, 21, 20" · "Sort: *Average temperature was 21°C*" · "Tap what needs interpreting" |

### 5.7 Execution order

**One subject at a time. Finish a subject before starting the next.** This avoids half-built subjects and lets each subject's pattern harden before the next.

1. **Science** (3 topics remaining) — validates labelled-diagram + simulator pattern across biology, physics, earth science. Ship: `forces-magnets`, `light-shadows`, `rocks-fossils`.
2. **Maths** (5 topics) — validates non-diagram archetypes: fraction-fold, array-grouping, read-a-chart, base-10 blocks. Higher variety; expect each one to need slightly different interaction code.
3. **English** (4 topics) — validates text-first archetypes: drag-to-match, reorder, tap-the-word, sort-into-buckets.
4. **History** (2), **Geography** (2), **Computing** (2) — last, reuse archetypes proven in earlier subjects (cutaways, timelines, sequence-builders, classifiers).

After each subject: play-test at least one topic with a real child. If the child doesn't engage, **stop and iterate** — don't ship the next subject on top of an unvalidated pattern.

---

## 6. The build loop (per topic)

1. **Read** the reference file `plants-functions-y3.html` until you understand the three sections, the SVG part pattern, and the quest logic.
2. **Copy** the file to your target path (`animations/year-{N}/{subject}/{slug}.html`).
3. **Swap the illustration.** Replace the plant SVG with your topic's diagram. Keep `<g class="part">` pattern. Keep tap targets ≥ 44px.
4. **Swap `PART_INFO` + `PROMPTS`.** Five prompts. Each answer must map to a `data-part` in your SVG.
5. **Rewrite the intro card** to 2–3 short paragraphs about your topic.
6. **Rewrite the content.md** to the §3 shape. Three paragraphs. Mandatory `## Sources`.
7. **Self-check** against the acceptance list in §7.
8. **Test with a real child.** A real child. Not your idea of a child.
9. **Iterate** until the child engages for ≥ 5 minutes unprompted and taps "play again" at least once.

---

## 7. Acceptance checklist

Before you commit, tick every box by reading your file. Agents that skip this are the reason 98 files shipped without `## Sources`.

**Structure**
- [ ] `content.md` has exactly two `---` fences. Just one frontmatter block.
- [ ] `content.md` ends with `## Sources` section with ≥ 2 citations (UK National Curriculum + one trusted secondary).
- [ ] `content.md` body ≤ 25 lines (excluding frontmatter and Sources).
- [ ] `animation.html` is a single self-contained HTML document. One `<!DOCTYPE html>`. One `<html>`. One `<body>`.
- [ ] Three visible sections in the animation: intro card, illustration, exercise. In that order.

**Visual standard**
- [ ] No hex literals outside the V1 palette in CSS, except explicitly-defined illustration-specific `--c-*` tokens.
- [ ] Body font uses `ui-rounded` stack.
- [ ] `@media (prefers-reduced-motion: reduce)` block present and kills all transitions.
- [ ] Feedback uses `✓` / `○` (circle-pause), never `✗`. Error language is "Not quite", never "Wrong".
- [ ] `aria-live="polite"` on the feedback region.
- [ ] All interactive elements ≥ 44px; primary ≥ 56px.
- [ ] Max content width 540px. No horizontal overflow at 360px viewport.

**Behaviour**
- [ ] Every illustration part is tappable and reveals a label bubble — *before* the quest starts (exploratory).
- [ ] Quest has exactly 5 prompts, shuffled per play.
- [ ] On wrong answer: part shakes softly, correct part reveals in green, amber "not quite" feedback.
- [ ] Completion card shows 1/2/3 stars by score; `playAgain` resets state.
- [ ] `postMessage` calls fire for `anim:ready`, `anim:attempt`, `anim:complete` with the topic slug.

**Content**
- [ ] No banned topics (safety-policy §2).
- [ ] Year-appropriate vocabulary (safety-policy §5).
- [ ] Facts verifiable from the cited Sources. Nothing invented.

If any box is unticked, the file is not ready to commit.

---

## 8. Hard "don't"s

- **Don't let the existing pipeline/orchestrator re-run over a hand-built exemplar under `--force`.** Those agents currently produce quiz-only output and will destroy your work. Backlog X6 (diff-before-regen guard) exists to fix this; until then, keep hand-built files out of `--force` runs.
- **Don't copy-paste old quiz template.** The old Y3 quiz HTML is in the repo; don't use it as a base. Start from `plants-functions-y3.html`.
- **Don't inflate the content.md.** "More content" is not "better teaching". The animation is the lesson; the .md is 3 paragraphs of context.
- **Don't use ASCII / monospace "diagrams".** An ASCII plant in a `<pre>` block is what we're moving *away* from. If the answer is a diagram, it must be an SVG.
- **Don't skip real-child validation.** Passing S1/S2/S10 is necessary, not sufficient. A file can pass all three and still be unplayable. The final judge is a child.
- **Don't bypass `## Sources`.** If you don't have two citations, you don't have a lesson, you have a creative writing exercise.

---

## 9. Prompt template for agent handoff

Paste this into GitHub Copilot Workspace / Claude Code / any coding agent when asking for a new topic build:

```
You are building a topic exemplar for the game-learn-mode platform.

CONTEXT
- Read doc/topic-build-runbook.md in full before writing anything.
- Read animations/year-3/science/plants-functions-y3.html + content/year-3/science/plants-functions-y3.md.
  These are the ONLY pattern. Your output must look like these two files with different subject content.
- The old Y3 quiz-only HTML files are NOT the pattern. Do not reuse their structure.

TASK
Build one topic end-to-end:
  year: {N}
  subject: {subject}
  topic: {human title}
  slug: {kebab-case}
  archetype: {one of — tap-to-identify / fraction-fold / drag-to-match / story-reorder / labelled-slider / sequence-builder}
  illustration focus: {what the SVG should show}
  5 exercise prompts: {list them explicitly}

DELIVERABLES
1. animations/year-{N}/{subject}/{slug}.html — self-contained, three sections (intro, illustration, exercise), V1 palette, Bix avatar, postMessage hooks.
2. content/year-{N}/{subject}/{slug}.md — one frontmatter block, 3 short paragraphs, mandatory ## Sources with ≥ 2 citations.

ACCEPTANCE
Tick every box in doc/topic-build-runbook.md §7 before declaring done.
Do not commit if any box is unticked.
```

Fill in the {placeholders} from §5 for whichever of the five remaining exemplars you are building next.

---

## 10. Change log

| Version | Date | Authors | Change |
|---|---|---|---|
| 1.0 | 2026-04-23 | Vaibhav Pandey · Claude Opus 4.7 | Initial runbook. Extracted the method from the first validated hand-built exemplar (`plants-functions-y3`). Codifies the 3-part model, V1 visual rules, content.md shape, acceptance checklist, and agent-handoff prompt template. |
