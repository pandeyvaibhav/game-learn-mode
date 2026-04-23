# GHCP Handoff — Year 3 Science Batch

**Two options:**
1. **§ 0 Combined batch prompt** — one prompt that builds all three topics in a single GHCP run, one commit per topic. Fastest path. Use this unless GHCP struggles with the length.
2. **§ 1–3 Individual prompts** — fallback if the batch prompt fails or GHCP needs to retry a single topic.

**Either way**, the agent must read [doc/topic-build-runbook.md](topic-build-runbook.md) and [animations/year-3/science/plants-functions-y3.html](../animations/year-3/science/plants-functions-y3.html) before writing anything. That's the pattern. Without it the output will revert to a quiz.

---

## § 0 — Batch prompt (recommended)

Paste the entire block below into Copilot Chat (Agent mode) after adding three `#file:` references:

```
#file:doc/topic-build-runbook.md
#file:animations/year-3/science/plants-functions-y3.html
#file:content/year-3/science/plants-functions-y3.md

You are building three Year 3 Science topic exemplars for the
game-learn-mode platform, in a single run.

RULES (non-negotiable)
- Read doc/topic-build-runbook.md in full before writing anything.
- Study animations/year-3/science/plants-functions-y3.html + its
  paired .md. This is the ONLY pattern. The old quiz-only templates
  in the Y3 folder are NOT the pattern.
- Build one topic at a time, in the listed order.
- Make ONE git commit per topic with message:
    feat(y3/science): hand-built {slug} exemplar
  Do NOT bundle multiple topics in one commit.
- After each topic, tick every box in runbook §7 acceptance checklist
  before moving on. If any box is unticked, fix it before committing.
- V1 palette only (see runbook §2.1). No new hex literals outside the
  palette except as explicitly-declared illustration tokens.
- Feedback: ✓ / ○ (circle-pause), not ✗. Error language is "Not quite",
  never "Wrong".
- postMessage hooks required: anim:ready / anim:attempt / anim:complete
  with topic = {slug}.

DELIVERABLE PER TOPIC
- animations/year-3/science/{slug}.html — self-contained, three
  sections: intro card, illustration, exercise. Five quest prompts.
- content/year-3/science/{slug}.md — one frontmatter block, 3 short
  paragraphs, mandatory ## Sources with ≥ 2 citations.

═══════════════════════════════════════════════════════════════════
TOPIC 1 — forces-magnets
═══════════════════════════════════════════════════════════════════

Archetype: tap-to-identify with a magnet + six objects.

Illustration SVG:
- A bar magnet at centre: left half red labelled "N", right half
  blue labelled "S", poles clearly coloured.
- Six objects arranged around the magnet, each a tappable
  <g class="part" data-part="{slug}">:
    1. paperclip       (metal, magnetic)
    2. iron-nail       (metal, magnetic)
    3. coin            (metal, NOT magnetic — copper/nickel)
    4. wooden-block    (not magnetic)
    5. rubber          (not magnetic)
    6. plastic-cup     (not magnetic)
- Flat-geometric. Declare extra tokens (--c-metal, --c-wood,
  --c-rubber, --c-plastic) at the top of <style>.

Five prompts (implement answer as an array where multiple parts are
valid, using `current.answer.includes(partName)`):
  1. "Tap a material the magnet will attract" → [paperclip, iron-nail]
  2. "Tap an object that is metal but NOT magnetic" → [coin]
  3. "Tap a material that is NOT magnetic" → [wooden-block, rubber, plastic-cup]
  4. "Tap the north pole of the magnet" → [n-pole]
  5. "Tap the south pole of the magnet" → [s-pole]

Content.md body (3 paragraphs):
  (1) Pushes and pulls are forces. Magnets pull certain metals without
      touching them.
  (2) Magnets attract iron and steel, not all metals. Every magnet has
      a north pole and a south pole. Opposite poles pull together; the
      same poles push apart.
  (3) "Open the game and tap each object to see if the magnet pulls it
      — then try the quest."

Sources:
  - UK National Curriculum — Science, Year 3: Forces and magnets
  - BBC Bitesize KS2 — "Forces and magnets"

COMMIT #1: feat(y3/science): hand-built forces-magnets exemplar

═══════════════════════════════════════════════════════════════════
TOPIC 2 — light-shadows
═══════════════════════════════════════════════════════════════════

NOTE: animations/year-3/science/light-shadows.html currently contains
a concatenated double-document (old quiz + older simulator). REPLACE
THE ENTIRE FILE with the new single 3-part structure.

Archetype: tap-to-identify with light / object / wall / shadow / glass.

Illustration SVG:
- Left: sun (yellow circle + rays), the light source.
- Between sun and object (slightly right): a clear-glass pane
  (transparent rectangle, very thin stroke, subtle fill).
- Middle: an opaque object (a ball or simple tree — pick one
  flat-geometric shape).
- Right: a wall (light-grey rounded rectangle) with a grey shadow
  shape projected onto it from the object.

Tappable parts:
  1. sun     (the light source)
  2. object  (the opaque body)
  3. shadow  (the grey shape on the wall)
  4. wall    (the surface the shadow falls on)
  5. glass   (transparent — light passes through)

Five prompts:
  1. "Tap the light source"                     → [sun]
  2. "Tap what blocks the light"                → [object]
  3. "Tap where the shadow forms"               → [wall, shadow]
  4. "Tap the object light passes through"      → [glass]
  5. "Tap the shadow"                           → [shadow]

Content.md body:
  (1) Light travels from a source in straight lines. We see things
      when light from a source reaches our eyes.
  (2) Shadows form when an opaque object blocks light from reaching
      a surface. Transparent materials (like glass) let light through,
      so they cast little or no shadow. Translucent materials let some
      light through.
  (3) "Open the game and tap each part of the scene to learn its role
      — then try the quest."

Sources:
  - UK National Curriculum — Science, Year 3: Light
  - BBC Bitesize KS2 — "Light and shadows"

COMMIT #2: feat(y3/science): hand-built light-shadows exemplar

═══════════════════════════════════════════════════════════════════
TOPIC 3 — rocks-fossils
═══════════════════════════════════════════════════════════════════

NOTE: animations/year-3/science/rocks-fossils.html is a quiz-only
vintage file — REPLACE it entirely.

Archetype: tap-to-identify labelled cross-section of Earth's crust.

Illustration SVG:
- Four horizontal bands, top to bottom:
    1. soil         — thin dark-brown band at top with grass tufts
    2. sedimentary  — layered tan/cream bands, with a fossil
                      silhouette (an ammonite spiral or dinosaur
                      bone outline) embedded
    3. igneous      — dark speckled grey block, with a magma chute
                      rising from below (suggesting volcanic origin)
    4. metamorphic  — banded swirl pattern (pink/grey) at the bottom

Tappable parts:
  1. soil
  2. sedimentary
  3. fossil          (shape inside the sedimentary layer)
  4. igneous
  5. metamorphic

Five prompts:
  1. "Tap the rock made when lava cools"         → [igneous]
  2. "Tap the rock that has layers"              → [sedimentary]
  3. "Tap the fossil"                            → [fossil]
  4. "Tap the rock changed by heat and pressure" → [metamorphic]
  5. "Tap where plants grow"                     → [soil]

Content.md body:
  (1) There are three main types of rock: igneous (formed when hot
      lava cools and hardens), sedimentary (formed from layers of
      sand, mud or shells pressed together over time), and
      metamorphic (older rock changed by heat or pressure deep
      underground).
  (2) Fossils are the preserved remains or impressions of plants
      and animals that lived long ago. They are usually found in
      sedimentary rock because the layers can trap them before
      they decay.
  (3) "Open the game and tap each layer to learn what it is — then
      try the quest."

Sources:
  - UK National Curriculum — Science, Year 3: Rocks
  - BBC Bitesize KS2 — "Rocks and fossils"

COMMIT #3: feat(y3/science): hand-built rocks-fossils exemplar

═══════════════════════════════════════════════════════════════════

END OF BATCH. Three topics, three commits. After this, the user will
play-test each with a real child before marking them protected via
tools/protected-exemplars.json.
```

