# Feature Design — Progress Tracking & Gamification

| | |
|---|---|
| **Document** | `doc/feature-design-progress-gamification.md` |
| **Version** | 1.0 |
| **Date** | 2026-04-19 |
| **Authors** | Vaibhav Pandey (Owner) · Claude Opus 4.7 (AI pair) |
| **Status** | **Draft** — design only, no code yet |
| **Related** | [BACKLOG.md](../BACKLOG.md) (P3, L1, L2, L5, P4, B1–B4) · [feature-design-s10-playability.md](feature-design-s10-playability.md) · safety-policy §8 (no PII) |

---

## 1. Summary

Introduce a **progress + gamification layer** that records what the child has done (topics viewed, quizzes attempted, scores, streaks) and turns it into a child-motivating loop (XP, badges, "continue where you left off"). Ship it as a **self-contained, framework-agnostic module** (`app/progress/`) that any future Vaibhav-Pandey app can drop in.

Storage is **localStorage-first** with a **pluggable adapter** so a backend can be added later without changing call sites.

This is the core retention mechanic. Without it, children have no sense of progression, no reason to return, and no way to resume — the app is effectively stateless.

---

## 2. Goals & non-goals

### Goals
- Track which topics a child has viewed / completed / quizzed.
- Award XP and badges against a rule set that is data-driven, not hard-coded per topic.
- Surface "continue where you left off" on the home screen.
- Be **portable**: the module must drop into another vanilla-JS app with zero changes.
- Be **offline-first**: localStorage is the source of truth; a backend is an *optional sync target*, never a dependency.
- Be **safe**: no PII, namespaced keys, explicit schema version, graceful reset on corruption.

### Non-goals
- Parent/teacher dashboards (L3, parked).
- Per-child accounts / multi-device sync on day one (B3 later).
- Adaptive difficulty (L5 — separate design, depends on this one).
- Social features (leaderboards, sharing). Children's product — out of scope.

---

## 3. Module shape

New folder `app/progress/` (copy-pasteable to any app):

```
app/progress/
├── progress.js          # public API (ProgressStore)
├── gamification.js      # rules engine (XP, badges, streaks)
├── adapters/
│   ├── local-storage.js # default adapter — browser localStorage
│   └── memory.js        # in-memory adapter — tests / SSR fallback
├── rules.json           # badge + XP rule config (data, not code)
└── README.md            # how to drop into another app
```

No framework, no build step, no dependency. Loaded as an ES module from the app shell.

### 3.1 Public API

```js
// app/progress/progress.js
export class ProgressStore {
  constructor({ adapter, rules, appId, schemaVersion }) { /* … */ }

  // reads
  getTopic(topicId)                 // { viewed, completed, attempts, bestScore, lastSeen }
  getSummary()                      // { xp, level, badges[], streakDays, lastTopicId }
  listCompleted()                   // [topicId, …]

  // writes
  markViewed(topicId)               // idempotent; sets lastSeen
  recordQuizAttempt(topicId, { score, total, durationMs })
  markCompleted(topicId)            // explicit completion (e.g. quiz ≥ threshold)

  // lifecycle
  reset()                           // wipes everything — parent setting later
  on(event, handler)                // 'xp', 'badge', 'levelup', 'completed'
  off(event, handler)
}
```

Events fire **after** state is persisted so UI can react safely.

### 3.2 Storage adapter interface

```js
// adapters/local-storage.js
export const localStorageAdapter = {
  read(key)        // -> parsed JSON or null
  write(key, val)  // stringifies + writes
  remove(key)
  keys()           // all keys under the configured namespace
}
```

A backend adapter (B1) implements the same four methods and is a drop-in replacement.

### 3.3 Rules config (`rules.json`)

Gamification rules are **data**, not code, so they can be tuned per deployment:

```json
{
  "xp": {
    "topicViewed": 5,
    "quizAttempt": 10,
    "quizPerfect": 25,
    "topicCompleted": 50,
    "dailyStreakDay": 15
  },
  "levels": [
    { "level": 1, "xpRequired": 0,    "title": "Explorer" },
    { "level": 2, "xpRequired": 100,  "title": "Learner" },
    { "level": 3, "xpRequired": 300,  "title": "Scholar" },
    { "level": 4, "xpRequired": 700,  "title": "Expert" },
    { "level": 5, "xpRequired": 1500, "title": "Champion" }
  ],
  "badges": [
    { "id": "first-step",    "title": "First Step",    "rule": "completedCount >= 1" },
    { "id": "maths-5",       "title": "Maths Five",    "rule": "completedCountIn(subject='maths') >= 5" },
    { "id": "streak-3",      "title": "3-Day Streak",  "rule": "streakDays >= 3" },
    { "id": "perfectionist", "title": "Perfectionist", "rule": "perfectScores >= 3" }
  ]
}
```

The rules engine evaluates a small, sandboxed DSL — no `eval`. Supported predicates: comparisons, `completedCountIn(subject=…)`, `streakDays`, `perfectScores`, `level`.

