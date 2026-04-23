# GHCP Handoff — Content Studio v1 (read-only dashboard)

Single prompt for GitHub Copilot (Agent mode). Builds the v1 operator dashboard specified in [feature-design-content-studio.md](feature-design-content-studio.md). v1 is **read-only**; no agent triggering, no file writes from the UI.

---

## How to use

Open Copilot Chat in Agent mode. Add these context references:

```
#file:doc/feature-design-content-studio.md
#file:doc/architecture.md
#file:curriculum/status.csv
#file:tools/protected-exemplars.json
#file:animations/_shared/child-baseline.css
```

Then paste the § 0 prompt below.

---

## § 0 — Prompt

```
You are building the Content Studio v1 for the game-learn-mode
platform. This is an OPERATOR-FACING DASHBOARD (not a child
surface). It visualises the state of the content pipeline
described in doc/architecture.md and doc/feature-design-content-studio.md.

HARD RULES

- Read doc/feature-design-content-studio.md in full before
  writing any code. It is the spec. Where this prompt and the
  design doc disagree, the design doc wins.
- No CDNs. No npm. No build step. Vanilla HTML + CSS + JS only.
- Single page application. All files live in studio/.
- Read-only v1 — the dashboard MUST NOT write to any file.
  Specifically: no POST-like behaviour, no fetch calls with
  mutating methods, no localStorage writes (reading is fine for
  cached last-fetch timestamps). Clicking "Rebuild" or similar
  is a v1.5 concern — omit those buttons entirely in v1.
- No external network. Every fetch() URL must be a relative
  path under the repo root. No "https://..." anywhere.
- Adult operator UI, not child-facing:
  - Font: standard system-ui stack (NOT ui-rounded).
  - Body text 13-14px, labels 11px, headings 18-20px.
  - Denser layout, max-width 1200px.
  - Keyboard-first: Tab navigation, Enter to drill, Esc to
    close drawer.
  - No Bix, no celebration animations, no bounce easings.
- Use V1 palette tokens from animations/_shared/child-baseline.css
  (the same semantic tokens — --c-bg, --c-success, etc.), but
  import them only by re-declaring in studio.css (do NOT link
  child-baseline.css; keep studio self-contained).
- Respect prefers-reduced-motion — transitions snap when set.
- Respect prefers-color-scheme: dark — auto dark mode for the
  studio (not opt-in like the child shell).

DELIVERABLES

Create these four files:

  studio/index.html   — the single-page shell
  studio/studio.css   — all styling
  studio/studio.js    — fetch + parse + render + keyboard nav
  studio/README.md    — how to open it + panel descriptions

LAYOUT (see design doc §5 for the sketch)

Top to bottom:

1. Header bar
   - "Game Learn · Content Studio" + tiny subtitle "operator dashboard"
   - Right: [Sync] button (reloads data — v1 just re-fetches),
            [⚙] icon (placeholder — no menu in v1)

2. Summary strip (single row, ~40px tall)
   - Total live topics (content_status=done AND animation_status=done)
   - Todo count (either status != done)
   - Validated count (protected=yes)
   - "Last build: Xh ago" (from newest file mtime under animations/
     or content/ — client-side read of status.csv content_sha change
     is not possible, so use 'last commit' once it's available via a
     server-side helper OR omit the timestamp entirely if no signal
     is reachable in pure browser-only reads)

3. Year × Subject grid
   - 6 rows (Y1-Y6) × 6 columns (maths, english, science, history,
     geography, computing).
   - Each cell: subject emoji + topic count + inline dots
     (one dot per topic, coloured per status legend).
   - Click a cell → opens the drawer below.
   - Arrow keys navigate cells; Enter opens drawer.

4. Concept drawer (appears below the grid when a cell is selected)
   - Header: "Y{N} · {subject} · {N_live} topics live · {N_todo} todo"
   - Groups topics by concept. Collapsible concept headers.
   - Each perspective-row shows:
       status-icon  slug  perspective-badge  lock-if-protected  validated-date
   - "Open in app" link per row: opens
       /app/#/year/{N}/{subject}/{slug} in a new tab.
   - "View content.md" link: opens content/year-{N}/{subject}/{slug}.md
       in a new tab (served as plain text).
   - "View animation.html" link: opens the animation file in a new
       tab.

5. Activity feed (bottom)
   - Last 10 meaningful commits touching content/ or animations/.
   - v1: since the browser can't run git commands, this feed reads
     from curriculum/status.csv's last_reviewed + validated_with_child
     columns instead — one row per topic with a date, sorted newest
     first, top 10. Call the section "Recent topic activity".
     Flag v1.5 as "to be powered by studio/data/activity.json once
     the runner exists".

DATA CONTRACTS (fetch these at load + on Sync click)

  curriculum/status.csv         — parse as 12-col CSV
  curriculum/curriculum.md      — best-effort parse for concept
                                  headings under Year 3 Science
                                  (other years fall back to slug-
                                  as-concept); extract "Concept:
                                  X" pattern on '####' lines only
  tools/protected-exemplars.json — parse as JSON; map slug ->
                                  {validated_date, reason}
  content/PIPELINE_REPORT.md    — optional; if present, render its
                                  markdown verbatim in a collapsed
                                  "last pipeline run" card below
                                  the activity feed. Do not fail
                                  if absent.

CSV PARSER — ~30 lines of vanilla JS. Split on newlines, then on
',' respecting simple quoting is not required for our CSV (we do
not embed commas in any field). Handle the UTF-8 BOM defensively.

STATE LEGEND (icon → status)
  ● done, both files       (--c-success)
  ◐ todo                   (--c-ink-muted)
  🔒 protected              (--c-accent)
  ✓ validated with child   (--c-celebrate)
  ⚠ needs iteration         (--c-warn) — shown only when there
                                         is evidence (in v1 this
                                         is purely a stub; feed
                                         a static empty list)
  ❌ blocked                 (--c-error)

A single topic's cell dot colour takes the most severe applicable
status: protected+validated shows as a compound icon
"✅🔒✓" in the drilled drawer; in the grid dot, protection wins
(orange dot) then validation (purple dot) then done (green).

INTERACTIONS (keyboard-first, all mouse-equivalent)

  Tab / Shift+Tab   — move between cells and rows
  Enter / Space     — activate (open drawer, open link)
  Arrow keys        — navigate grid cells
  Esc               — close drawer
  r                 — reload data (same as Sync button)
  / (slash)         — focus filter input (filter by slug
                       substring; v1 simple; no fuzzy match)

ACCESSIBILITY

- Every interactive element has role / aria-label where needed.
- aria-live="polite" on the activity feed section.
- Focus ring always visible (3px solid var(--c-primary),
  2px offset).
- All colours in the legend have a text/icon companion; never
  colour alone.

DOM STRUCTURE (suggested — adjust as you see fit)

  <main>
    <header class="bar">…</header>
    <section class="summary">…</section>
    <section class="grid" aria-label="Year by subject production grid">
      <div class="cell" tabindex="0" data-year="3" data-subject="science">…</div>
      …
    </section>
    <section class="drawer" aria-live="polite" aria-label="Selected cell detail" hidden>
      <header>…</header>
      <div class="concept-group">…</div>
    </section>
    <section class="activity" aria-live="polite">
      <h2>Recent topic activity</h2>
      <ul class="feed">…</ul>
    </section>
    <section class="last-run" hidden>
      <details><summary>Last pipeline report</summary>…</details>
    </section>
  </main>

ACCEPTANCE CHECKLIST (before declaring done, verify every one):

- [ ] Four files exist: studio/index.html, studio/studio.css,
      studio/studio.js, studio/README.md.
- [ ] Opening http://localhost:3000/studio/ renders the dashboard
      without errors in the console.
- [ ] Summary strip shows correct counts parsed from status.csv.
      Expected numbers as of 2026-04-24: 120 live, 9 todo, 4
      validated. (These may shift as new topics ship; numbers
      must be computed from status.csv at load, not hard-coded.)
- [ ] 6 × 6 grid renders with all 36 cells.
- [ ] Each cell shows correct topic count and per-topic dots
      coloured per the legend.
- [ ] Clicking (or Enter-activating) the Y3 Science cell opens
      the drawer below the grid.
- [ ] Drawer lists 4 concepts under Y3 Science: Plants, Rocks
      and Fossils, Forces and Magnets, Light and Shadows.
- [ ] Each concept is collapsible; expanded rows show slug,
      perspective badge, status icons.
- [ ] plants-functions-y3, rocks-fossils, forces-magnets, and
      light-shadows all show 🔒 (protected) and ✓ (validated).
- [ ] "Open in app" link for a validated topic opens
      /app/#/year/3/science/{slug} in a new tab.
- [ ] Activity feed shows at least 4 entries (the 4 validated
      Y3 science topics with their validated_with_child dates).
- [ ] Keyboard navigation works: Tab moves through cells, arrow
      keys across grid, Enter drills, Esc closes, r reloads,
      / focuses filter.
- [ ] No console errors. No external URLs. prefers-reduced-motion
      respected. prefers-color-scheme: dark renders a dark variant.
- [ ] studio/README.md explains: how to open, each panel's meaning,
      keyboard shortcuts, what v1.5 will add.

NON-FUNCTIONAL

- Single commit: feat(studio): v1 content-studio dashboard.
- Do NOT modify anything outside studio/. The studio is purely
  additive.
- Do NOT add studio/ topics to curriculum/status.csv or
  tools/protected-exemplars.json — the studio is not a topic.
- Do NOT run `python tools/seed_status_csv.py` as part of this
  build; the studio only READS that CSV and does not affect it.

WHAT TO SKIP IN v1 (leave stubs if natural, omit if not)

- [Rebuild] / [Run pipeline] buttons — v1.5.
- Diff viewer — v1.5.
- Live stage strip — v1.5.
- Reviewer-verdict per-topic panels — waits on backlog X3
  (verdict JSON files); until then, verdicts are only visible
  via the optional last-pipeline-report block.
- WebSocket / SSE / polling — v2.
```

---

## After GHCP is done

1. Open `http://localhost:3000/studio/` and visually confirm the grid + drawer + feed render.
2. Diff-review the 4 new files for:
   - No external URLs
   - No writes (grep for `.write`, `localStorage.setItem`, POST, PUT, PATCH, DELETE)
   - Correct palette token use
3. If v1 looks right, commit. If something's off, iterate with a follow-up GHCP prompt naming the specific panel to fix.
4. Use it for a week. Note what you actually look at vs what's noise. That's the input to v1.5 scope.