After GHCP finishes, you will have three new commits on top of the
current branch, one per topic. Play-test each in the browser with a
child; if any fails, `git revert <commit>` just that one and
re-prompt GHCP using the individual prompt in §1–3 below.

---

## § 1 — Individual prompt — `forces-magnets`

```
You are building a topic exemplar for the game-learn-mode platform.

CONTEXT — read these first:
- doc/topic-build-runbook.md (the full methodology)
- animations/year-3/science/plants-functions-y3.html (the pattern)
- content/year-3/science/plants-functions-y3.md (byte-sized content shape)

The old quiz-style files in animations/year-3/ are NOT the pattern. Do not
reuse their structure. Your output must look like plants-functions-y3
with different subject content.

TASK — build this topic end-to-end:
  year:    3
  subject: science
  topic:   Forces and Magnets
  slug:    forces-magnets
  age:     7–8
  archetype: tap-to-identify (with a magnet + six objects)

ILLUSTRATION (the SVG inside the stage card):
  - A bar magnet in the centre: left half red labelled "N", right half
    blue labelled "S", both poles clearly coloured.
  - Six objects arranged in two rows of three around the magnet,
    each a tappable <g class="part" data-part="{slug}">:
      1. paperclip         (metal, magnetic)
      2. iron nail         (metal, magnetic)
      3. coin              (metal, NOT magnetic — copper/nickel)
      4. wooden block      (not magnetic)
      5. rubber            (not magnetic)
      6. plastic cup       (not magnetic)
  - Flat-geometric shapes only. Use the V1 palette + the bespoke
    colour tokens (--c-metal, --c-wood, --c-rubber, --c-plastic) defined
    at the top of <style>.

PROMPTS (exactly five, in PROMPTS array):
  1. "Tap a material the magnet will attract"      → answer: paperclip (or iron-nail — see NOTE)
  2. "Tap an object that is metal but NOT magnetic" → answer: coin
  3. "Tap a material that is NOT magnetic"         → answer: wood (or rubber / plastic)
  4. "Tap the north pole of the magnet"            → answer: n-pole
  5. "Tap the south pole of the magnet"            → answer: s-pole

NOTE on multi-valid answers: for prompts where several parts are valid
(e.g. any non-magnetic), accept any of the correct group. Easiest
implementation: change answer from a single slug to an array of slugs
and test with `current.answer.includes(partName)`.

CONTENT.md — content/year-3/science/forces-magnets.md:
  - One frontmatter block (not two).
  - 3 short paragraphs:
      (1) intro — pushes and pulls are forces; magnets pull some metals.
      (2) core — magnets attract iron and steel (not all metals); poles
          (north + south); same poles push, opposite poles pull.
      (3) italic pointer to the game.
  - Mandatory "## Sources":
      - UK National Curriculum — Science, Year 3: Forces and magnets
      - BBC Bitesize KS2 — "Forces and magnets"

ACCEPTANCE — tick every box in runbook §7 before declaring done:
  - Three visible sections (intro, illustration, exercise).
  - Only V1 palette + explicitly-declared illustration tokens.
  - ui-rounded font stack, clamp() sizes.
  - prefers-reduced-motion block present.
  - ✓ / ○ feedback language (NOT ✗ / harsh red).
  - aria-live on feedback region.
  - All interactive parts ≥ 44px.
  - Content.md has one frontmatter block + ## Sources.
  - postMessage hooks: anim:ready / anim:attempt / anim:complete.
```

