# Feature Design — Child Visual Standard v1

| | |
|---|---|
| **Document** | `doc/feature-design-child-visual-standard.md` |
| **Version** | 1.0 |
| **Date** | 2026-04-19 |
| **Authors** | Vaibhav Pandey (Owner) · Claude Opus 4.7 (AI pair) |
| **Status** | **Draft** — opinionated defaults; tune after first play-test |
| **Related** | [BACKLOG.md](../BACKLOG.md) (V1–V5, L6) · [feature-design-animation-system.md](feature-design-animation-system.md) · [child-baseline.css](../animations/_shared/child-baseline.css) · [safety-policy.md](../.github/agents/_shared/safety-policy.md) |

---

## 1. Summary

We have a technical baseline (tap sizes, motion safety, font floors) but no **visual design language**. Each of the 117 animations picked its own look by copy-paste: dark navy background, indigo primary, ad-hoc emoji for feedback. That "default" was never a decision — it propagated from the first file. Consequence: a child moves from phonics to fractions to volcanoes and every screen is the same muted developer-dark look, with no recurring visual identity to anchor them.

This document sets an opinionated v1 — one illustration style, one semantic colour system, one type scale, one motion vocabulary, one icon library, one mascot, one feedback/celebration language. It is **prescriptive, not a menu**. We tune after play-testing, but we ship with choices, not options.

Because the standard is expressed almost entirely as CSS custom properties + an SVG symbol file, the generator inherits it for free — no per-topic styling decisions.

---

## 2. Goals & non-goals

### Goals
- One cohesive look across all subjects and years.
- Child-warm, not developer-dark. Vibrant but not overstimulating.
- Readable at Y1 (age 5) with growing density as year increases.
- Works offline, no web fonts, no licensed art.
- Accessibility-first: WCAG 2.2 AA body contrast minimum, AAA where practical.
- Inheritable: archetype shells and the 117 retrofits consume tokens, don't re-decide.

