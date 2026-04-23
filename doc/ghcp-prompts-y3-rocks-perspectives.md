# GHCP Handoff — Year 3 Science: Rocks-Concept Perspective Batch

The "explode one concept into multiple perspectives" experiment. The **Rocks** concept already has one perspective topic live — `rocks-fossils` (identify). This batch adds the other three perspectives so a child can encounter Rocks from four angles:

| Perspective | Topic | Status |
|---|---|---|
| identify | `rocks-fossils` | ✅ shipped + child-validated |
| **sort** | **`rock-properties-sort`** | 🟡 this batch |
| **sequence** | **`fossil-formation`** | 🟡 this batch |
| **compose** | **`soil-composition`** | 🟡 this batch |

After the child plays all four in one session, we know whether the multiple-perspectives framework holds (see [feedback_multiple_perspectives.md](../../../../Users/vaibh/.claude/projects/c--VP-GH-game-learn-mode/memory/feedback_multiple_perspectives.md) memory).

---

## § 0 — Batch prompt

Paste the entire block into Copilot Chat (Agent mode) with these three `#file:` references at the top:

```
#file:doc/topic-build-runbook.md
#file:animations/year-3/science/plants-functions-y3.html
#file:content/year-3/science/plants-functions-y3.md

You are building three Year 3 Science topic exemplars for the
game-learn-mode platform, in a single run.

These three topics all explore the SAME concept (Rocks) from three
DIFFERENT cognitive perspectives. The existing identify-perspective
(rocks-fossils) already ships; you are adding sort, sequence, and
compose.

RULES (non-negotiable)
- Read doc/topic-build-runbook.md in full before writing anything.
- Study animations/year-3/science/plants-functions-y3.html + its
  paired .md. This is the ONLY pattern. The older quiz-only vintage
  templates elsewhere in Y3 are NOT the pattern.
- Build one topic at a time, in the listed order.
- Make ONE git commit per topic:
    feat(y3/science): hand-built {slug} exemplar (rocks {perspective})
- Tick every box in runbook §7 before committing.
- V1 palette only (runbook §2.1). Declare any illustration-specific
  colour as a --c-* token at the top of <style>.
- Feedback: ✓ / ○ (circle-pause), not ✗. Error language "Not quite".
- postMessage hooks: anim:ready / anim:attempt / anim:complete.

DELIVERABLE PER TOPIC
- animations/year-3/science/{slug}.html — 3-section self-contained
  file: intro card, illustration, exercise. Exactly five quest
  prompts.
- content/year-3/science/{slug}.md — one frontmatter block, 3 short
  paragraphs, mandatory ## Sources with >= 2 citations.

IMPORTANT: the existing `rocks-fossils` topic file (the identify
perspective) is PROTECTED. Do NOT modify it. Do NOT re-generate it.
X6 guard will block the commit if you do.

═══════════════════════════════════════════════════════════════════
TOPIC 1 — rock-properties-sort (Rocks concept · SORT perspective)
═══════════════════════════════════════════════════════════════════

Archetype: drag-to-bucket. The child sorts 6 rock examples into
property buckets.

Illustration SVG:
- Top half: six rock illustrations laid out in a row. Each is a
  tappable <g class="part" data-part="{slug}"> that the child can
  drag. Use flat-geometric rounded shapes with bespoke --c-* tokens.
    1. granite       (speckled grey, hard)
    2. sandstone     (warm tan, rough layers)
    3. pumice        (pale grey, visible holes / porous look)
    4. marble        (smooth white with pink veins)
    5. slate         (dark grey-blue, flat layers)
    6. chalk         (soft off-white, crumbly look)
- Bottom half: THREE buckets side-by-side with labels:
    - "Hard"    (⬛ icon)
    - "Soft"    (🟤 lighter icon)
    - "Porous"  (💧 droplet icon — holds water)

Child drags each rock into a bucket. Correct mapping (source: KS2):
- Hard:   granite, marble, slate
- Soft:   chalk
- Porous: sandstone, pumice

PROMPTS array (the text the prompt bar shows — since this is a
sorting task rather than tap-identify, each prompt asks about ONE
rock and the "answer" is the bucket slug):
  1. "Where does granite belong?"   → ["hard"]
  2. "Where does chalk belong?"     → ["soft"]
  3. "Where does pumice belong?"    → ["porous"]
  4. "Where does slate belong?"     → ["hard"]
  5. "Where does sandstone belong?" → ["porous"]

Interaction detail: the child can drag a rock onto a bucket OR tap
the rock then tap the bucket (keyboard + switch accessible). On
correct drop: bucket briefly highlights --c-success + bounce.
On wrong drop: rock bounces back to its original position, bucket
flashes --c-warn amber, feedback bar says "Not quite — try again".

CONTENT.md body (3 paragraphs):
  (1) Not all rocks are the same. Some are hard (you can't scratch
      them easily). Some are soft (they crumble between your
      fingers). Some are porous — tiny holes let water soak in.
  (2) Granite, marble, and slate are hard. Chalk is soft — it's
      what's in the white sticks of chalk you might draw with!
      Sandstone and pumice have lots of tiny holes, so water can
      soak right through.
  (3) "Open the game and drag each rock into the right group."

Sources:
  - UK National Curriculum — Science, Year 3: Rocks
  - BBC Bitesize KS2 Science — "Properties of rocks"

COMMIT #1: feat(y3/science): hand-built rock-properties-sort exemplar (rocks sort)

═══════════════════════════════════════════════════════════════════
TOPIC 2 — fossil-formation (Rocks concept · SEQUENCE perspective)
═══════════════════════════════════════════════════════════════════

Archetype: sequence-builder. The child reorders 5 scene cards into
the correct order that shows how a fossil forms over millions of
years.

Illustration SVG:
- Main stage: a wide horizontal "timeline track" across the middle.
  Empty slot 1 | Empty slot 2 | Empty slot 3 | Empty slot 4 | Empty slot 5
- Below the track: five scene-card illustrations (shuffled):
    1. alive        — a friendly ammonite or simple dinosaur
                      swimming / walking
    2. dies         — the creature lying still (no blood, no
                      violence — just stopped moving, eyes closed)
    3. buried       — same creature under sand/mud layers
    4. pressed      — sand/mud becomes rock, creature outline
                      visible inside
    5. discovered   — a friendly palaeontologist with a brush
                      uncovering the fossil
- Each card has a number-less space on top (the child fills it).
- Tappable parts are the five cards (data-part="alive" etc).
- When dropped onto the track, the card snaps to the slot and the
  slot shows a number badge.

PROMPTS (sequence perspective — ask the child to place each stage
in order — so each prompt is actually "place the NEXT card"):
  1. "Tap the very first stage — the creature is alive"    → ["alive"]
  2. "Tap what happens next — the creature dies"           → ["dies"]
  3. "Tap what happens next — it gets buried in layers"    → ["buried"]
  4. "Tap what happens next — layers squash into rock"     → ["pressed"]
  5. "Tap the last stage — someone finds the fossil"       → ["discovered"]

After all 5 placed correctly the timeline shows the full sequence
with gentle arrow transitions between cards.

Safety: keep "dies" illustration neutral — creature simply lying
still with closed eyes. No injury, no blood, no graphic detail.

CONTENT.md body:
  (1) Fossils are the remains or shapes of living things that are
      trapped inside rock. They can be millions of years old!
  (2) A fossil forms when an animal or plant dies and is quickly
      buried by mud or sand. Over a very long time, more and more
      layers press down, and the soft parts disappear but the hard
      shape stays in the rock. Later, people dig it up.
  (3) "Open the game and put the stages in the right order — from
      alive all the way to discovered."

Sources:
  - UK National Curriculum — Science, Year 3: Rocks (fossils
    formation)
  - Natural History Museum learning resources — "How do fossils
    form?" (KS2)

COMMIT #2: feat(y3/science): hand-built fossil-formation exemplar (rocks sequence)

═══════════════════════════════════════════════════════════════════
TOPIC 3 — soil-composition (Rocks concept · COMPOSE perspective)
═══════════════════════════════════════════════════════════════════

Archetype: tap-to-build. The child taps four ingredient cards to
add them into a "soil jar" illustration. When all four are added,
the jar is full of layered soil and gives a satisfying completion
animation.

Illustration SVG:
- Centre: a large glass jar (flat-geometric — rounded rectangle with
  transparent-style border, subtle --c-glass fill).
- Around the jar: four ingredient cards, each tappable:
    1. rock-bits    (small grey/tan fragments)
    2. rotted-plants (brown leaves + twigs)
    3. water         (blue droplets)
    4. air           (small white circles / bubbles)
- Inside the jar: initially empty. As each ingredient is added
  (tapped), a layer or sprinkle of that ingredient fills a portion
  of the jar:
    - rock-bits    → bottom third (brown/grey speckled layer)
    - rotted-plants→ middle third (dark brown)
    - water        → tiny droplets throughout the existing layers
    - air          → small bubbles in the layers
- When all 4 added: jar is "full of soil", a small sprout emerges
  from the top (celebration moment).

PROMPTS (compose perspective — ask the child what's in soil in
several ways):
  1. "Tap to add rock bits to the jar"          → ["rock-bits"]
  2. "Tap to add rotted plants and leaves"      → ["rotted-plants"]
  3. "Tap to add water"                         → ["water"]
  4. "Tap to add air"                           → ["air"]
  5. "Which ingredient gives soil its crumbly feel?" → ["rotted-plants"]

Interaction detail: each ingredient can only be added once. Tapping
an already-added ingredient gives a gentle "already there!" nudge
(warn colour + circle-pause icon). After all 4 ingredients are in,
the quest moves to prompt 5 which is a recall question.

CONTENT.md body:
  (1) Soil is what plants grow in. It looks like just brown dirt,
      but it's actually a mixture of four things.
  (2) Soil has **rock bits** (from rocks breaking down over a long
      time), **rotted plants** (leaves and twigs that have broken
      down), **water**, and **air**. Plants need all four to grow
      well!
  (3) "Open the game and build soil by adding each ingredient to
      the jar."

Sources:
  - UK National Curriculum — Science, Year 3: Rocks (soils from
    rocks and organic matter)
  - BBC Bitesize KS2 Science — "What is soil?"

COMMIT #3: feat(y3/science): hand-built soil-composition exemplar (rocks compose)

═══════════════════════════════════════════════════════════════════

END OF BATCH. Three topics, three commits. After this, the user
will play-test all four Rocks topics in one session with a child
to validate the multiple-perspectives framework.

status.csv rows to update after each commit:
  rock-properties-sort  → content_status=done, animation_status=done
  fossil-formation      → content_status=done, animation_status=done
  soil-composition      → content_status=done, animation_status=done

(If you can write to curriculum/status.csv, do so as the last step
of each commit. If you cannot, leave the rows as-is and the user
will re-run tools/seed_status_csv.py.)
```