---

## § 2 — Individual prompt — `light-shadows`

```
You are building a topic exemplar for the game-learn-mode platform.

CONTEXT — read these first:
- doc/topic-build-runbook.md
- animations/year-3/science/plants-functions-y3.html  (the pattern)
- animations/year-3/science/forces-magnets.html        (second exemplar, once built)

NOTE: animations/year-3/science/light-shadows.html currently contains a
concatenated double-document — an old quiz at the top and a richer
shadow-puppet simulator below. REPLACE THE ENTIRE FILE with the new
single 3-part structure. Do not keep the old content.

TASK:
  year:    3
  subject: science
  topic:   Light and Shadows
  slug:    light-shadows
  age:     7–8
  archetype: tap-to-identify with object-placement

ILLUSTRATION (the SVG inside the stage card):
  - Left: a sun (yellow circle + rays) as the light source.
  - Middle (slightly right): an opaque object — a simple house or tree
    or ball. Flat-geometric, one bespoke fill token.
  - Right: a wall (light grey rectangle) with a grey shadow shape
    projected onto it from the object.
  - Between light and object: optionally a clear-glass pane to
    demonstrate transparency.
  - Tappable parts:
      1. sun           (the light source)
      2. object        (the opaque body)
      3. shadow        (the grey shape on the wall)
      4. wall          (the surface the shadow falls on)
      5. glass         (transparent — no or faint shadow)

PROMPTS (five):
  1. "Tap the light source"                     → sun
  2. "Tap what blocks the light"                → object
  3. "Tap where the shadow forms"               → wall (or shadow — accept either)
  4. "Tap the object the light passes through"  → glass
  5. "Tap the shadow"                           → shadow

CONTENT.md:
  3 paragraphs:
    (1) light travels from a source; we see things when light
        reaches our eyes.
    (2) shadows form when an opaque object blocks light; transparent
        materials let light through (little/no shadow); translucent
        lets some light through.
    (3) italic pointer to the game.
  ## Sources:
    - UK National Curriculum — Science, Year 3: Light
    - BBC Bitesize KS2 — "Light and shadows"

ACCEPTANCE: same checklist as runbook §7.
```