---

## 4. Storage schema (v1)

All keys are namespaced: `glm.v1.*` (app id `glm` = game-learn-mode).

| Key | Shape |
|---|---|
| `glm.v1.meta` | `{ schemaVersion: 1, createdAt, lastOpenedAt }` |
| `glm.v1.summary` | `{ xp, level, badges: [id], streakDays, streakLastDay, lastTopicId }` |
| `glm.v1.topic.{topicId}` | `{ viewed: bool, completed: bool, attempts, bestScore, lastSeen }` |
| `glm.v1.history` | Ring buffer (last 50 events) for debugging / future sync replay |

Schema version bump triggers a migration function. Unknown version → reset with a backup copy in `glm.v1.backup.{timestamp}` before wipe.

---

## 5. Integration points in the current app

1. **[app/app.js](../app/app.js)** — on topic open, call `store.markViewed(topicId)`. On quiz completion (once L1 lands), call `recordQuizAttempt`.
2. **Home screen** — render a "Continue where you left off" card from `store.getSummary().lastTopicId`.
3. **Header** — show current level + XP bar (hidden until the child completes the first topic, to avoid an empty state).
4. **Topic page footer** — show badges earned relating to this topic/subject.
5. **Settings → Reset progress** — a clearly labelled, confirmation-gated button.

No changes to `animations/` — animations stay self-contained; the app shell tracks progress based on quiz/completion events the animation already exposes (or fires its own).

---

## 6. Backend evolution (phased)

localStorage is the **source of truth**. A backend is an **optional mirror** added later.

| Phase | Feature | Backlog ID |
|---|---|---|
| v1 | localStorage only. No network. | P3 |
| v2 | Backend adapter reads/writes to a tiny JSON endpoint. Opt-in. Conflict policy = last-write-wins per key. | B1 |
| v3 | Auth (magic-link email or device code). Child profiles separate from adult login. | B2 |
| v4 | Multi-device sync + offline queue with replay. | B3 |
| v5 | Parent dashboard reads the same store via a different view. | B4 / L3 |

The adapter boundary means the module contract never changes — only the adapter switches. This is what makes it liftable.

---

## 7. Portability checklist

For the module to drop into another app cleanly:

- [ ] No imports outside `app/progress/`.
- [ ] No hard-coded `topicId` values, subject names, or year numbers. Everything comes from the host app's data.
- [ ] No DOM writes from inside the module — only events out.
- [ ] `appId` is configurable (so two apps on the same origin don't collide on localStorage keys).
- [ ] README documents: install, init, three-line usage example, adapter swap.
- [ ] Zero build step; works when served as static files.

---

## 8. Safety & privacy

- **No PII.** Never store name, email, date of birth, device ID. `appId` is the only identifier.
- **No analytics ping-outs** from the module. If the host app wants telemetry it subscribes to events and decides.
- **Reset is destructive but recoverable within one session** — latest backup kept under `glm.v1.backup.{timestamp}` for 24h, then purged.
- **Storage quota:** module caps `history` at 50 events and compacts on write. Total footprint target ≤ 50KB per child per app.
- **A11y:** level-up / badge-earned toasts must respect `prefers-reduced-motion` and be screen-reader announced via `aria-live="polite"`.

---

## 9. Risks & open questions

| # | Risk / question | Mitigation |
|---|---|---|
| R1 | Badges feel meaningless if the child can't see *why* they earned one | Every badge has a one-line explanation in `rules.json` shown on earn + in the badge list |
| R2 | Streak mechanics create pressure / shame when a streak breaks | No red "streak broken" UI; just silently reset. Show "start a new streak today!" instead |
| R3 | localStorage wiped by browser / incognito → child loses everything | Add "export progress" / "import progress" as a file (JSON) — v1.1 |
| R4 | Two children share a device | Accept v1 limitation. B2 (auth) solves properly. Document in README |
| Q1 | Should XP/levels be visible in Year 1? Or is it cognitive load? | Default: XP bar hidden until first completion, level badge only. Tune after play-test |
| Q2 | Where does the quiz mechanic live — in the animation or in the shell? | Separate decision in L1 design. This doc treats quiz results as an input event either way |

---

## 10. Acceptance

- [ ] `app/progress/` module exists with the four files in §3.
- [ ] `ProgressStore` used from `app/app.js` on topic open.
- [ ] Home screen shows a "Continue" card when state is non-empty.
- [ ] Header shows level + XP once the first topic is completed.
- [ ] Reset works from settings with confirmation.
- [ ] Module copies cleanly into a throwaway second app and works with only `appId` changed.
- [ ] No PII. No external network calls.

---

## 11. Change log

| Version | Date | Authors | Change |
|---|---|---|---|
| 1.0 | 2026-04-19 | Vaibhav Pandey · Claude Opus 4.7 | Initial design. Module layout, adapter interface, rules config, backend phasing, portability checklist. |