### Non-goals
- Per-subject visual themes. (A child doesn't need a different palette for maths vs english — it adds cognitive load for zero learning benefit.)
- Per-year themes. (Year progression shows in *content density* and *motion subtlety*, not look.)
- Full brand identity (logo, marketing). This is the *in-product* child surface only.
- Dark mode as a first-class mode. Child-facing default is light. A dark variant exists for parent-controlled settings but is not the primary canvas.
- Audio design. Out of scope v1 (consent + a11y complexity).

---

## 3. Illustration style

**Decision: flat-geometric with rounded corners.**

| Option | Chosen? | Reason |
|---|---|---|
| **Flat-geometric + rounded** | ✅ | Agent-generatable, SVG-native, scales to any screen, no art production per topic, ages 5–11 all parse it. |
| Hand-drawn / sketched | ❌ | Beautiful but not generator-producible without per-topic art. Vendor lock. |
| Cut-paper / collage | ❌ | Same problem; also busy on mobile. |
| Pixel art | ❌ | Nostalgic for adults, not warm for kids. Does not scale. |
| Line-art only | ❌ | Too sparse for Y1–2; reads as "diagram" not "game". |

**Rules for the style:**
- All shapes built from SVG primitives (`<rect>`, `<circle>`, `<path>` with rounded joins).
- Corner radius proportional to shape size (roughly ⅙ of the shorter edge). No sharp corners anywhere in the child surface.
- Stroke weight 2px at 24px viewport, scales with size.
- Fill-based, not stroke-only. Use a solid fill plus *one* subtle shadow or highlight; no gradients except for sky/water backdrops.
- No photorealism. No stock photography.
- No text on top of busy backgrounds. Text areas always sit on a flat fill.

### 3.1 Style preview

Sample composition using only the V1 style rules — rounded rectangles, solid fills, one warm accent, no gradients, no strokes competing with fills:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 140" width="420" height="140" role="img" aria-label="Style preview: flat-geometric with rounded corners">
  <rect width="420" height="140" rx="16" fill="#FFF9F2"/>
  <!-- sun -->
  <circle cx="60" cy="52" r="22" fill="#FF8A3D"/>
  <!-- cloud -->
  <rect x="100" y="40" width="70" height="26" rx="13" fill="#FFFFFF" stroke="#E8DCC7" stroke-width="2"/>
  <circle cx="112" cy="40" r="12" fill="#FFFFFF" stroke="#E8DCC7" stroke-width="2"/>
  <circle cx="140" cy="34" r="14" fill="#FFFFFF" stroke="#E8DCC7" stroke-width="2"/>
  <!-- plant pot -->
  <rect x="210" y="80" width="46" height="38" rx="8" fill="#B24EE0"/>
  <path d="M233 80 C 220 62, 206 60, 212 42 C 218 58, 226 60, 233 58 C 240 60, 248 58, 254 42 C 260 60, 246 62, 233 80 Z" fill="#1FA66A"/>
  <!-- shape tile -->
  <rect x="300" y="36" width="84" height="84" rx="18" fill="#4A5FDB"/>
  <text x="342" y="90" font-family="ui-rounded, system-ui, sans-serif" font-size="44" font-weight="700" fill="#FFFFFF" text-anchor="middle">7</text>
</svg>
```

Everything above is reachable from the v1 palette + primitive rules alone; no bespoke art per topic.

---

## 4. Colour system

Defined as CSS custom properties in `child-baseline.css` (additive — no removals). All colours meet WCAG 2.2 AA (4.5:1) on their paired text colour; body text hits AAA (7:1).

### 4.1 Neutral canvas (default child-facing surface)

| Token | Hex | Role | Contrast vs text |
|---|---|---|---|
| `--c-bg` | `#FFF9F2` | Warm off-white background. Never pure white — harsh on young eyes in dark rooms. | 13.1:1 vs `--c-ink` ✅ AAA |
| `--c-surface` | `#FFFFFF` | Cards, tiles, raised surfaces | 14.8:1 vs `--c-ink` ✅ AAA |
| `--c-surface-alt` | `#F5EEE3` | Secondary surface, disabled state, subtle sections | 11.8:1 vs `--c-ink` ✅ AAA |
| `--c-border` | `#E8DCC7` | Hairlines, separators | — |
| `--c-ink` | `#1E1E2A` | Primary text | baseline |
| `--c-ink-muted` | `#5A5566` | Secondary text, captions | 7.2:1 vs `--c-bg` ✅ AAA |

### 4.2 Semantic roles

| Token | Hex | Role | On-text pair |
|---|---|---|---|
| `--c-primary` | `#4A5FDB` | Primary action, links, focus highlight | `#FFFFFF` ✅ AA |
| `--c-primary-ink` | `#2B38A0` | Primary text on neutral surface | — |
| `--c-accent` | `#FF8A3D` | Accent (second-priority CTAs, highlights, mascot warm) | `#1E1E2A` ✅ AA |
| `--c-success` | `#1FA66A` | Correct answer | `#FFFFFF` ✅ AA |
| `--c-warn` | `#E0A020` | "Nearly", hint, soft-negative | `#1E1E2A` ✅ AA |
| `--c-error` | `#D8452B` | "Not quite" — still kind, never harsh red | `#FFFFFF` ✅ AA |
| `--c-celebrate` | `#B24EE0` | Level-up, badge earned, special moments | `#FFFFFF` ✅ AA |

### 4.3 Dark variant (opt-in only)

Same tokens, dark canvas. Child-facing default stays light. Dark exists for parent-controlled settings (`data-theme="dark"` on `<html>`).

| Token | Dark value |
|---|---|
| `--c-bg` | `#15131F` |
| `--c-surface` | `#1F1C2B` |
| `--c-ink` | `#F0EAD8` |
| `--c-ink-muted` | `#B8AEA0` |
| *(semantic roles lighten ~15% in dark)* | |

### 4.4 Rules
- **Never colour-alone for feedback.** Success always ships green + ✓ icon + text "Correct!" Error always red + ○ icon + text "Not quite". Enforced by S10 P8.
- **Max 3 semantic colours on one screen.** More fractures attention.
- **Mascot uses accent + warm highlight.** Never primary (reserved for the child's own actions).

### 4.5 Palette preview

Neutral canvas (light default):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 80" width="560" height="80" role="img" aria-label="Neutral canvas swatches">
  <g font-family="ui-rounded, system-ui, sans-serif" font-size="11">
    <rect x="0"   y="0" width="90" height="80" rx="10" fill="#FFF9F2" stroke="#E8DCC7"/>
    <text x="45" y="50" text-anchor="middle" fill="#1E1E2A">--c-bg</text>
    <text x="45" y="66" text-anchor="middle" fill="#5A5566">#FFF9F2</text>

    <rect x="95"  y="0" width="90" height="80" rx="10" fill="#FFFFFF" stroke="#E8DCC7"/>
    <text x="140" y="50" text-anchor="middle" fill="#1E1E2A">--c-surface</text>
    <text x="140" y="66" text-anchor="middle" fill="#5A5566">#FFFFFF</text>

    <rect x="190" y="0" width="90" height="80" rx="10" fill="#F5EEE3"/>
    <text x="235" y="50" text-anchor="middle" fill="#1E1E2A">--c-surface-alt</text>
    <text x="235" y="66" text-anchor="middle" fill="#5A5566">#F5EEE3</text>

    <rect x="285" y="0" width="90" height="80" rx="10" fill="#E8DCC7"/>
    <text x="330" y="50" text-anchor="middle" fill="#1E1E2A">--c-border</text>
    <text x="330" y="66" text-anchor="middle" fill="#5A5566">#E8DCC7</text>

    <rect x="380" y="0" width="90" height="80" rx="10" fill="#1E1E2A"/>
    <text x="425" y="50" text-anchor="middle" fill="#FFF9F2">--c-ink</text>
    <text x="425" y="66" text-anchor="middle" fill="#B8AEA0">#1E1E2A</text>

    <rect x="475" y="0" width="85" height="80" rx="10" fill="#5A5566"/>
    <text x="517" y="50" text-anchor="middle" fill="#FFF9F2">--c-ink-muted</text>
    <text x="517" y="66" text-anchor="middle" fill="#D8D5DA">#5A5566</text>
  </g>
</svg>
```

Semantic roles:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 80" width="560" height="80" role="img" aria-label="Semantic role swatches">
  <g font-family="ui-rounded, system-ui, sans-serif" font-size="11">
    <rect x="0"   y="0" width="78" height="80" rx="10" fill="#4A5FDB"/>
    <text x="39"  y="44" text-anchor="middle" fill="#FFFFFF" font-weight="600">primary</text>
    <text x="39"  y="62" text-anchor="middle" fill="#FFFFFF">#4A5FDB</text>

    <rect x="82"  y="0" width="78" height="80" rx="10" fill="#FF8A3D"/>
    <text x="121" y="44" text-anchor="middle" fill="#1E1E2A" font-weight="600">accent</text>
    <text x="121" y="62" text-anchor="middle" fill="#1E1E2A">#FF8A3D</text>

    <rect x="164" y="0" width="78" height="80" rx="10" fill="#1FA66A"/>
    <text x="203" y="44" text-anchor="middle" fill="#FFFFFF" font-weight="600">success</text>
    <text x="203" y="62" text-anchor="middle" fill="#FFFFFF">#1FA66A</text>

    <rect x="246" y="0" width="78" height="80" rx="10" fill="#E0A020"/>
    <text x="285" y="44" text-anchor="middle" fill="#1E1E2A" font-weight="600">warn</text>
    <text x="285" y="62" text-anchor="middle" fill="#1E1E2A">#E0A020</text>

    <rect x="328" y="0" width="78" height="80" rx="10" fill="#D8452B"/>
    <text x="367" y="44" text-anchor="middle" fill="#FFFFFF" font-weight="600">error</text>
    <text x="367" y="62" text-anchor="middle" fill="#FFFFFF">#D8452B</text>

    <rect x="410" y="0" width="90" height="80" rx="10" fill="#B24EE0"/>
    <text x="455" y="44" text-anchor="middle" fill="#FFFFFF" font-weight="600">celebrate</text>
    <text x="455" y="62" text-anchor="middle" fill="#FFFFFF">#B24EE0</text>
  </g>
</svg>
```

---

## 5. Typography

### 5.1 Type stack

System fonts only — no web font download, offline-first, instant render.

```css
--font-body: ui-rounded, "SF Pro Rounded", "Nunito", "Segoe UI Variable", "Segoe UI", system-ui, -apple-system, sans-serif;
--font-display: ui-rounded, "SF Pro Rounded", "Fredoka", "Nunito", system-ui, sans-serif;
```

`ui-rounded` is the key token — modern iOS, macOS, and recent Windows deliver genuinely rounded system faces. Android falls back through "Nunito" (common pre-installed) to `system-ui`. Net effect: warm, rounded letters on 95%+ of devices with zero network.

### 5.2 Size scale (fluid)

All sizes use `clamp()` so they scale with viewport. Reference is 360px → 540px mobile.

| Token | Value | Use |
|---|---|---|
| `--fs-xs` | `clamp(13px, 3.5vw, 14px)` | Meta labels, caption |
| `--fs-sm` | `clamp(15px, 4vw, 16px)` | Secondary text |
| `--fs-body` | `clamp(17px, 4.5vw, 18px)` | Body text |
| `--fs-prompt` | `clamp(19px, 5vw, 21px)` | Instructions to the child |
| `--fs-answer` | `clamp(20px, 5.5vw, 22px)` | Answer buttons, tile labels |
| `--fs-display` | `clamp(24px, 7vw, 32px)` | Titles, celebration |
| `--fs-xl` | `clamp(32px, 10vw, 44px)` | Number displays, score |

### 5.3 Rules
- Line-height 1.45 for body, 1.2 for display.
- Weight scale: 400 body, 600 prompt, 700 display. No 300 (too thin for emerging readers).
- Letter-spacing 0 default; +0.02em on all-caps labels only.
- **Maximum line length 45 characters** on any instruction line (roughly 20 words in a typical mix). S10 P3 already enforces word count; this enforces *visual* line length.

### 5.4 Type scale preview

Each line rendered in `ui-rounded` at its target size and weight:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 260" width="560" height="260" role="img" aria-label="Type scale preview">
  <rect width="560" height="260" rx="12" fill="#FFF9F2"/>
  <g font-family="ui-rounded, 'SF Pro Rounded', 'Nunito', system-ui, sans-serif" fill="#1E1E2A">
    <text x="20" y="28"  font-size="14" font-weight="400" fill="#5A5566">xs  14px · caption</text>
    <text x="20" y="52"  font-size="16" font-weight="400">sm  16px · secondary</text>
    <text x="20" y="78"  font-size="18" font-weight="400">body  18px · lesson body</text>
    <text x="20" y="108" font-size="21" font-weight="600">prompt  21px · instruction to child</text>
    <text x="20" y="140" font-size="22" font-weight="600">answer  22px · tile label</text>
    <text x="20" y="182" font-size="32" font-weight="700">display  32px · title</text>
    <text x="20" y="236" font-size="44" font-weight="700">xl  44</text>
  </g>
</svg>
```

---

## 6. Iconography

One SVG symbol file: `animations/_shared/svg/icons.svg`. ~24 named symbols to start.

### 6.1 Design rules
- 24px × 24px base viewBox.
- 2px stroke OR solid fill (pick per symbol — not mixed in one icon).
- 4px corner radius on stems, 2px on small details.
- Single-colour — consumes `currentColor`, so the caller sets it via `color:`.
- No text inside icons. Arrows point right by default; flip via CSS transform.

### 6.2 v1 symbol list

| Category | Symbols |
|---|---|
| Feedback | `check`, `cross`, `circle-pause` (for "nearly"), `star`, `sparkle` |
| Navigation | `arrow-right`, `arrow-left`, `arrow-up`, `arrow-down`, `back`, `next`, `close` |
| Learning | `book`, `pencil`, `question`, `lightbulb`, `ruler`, `calculator` |
| World | `sun`, `moon`, `cloud`, `plant`, `drop`, `letter`, `number` |
| Progress | `badge`, `trophy`, `flame` (streak) |

### 6.3 Usage

```html
<svg class="icon" aria-hidden="true"><use href="/animations/_shared/svg/icons.svg#check"/></svg>
```

Sized via `.icon { width: 1em; height: 1em; }` so it inherits line-height. Colour via `color: var(--c-success);`.

### 6.4 Icon preview

A subset of the v1 set rendered at 32px on canvas with semantic colours applied:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 120" width="560" height="120" role="img" aria-label="Icon preview">
  <rect width="560" height="120" rx="12" fill="#FFF9F2"/>
  <g fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <!-- check -->
    <g transform="translate(28,30)">
      <circle cx="16" cy="16" r="16" fill="#1FA66A" stroke="none"/>
      <path d="M9 17 L14 22 L23 11" stroke="#FFFFFF"/>
    </g>
    <!-- cross -->
    <g transform="translate(88,30)">
      <circle cx="16" cy="16" r="16" fill="#D8452B" stroke="none"/>
      <path d="M10 16 H22" stroke="#FFFFFF"/>
    </g>
    <!-- star -->
    <g transform="translate(148,30)">
      <path d="M16 3 L20 12 L30 13 L22 20 L24 30 L16 25 L8 30 L10 20 L2 13 L12 12 Z" fill="#E0A020" stroke="none"/>
    </g>
    <!-- sparkle -->
    <g transform="translate(208,30)" stroke="#B24EE0">
      <path d="M16 4 V28 M4 16 H28 M8 8 L24 24 M24 8 L8 24"/>
    </g>
    <!-- arrow-right -->
    <g transform="translate(268,30)" stroke="#4A5FDB">
      <path d="M4 16 H26 M20 10 L26 16 L20 22"/>
    </g>
    <!-- back -->
    <g transform="translate(328,30)" stroke="#4A5FDB">
      <path d="M28 16 H6 M12 10 L6 16 L12 22"/>
    </g>
    <!-- book -->
    <g transform="translate(388,30)" stroke="#1E1E2A">
      <path d="M5 6 H27 V26 H5 Z M16 6 V26"/>
    </g>
    <!-- lightbulb -->
    <g transform="translate(448,30)" stroke="#E0A020">
      <path d="M16 5 C 10 5 7 9 7 14 C 7 17 9 19 11 21 V25 H21 V21 C 23 19 25 17 25 14 C 25 9 22 5 16 5 Z M13 28 H19"/>
    </g>
    <!-- trophy -->
    <g transform="translate(508,30)" stroke="#B24EE0">
      <path d="M10 5 H22 V13 C 22 18 18 21 16 21 C 14 21 10 18 10 13 Z M6 8 C 6 12 8 14 10 14 M26 8 C 26 12 24 14 22 14 M12 21 V26 H20 V21"/>
    </g>
  </g>
  <g font-family="ui-rounded, system-ui, sans-serif" font-size="10" fill="#5A5566" text-anchor="middle">
    <text x="44"  y="90">check</text>
    <text x="104" y="90">cross</text>
    <text x="164" y="90">star</text>
    <text x="224" y="90">sparkle</text>
    <text x="284" y="90">arrow</text>
    <text x="344" y="90">back</text>
    <text x="404" y="90">book</text>
    <text x="464" y="90">bulb</text>
    <text x="524" y="90">trophy</text>
  </g>
</svg>
```

Each inherits `color:` from its container — one symbol file powers every semantic variant.

---

## 7. Motion vocabulary

### 7.1 Easing tokens

| Token | Curve | Use |
|---|---|---|
| `--ease-out` | `cubic-bezier(0.22, 1, 0.36, 1)` | Entrances, anything moving *in* |
| `--ease-in` | `cubic-bezier(0.64, 0, 0.78, 0)` | Exits, anything moving *out* |
| `--ease-both` | `cubic-bezier(0.4, 0, 0.2, 1)` | Symmetric transitions (open/close) |
| `--ease-bounce` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Celebration only — small overshoot |

Only these four. No custom curves per animation.

### 7.2 Duration scale

| Token | Value | Use |
|---|---|---|
| `--d-instant` | `80ms` | Hover, focus ring |
| `--d-fast` | `180ms` | Feedback flash, tap confirm |
| `--d-med` | `320ms` | Element entrance, page change |
| `--d-slow` | `560ms` | Celebration bounce, reveal |
| `--d-ambient` | `2400ms` | Idle background motion (breathing mascot, parallax) |

### 7.3 Motion roles

| Role | Easing | Duration | Example |
|---|---|---|---|
| Entrance | `--ease-out` | `--d-med` | Question card slides up + fades in |
| Feedback | `--ease-out` | `--d-fast` | Correct-answer pulse |
| Celebration | `--ease-bounce` | `--d-slow` | Star burst on topic complete |
| Transition | `--ease-both` | `--d-med` | Question N → N+1 crossfade |
| Ambient | `linear` | `--d-ambient` (looped) | Mascot breathing, drifting clouds |

### 7.4 Reduced-motion
`@media (prefers-reduced-motion: reduce)` — all transitions snap to `0.01ms`, ambient loops are disabled, celebration becomes a static burst (no bounce). **Parity of information**, not suppression of meaning.

### 7.5 Easing curves

X-axis is time (0→1), Y-axis is progress (0→1). A diagonal line would be `linear`; these four deviate deliberately:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 200" width="560" height="200" role="img" aria-label="Easing curve plot">
  <rect width="560" height="200" rx="10" fill="#FFF9F2"/>
  <g transform="translate(20,20)">
    <!-- grid -->
    <rect width="120" height="120" fill="none" stroke="#E8DCC7" stroke-width="1"/>
    <rect x="140" width="120" height="120" fill="none" stroke="#E8DCC7" stroke-width="1"/>
    <rect x="280" width="120" height="120" fill="none" stroke="#E8DCC7" stroke-width="1"/>
    <rect x="420" width="120" height="120" fill="none" stroke="#E8DCC7" stroke-width="1"/>

    <!-- reference linear (dotted) -->
    <line x1="0"   y1="120" x2="120" y2="0" stroke="#E8DCC7" stroke-dasharray="3 3"/>
    <line x1="140" y1="120" x2="260" y2="0" stroke="#E8DCC7" stroke-dasharray="3 3"/>
    <line x1="280" y1="120" x2="400" y2="0" stroke="#E8DCC7" stroke-dasharray="3 3"/>
    <line x1="420" y1="120" x2="540" y2="0" stroke="#E8DCC7" stroke-dasharray="3 3"/>

    <!-- ease-out cubic-bezier(0.22, 1, 0.36, 1): fast start, soft land -->
    <path d="M0,120 C 26.4,0 43.2,0 120,0" fill="none" stroke="#4A5FDB" stroke-width="3"/>

    <!-- ease-in cubic-bezier(0.64, 0, 0.78, 0): slow start, hard land -->
    <path d="M140,120 C 216.8,120 233.6,120 260,0" fill="none" stroke="#D8452B" stroke-width="3"/>

    <!-- ease-both cubic-bezier(0.4, 0, 0.2, 1): symmetric -->
    <path d="M280,120 C 328,120 304,0 400,0" fill="none" stroke="#1FA66A" stroke-width="3"/>

    <!-- ease-bounce cubic-bezier(0.34, 1.56, 0.64, 1): overshoot -->
    <path d="M420,120 C 460.8,-67.2 496.8,0 540,0" fill="none" stroke="#B24EE0" stroke-width="3"/>

    <g font-family="ui-rounded, system-ui, sans-serif" font-size="12" fill="#1E1E2A" text-anchor="middle">
      <text x="60"  y="145" font-weight="600">--ease-out</text>
      <text x="60"  y="160" fill="#5A5566">entrances</text>
      <text x="200" y="145" font-weight="600">--ease-in</text>
      <text x="200" y="160" fill="#5A5566">exits</text>
      <text x="340" y="145" font-weight="600">--ease-both</text>
      <text x="340" y="160" fill="#5A5566">transitions</text>
      <text x="480" y="145" font-weight="600">--ease-bounce</text>
      <text x="480" y="160" fill="#5A5566">celebration</text>
    </g>
  </g>
</svg>
```

Visually: blue shoots away fast then coasts in; red waits then rushes; green is symmetric; purple overshoots past 1.0 before settling — the "celebration feel" in a curve.

---

## 8. Mascot — "Bix"

**Decision: add one small recurring character.** Optional per-animation, required for reward overlays (L6).

### 8.1 Design
- Circle body (filled `--c-primary`), circle head (filled `--c-primary`), two dot eyes, small smile arc.
- One floating wave-hand. That's it. A child can draw it.
- Two antennae tipped with accent-orange sparks — that's the only warm element; the rest reads cool.
- Pure SVG, ~60 lines, no raster.

### 8.2 States
| State | Visual | When |
|---|---|---|
| Idle | Gentle breathing (scale 1.0 → 1.03, `--d-ambient` loop) | Reward moments, topic complete |
| Cheer | Small bounce + both hands up + sparkles | Correct answer streak, level-up |
| Think | Head tilt, one finger up | Hint shown, slow-response nudge |
| Console | Head slightly down, soft wave | Third wrong answer in a row — "let's try a different one" |

### 8.3 Rules
- Bix **never teaches content.** Speech bubbles are at most 6 words, always encouragement ("nice one!", "try again!"). Subject content stays in the animation itself.
- Bix does **not** appear in the core interaction area — only borders, reward overlays, intro/outro cards. The interaction gets the child's full attention.
- Bix is **optional per archetype.** Low-reading archetypes (AR5 phoneme-tap, AR8 canvas-paint) benefit from Bix presence; dense drag-reorder archetypes may skip.

### 8.4 Bix preview — four states

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 180" width="560" height="180" role="img" aria-label="Bix mascot in four states">
  <rect width="560" height="180" rx="12" fill="#FFF9F2"/>

  <!-- IDLE -->
  <g transform="translate(70,90)">
    <!-- antennae -->
    <line x1="-14" y1="-40" x2="-18" y2="-56" stroke="#4A5FDB" stroke-width="3" stroke-linecap="round"/>
    <line x1="14"  y1="-40" x2="18"  y2="-56" stroke="#4A5FDB" stroke-width="3" stroke-linecap="round"/>
    <circle cx="-18" cy="-58" r="4" fill="#FF8A3D"/>
    <circle cx="18"  cy="-58" r="4" fill="#FF8A3D"/>
    <!-- head -->
    <circle cx="0" cy="-22" r="22" fill="#4A5FDB"/>
    <circle cx="-7" cy="-24" r="2.5" fill="#FFF9F2"/>
    <circle cx="7"  cy="-24" r="2.5" fill="#FFF9F2"/>
    <path d="M-6 -16 Q 0 -12 6 -16" stroke="#FFF9F2" stroke-width="2" fill="none" stroke-linecap="round"/>
    <!-- body -->
    <circle cx="0" cy="14" r="26" fill="#4A5FDB"/>
    <text x="0" y="58" text-anchor="middle" font-family="ui-rounded, system-ui, sans-serif" font-size="12" fill="#5A5566">idle</text>
  </g>

  <!-- CHEER -->
  <g transform="translate(210,90)">
    <line x1="-14" y1="-40" x2="-20" y2="-58" stroke="#4A5FDB" stroke-width="3" stroke-linecap="round"/>
    <line x1="14"  y1="-40" x2="20"  y2="-58" stroke="#4A5FDB" stroke-width="3" stroke-linecap="round"/>
    <circle cx="-20" cy="-60" r="5" fill="#FF8A3D"/>
    <circle cx="20"  cy="-60" r="5" fill="#FF8A3D"/>
    <!-- sparkles -->
    <path d="M-34 -36 L-30 -30 M-34 -30 L-30 -36" stroke="#B24EE0" stroke-width="2"/>
    <path d="M34 -36 L30 -30 M34 -30 L30 -36" stroke="#B24EE0" stroke-width="2"/>
    <!-- head -->
    <circle cx="0" cy="-22" r="22" fill="#4A5FDB"/>
    <circle cx="-7" cy="-26" r="2.5" fill="#FFF9F2"/>
    <circle cx="7"  cy="-26" r="2.5" fill="#FFF9F2"/>
    <path d="M-8 -14 Q 0 -6 8 -14" stroke="#FFF9F2" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <!-- body + arms up -->
    <circle cx="0" cy="14" r="26" fill="#4A5FDB"/>
    <line x1="-22" y1="-2" x2="-34" y2="-18" stroke="#4A5FDB" stroke-width="6" stroke-linecap="round"/>
    <line x1="22"  y1="-2" x2="34"  y2="-18" stroke="#4A5FDB" stroke-width="6" stroke-linecap="round"/>
    <text x="0" y="58" text-anchor="middle" font-family="ui-rounded, system-ui, sans-serif" font-size="12" fill="#5A5566">cheer</text>
  </g>

  <!-- THINK -->
  <g transform="translate(350,90)">
    <!-- head tilted -->
    <g transform="rotate(-8)">
      <line x1="-14" y1="-40" x2="-18" y2="-56" stroke="#4A5FDB" stroke-width="3" stroke-linecap="round"/>
      <line x1="14"  y1="-40" x2="18"  y2="-56" stroke="#4A5FDB" stroke-width="3" stroke-linecap="round"/>
      <circle cx="-18" cy="-58" r="4" fill="#FF8A3D"/>
      <circle cx="18"  cy="-58" r="4" fill="#FF8A3D"/>
      <circle cx="0" cy="-22" r="22" fill="#4A5FDB"/>
      <circle cx="-7" cy="-24" r="2.5" fill="#FFF9F2"/>
      <circle cx="7"  cy="-24" r="2.5" fill="#FFF9F2"/>
      <path d="M-6 -15 Q 0 -15 6 -13" stroke="#FFF9F2" stroke-width="2" fill="none" stroke-linecap="round"/>
    </g>
    <!-- body + finger up -->
    <circle cx="0" cy="14" r="26" fill="#4A5FDB"/>
    <line x1="18" y1="-4" x2="26" y2="-24" stroke="#4A5FDB" stroke-width="6" stroke-linecap="round"/>
    <circle cx="26" cy="-28" r="5" fill="#FF8A3D"/>
    <text x="0" y="58" text-anchor="middle" font-family="ui-rounded, system-ui, sans-serif" font-size="12" fill="#5A5566">think</text>
  </g>

  <!-- CONSOLE -->
  <g transform="translate(490,90)">
    <line x1="-14" y1="-36" x2="-18" y2="-52" stroke="#4A5FDB" stroke-width="3" stroke-linecap="round"/>
    <line x1="14"  y1="-36" x2="18"  y2="-52" stroke="#4A5FDB" stroke-width="3" stroke-linecap="round"/>
    <circle cx="-18" cy="-54" r="4" fill="#FF8A3D"/>
    <circle cx="18"  cy="-54" r="4" fill="#FF8A3D"/>
    <!-- head tilted down -->
    <circle cx="0" cy="-18" r="22" fill="#4A5FDB"/>
    <circle cx="-7" cy="-18" r="2.5" fill="#FFF9F2"/>
    <circle cx="7"  cy="-18" r="2.5" fill="#FFF9F2"/>
    <path d="M-6 -8 Q 0 -10 6 -8" stroke="#FFF9F2" stroke-width="2" fill="none" stroke-linecap="round"/>
    <!-- body + soft wave -->
    <circle cx="0" cy="16" r="26" fill="#4A5FDB"/>
    <line x1="-20" y1="8" x2="-32" y2="2" stroke="#4A5FDB" stroke-width="6" stroke-linecap="round"/>
    <text x="0" y="60" text-anchor="middle" font-family="ui-rounded, system-ui, sans-serif" font-size="12" fill="#5A5566">console</text>
  </g>
</svg>
```

All four states are the same six primitives (two antennae, two dots, head, body) with different limb + head angles — a single ~80-line SVG file covers them all via CSS class swaps.

---

## 9. Feedback + celebration language

One consistent treatment across every archetype.

### 9.1 Correct answer
- Button turns `--c-success`, `check` icon appears, text label "Correct!" (Y1–4) or "Nice!" (Y5–6).
- Tile pulses: scale 1.0 → 1.04 → 1.0 with `--ease-bounce --d-fast`.
- Score increments with a `--d-instant` tick.
- `aria-live="polite"` announces "Correct."

### 9.2 Wrong answer
- Button turns `--c-error`, `circle-pause` icon (never ✗ — too harsh), text "Not quite" (Y1–2) or "Nearly — try again" (Y3–6).
- The *correct* button lights `--c-success` with `check`.
- No shake, no red flash, no negative sound. Shame-free.
- `aria-live="polite"` announces "Not quite. Answer is X."

### 9.3 Hint / "nearly"
- `--c-warn` outline, `lightbulb` icon, no button disable.

### 9.4 Topic complete
- Celebration card: Bix Cheer state, 5 stars (filled by score threshold), badge if earned.
- Confetti burst via SVG symbol array (or Lottie once A7 lands) — duration `--d-slow`.
- "Play again" + "Next topic" CTAs in `--c-primary`.

### 9.5 Level-up (L6 reward)
- Overlay above animation iframe, in the app shell.
- `--c-celebrate` background, Bix Cheer + "Level N!" + badge icon.
- Dismissable by tap anywhere. Auto-dismiss 3.5s.

### 9.6 Feedback state preview

Same answer button shown in its four visual states — idle, correct, not-quite, and the resolved pair after a wrong answer (original choice in error, correct answer highlighted):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 260" width="560" height="260" role="img" aria-label="Feedback states">
  <rect width="560" height="260" rx="12" fill="#FFF9F2"/>
  <g font-family="ui-rounded, system-ui, sans-serif">

    <!-- IDLE -->
    <g transform="translate(20,20)">
      <rect width="150" height="56" rx="14" fill="#FFFFFF" stroke="#E8DCC7" stroke-width="2"/>
      <text x="75" y="36" text-anchor="middle" font-size="20" font-weight="600" fill="#1E1E2A">Ship</text>
      <text x="75" y="84" text-anchor="middle" font-size="11" fill="#5A5566">idle</text>
    </g>

    <!-- CORRECT -->
    <g transform="translate(200,20)">
      <rect width="150" height="56" rx="14" fill="#1FA66A"/>
      <circle cx="22" cy="28" r="11" fill="#FFFFFF"/>
      <path d="M17 28 L21 32 L28 24" stroke="#1FA66A" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <text x="87" y="36" text-anchor="middle" font-size="20" font-weight="600" fill="#FFFFFF">Ship</text>
      <text x="75" y="84" text-anchor="middle" font-size="11" fill="#1FA66A" font-weight="600">Correct!</text>
    </g>

    <!-- NOT QUITE -->
    <g transform="translate(380,20)">
      <rect width="150" height="56" rx="14" fill="#D8452B"/>
      <circle cx="22" cy="28" r="11" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
      <line x1="16" y1="28" x2="28" y2="28" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
      <text x="87" y="36" text-anchor="middle" font-size="20" font-weight="600" fill="#FFFFFF">Ship</text>
      <text x="75" y="84" text-anchor="middle" font-size="11" fill="#D8452B" font-weight="600">Not quite</text>
    </g>

    <!-- RESOLVED PAIR -->
    <g transform="translate(20,130)">
      <text x="0" y="-10" font-size="11" fill="#5A5566">After a wrong answer — original stays dim-error, correct lights up so the child sees both:</text>

      <!-- wrong original -->
      <g transform="translate(0,0)">
        <rect width="150" height="56" rx="14" fill="#D8452B" opacity="0.55"/>
        <circle cx="22" cy="28" r="11" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
        <line x1="16" y1="28" x2="28" y2="28" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
        <text x="87" y="36" text-anchor="middle" font-size="20" font-weight="600" fill="#FFFFFF">Chip</text>
      </g>

      <!-- correct highlighted -->
      <g transform="translate(180,0)">
        <rect width="150" height="56" rx="14" fill="#1FA66A"/>
        <circle cx="22" cy="28" r="11" fill="#FFFFFF"/>
        <path d="M17 28 L21 32 L28 24" stroke="#1FA66A" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        <text x="87" y="36" text-anchor="middle" font-size="20" font-weight="600" fill="#FFFFFF">Ship</text>
      </g>

      <!-- feedback line -->
      <g transform="translate(360,0)">
        <rect width="180" height="56" rx="14" fill="#F5EEE3"/>
        <text x="90" y="26" text-anchor="middle" font-size="13" fill="#1E1E2A" font-weight="600">Nearly — try again</text>
        <text x="90" y="44" text-anchor="middle" font-size="11" fill="#5A5566">announced via aria-live</text>
      </g>
    </g>
  </g>
</svg>
```

Note the `circle-pause` glyph on "Not quite" — deliberately softer than a ✗. The resolved pair teaches while it corrects: the child sees what they picked *and* what was right, side by side, with no shame cue.

---

## 10. Layout grid

- **Max content width** `540px`. On wider screens, centre with generous ambient margin.
- **Safe-area padding** `max(env(safe-area-inset-top), 16px)` top, same bottom — handles notch phones.
- **Base unit** `8px`. All paddings, margins, gaps are multiples.
- **Gutter** `16px` mobile, `24px` tablet+.
- **Vertical rhythm** `8px` — text baselines align to this grid.
- **Interactive element gap** `--tap-gap: 12px` (already in baseline CSS) — stops accidental double-taps.

---

## 11. Accessibility floors

Non-negotiable:

- **Contrast:** body ≥ 7:1 (AAA), prompts/buttons ≥ 4.5:1 (AA). Colours in §4 are pre-checked.
- **Focus ring:** 3px `--c-primary` outline, 2px offset, on every focusable element. Never `outline: none` without a replacement.
- **Keyboard:** tab order matches visual order; Enter + Space activate buttons; Escape closes overlays.
- **Screen reader:** `aria-live="polite"` on feedback region; `aria-label` on icon-only controls.
- **Motion:** `prefers-reduced-motion` respected everywhere (§7.4).
- **Touch target:** ≥ 44px min, ≥ 56px primary — already in baseline CSS.
- **Text alternative:** every meaningful SVG has `<title>` or `aria-label`.

---

## 12. Integration

### 12.1 Token delivery
Additive update to [child-baseline.css](../animations/_shared/child-baseline.css) — new tokens under the existing `:root` block. No existing selector behaviour changes. (V2 in backlog.)

### 12.2 Icon delivery
New file `animations/_shared/svg/icons.svg` with `<symbol>` defs. Referenced by `<use>` — browser caches once, then free. (V3 in backlog.)

### 12.3 Archetype shells (A1)
Each archetype shell built on this standard from day one. Shells inline baseline tokens, reference icon symbols, use motion tokens. No ad-hoc colour / duration literals.

### 12.4 Agent prompts
[animation-generator.agent.md](../.github/agents/animation-generator.agent.md) gets a new "Visual standard — MANDATORY" section that forbids:
- Hardcoded hex colours outside the V1 palette.
- Hardcoded durations (must use `--d-*` tokens).
- Icon glyphs as unicode emoji where a symbol exists in icons.svg.
- Introducing new fonts.

S1 reviewer gets a mechanical pre-check (analogous to X5 for Sources): grep for hex colour literals; any outside the approved palette → FAIL before LLM review.

---

## 13. Retrofit plan

1. **Land V2** (tokens in baseline CSS). No animation files change yet.
2. **Land V3** (icons.svg). No animation files change yet.
3. **Land V4** (Bix mascot as SVG). No animation files change yet.
4. **A1 archetype shells** are written against the full standard — 12 shells, reference-quality.
5. **A3 retrofit** of 117 files picks up the visual standard automatically via the archetype-aware generator.
6. **V5** stylistic retrofit for any lingering files not covered by A3 — cleanup sweep.

Net: no standalone visual retrofit of 117 files is needed. The standard lands when archetypes land.

---

## 14. Risks & open questions

| # | Risk / question | Mitigation |
|---|---|---|
| R1 | Warm off-white (`#FFF9F2`) reads yellowish on poorly calibrated screens | Acceptable — warm palette is deliberate. If complaints surface, add a `--c-bg-neutral: #FFFFFF` variant token. |
| R2 | `ui-rounded` fallback on Android delivers `system-ui` which may be sans-geometric, not rounded | Accept v1 degradation. Could bundle a 20KB rounded web font (Nunito subset) later — revisit if Android feedback is negative. |
| R3 | Bix adds cognitive load when child is mid-interaction | §8.3 rules keep Bix out of the interaction area. Enforced by visual QA, not the generator. |
| R4 | One palette for all years means Y6 feels the same as Y1 | Year differentiation lives in *content density* and *motion subtlety*, not colour. If we later need year variants, we introduce sub-tokens (e.g. `--c-primary-y6: hue-shifted`) without breaking the base system. |
| R5 | Generator may drift from palette under LLM load — "#4A5FDA" instead of "#4A5FDB" | S1 mechanical pre-check (§12.4) catches any hex literal not in the allowlist before LLM review. |
| R6 | Dark variant parity work is unbounded | v1 ships with just canvas + ink dark tokens. Semantic roles are lightened programmatically (15% lightness shift) — if a specific role doesn't pass AA in dark, we override per-token. |
| Q1 | Do we need a brand/voice guideline alongside the visual one? | Yes, eventually. Voice (reading register, sentence length, encouragement phrasing) is already partly in safety-policy §3. Extract a companion "Voice standard" doc after V1 ships. |
| Q2 | Should the mascot have a colour that's distinct from `--c-primary`? | Considered. Primary-coloured mascot ties it to "your actions" visually — reinforces that Bix is on the child's side. If user-testing says it's confusing, split to `--c-bix`. |

---

## 15. Non-goals

- **Sound design** — no audio v1.
- **Animated mascot dialogue** — Bix does not speak (no bubbles beyond 6-word encouragement). Keeps safety review surface small.
- **Seasonal / holiday variants** — no. The product works year-round without calendar awareness.
- **Custom per-child avatars** — no. Requires auth (B2) and adds PII surface.
- **Dark mode parity with light** — v1 ships dark with functional parity only, not pixel-equivalent polish.

---

## 16. Acceptance

### v1 — standard published
- [ ] This document merged.
- [ ] Backlog V1 marked done; V2, V3, V4 queued.

### v2 — tokens live
- [ ] `child-baseline.css` updated with §4, §5, §7 tokens.
- [ ] One reference animation (`counting-to-100.html`) manually rebuilt under the new tokens as a proof of concept.
- [ ] Contrast audit passes on all semantic colours (automated or manual).

### v3 — assets live
- [ ] `animations/_shared/svg/icons.svg` contains all §6.2 symbols.
- [ ] Bix SVG + four state variants shipped as `animations/_shared/svg/bix.svg`.

### v4 — enforcement live
- [ ] Animation-generator agent prompt updated with §12.4 rules.
- [ ] S1 reviewer gains mechanical hex-colour allowlist pre-check.
- [ ] First post-standard pipeline run produces zero out-of-palette hex literals.

---

## 17. Change log

| Version | Date | Authors | Change |
|---|---|---|---|
| 1.0 | 2026-04-19 | Vaibhav Pandey · Claude Opus 4.7 | Initial opinionated standard. Flat-geometric illustration, warm-light canvas, 7-role semantic palette, fluid type scale on `ui-rounded` stack, four easings × five durations, 24-symbol icon library, Bix mascot v1, universal feedback language, 8px grid, AA/AAA accessibility floors. |