---

## § 3 — Individual prompt — `rocks-fossils`

```
You are building a topic exemplar for the game-learn-mode platform.

CONTEXT — read these first:
- doc/topic-build-runbook.md
- animations/year-3/science/plants-functions-y3.html  (the pattern)

NOTE: The current animations/year-3/science/rocks-fossils.html is a
quiz-only vintage file — REPLACE it.

TASK:
  year:    3
  subject: science
  topic:   Rocks and Fossils
  slug:    rocks-fossils
  age:     7–8
  archetype: tap-to-identify labelled cross-section

ILLUSTRATION (the SVG):
  A cross-section of the Earth's crust, four horizontal bands top to bottom:
    1. soil       — thin dark-brown band at top with small grass tufts
    2. sedimentary — layered tan/cream bands with a fossil silhouette
                     embedded (dinosaur bone or ammonite)
    3. igneous    — dark speckled grey block, with a magma chute rising
                     from below suggesting volcanic origin
    4. metamorphic — banded swirl pattern (pink/grey) at the bottom

  Tappable parts:
    1. soil
    2. sedimentary
    3. fossil          (the shape within the sedimentary layer)
    4. igneous
    5. metamorphic

PROMPTS (five):
  1. "Tap the rock made when lava cools"        → igneous
  2. "Tap the rock that has layers"             → sedimentary
  3. "Tap the fossil"                           → fossil
  4. "Tap the rock changed by heat and pressure"→ metamorphic
  5. "Tap where plants grow"                    → soil

CONTENT.md:
  3 paragraphs:
    (1) the three types of rock — igneous (from cooled lava),
        sedimentary (from layers of sand/mud pressed together),
        metamorphic (changed by heat or pressure).
    (2) fossils are preserved remains of living things, mostly
        found in sedimentary rock because the layers trap them.
    (3) italic pointer to the game.
  ## Sources:
    - UK National Curriculum — Science, Year 3: Rocks
    - BBC Bitesize KS2 — "Rocks and fossils"

ACCEPTANCE: runbook §7.
```

---

## After all three are built

1. Open each in the browser: `http://127.0.0.1:3000/app/#/year/3/science/{slug}`
2. Play-test with a real child. **One minute per topic.** What do they tap first? Do they stick with it past prompt 3? Do they play again?
3. If any topic doesn't engage, fix it before moving to maths. Don't stack another subject on top of an unvalidated pattern.
4. Commit each topic in its own commit: `feat(y3/science): hand-built {slug} exemplar`.
5. When all three pass child-testing, start Maths prompts (see runbook §5.2).
