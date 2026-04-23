# GHCP Handoff — Year 3 Science Batch

Three ready-to-paste prompts for GitHub Copilot Workspace (or Claude Code, or any coding agent that can read the repo). Do them **in order**. After each one, open the result in the browser, play-test with a child, and iterate if the child doesn't engage before moving to the next.

The agent must read [doc/topic-build-runbook.md](topic-build-runbook.md) and [animations/year-3/science/plants-functions-y3.html](../animations/year-3/science/plants-functions-y3.html) before writing anything. That's the pattern. Without it the output will revert to a quiz.

---

## Prompt 1 — `forces-magnets`

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

## Prompt 2 — `light-shadows`

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

## Prompt 3 — `rocks-fossils`

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