---

## After GHCP is done

1. **Play-test all four Rocks topics with the child, in one sitting, in order:**
   ```
   http://localhost:3000/app/#/year/3/science/rocks-fossils         (identify)
   http://localhost:3000/app/#/year/3/science/rock-properties-sort  (sort)
   http://localhost:3000/app/#/year/3/science/fossil-formation      (sequence)
   http://localhost:3000/app/#/year/3/science/soil-composition      (compose)
   ```
   **Goal signal:** does the child do all 4 in one session, or bounce after the 2nd? If all 4, the perspectives framework holds and we generalise it. If they bounce after the 2nd, we've found the ceiling and adjust.

2. **If all 4 pass the play-test:**
   - Update `tools/protected-exemplars.json` — add entries for the 3 new slugs, mark validated_by "child played all 4 rocks perspectives", run `python tools/guard_exemplar.py update <slug>` for each.
   - Re-seed `curriculum/status.csv` (`python tools/seed_status_csv.py`).
   - Draft the Plants-concept perspective batch prompt (`plant-growth-needs`, `plant-lifecycle`, `water-transport`) — same shape as this file.
   - Then Forces concept, then Light concept. Y3 Science complete (16 topics) in ~4 GHCP batches.

3. **If the framework fails** (child bounces after 2–3 perspectives):
   - Reduce perspectives per concept from 4 → 2 (identify + one other).
   - Update `curriculum.md` Y3 Science section to drop the failed perspectives.
   - Update the runbook §5.7 execution order.
   - Learn which cognitive modes carry and which don't for this age.
