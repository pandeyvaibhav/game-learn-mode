# Feature Design — Progress Tracking & Gamification

| | |
|---|---|
| **Document** | `doc/feature-design-progress-gamification.md` |
| **Version** | 2.0 |
| **Date** | 2026-04-23 |
| **Authors** | Vaibhav Pandey (Owner) · Claude Opus 4.7 (AI pair) |
| **Status** | **Draft** — design only, no code yet |
| **Related** | [BACKLOG.md](../BACKLOG.md) (P3, L1, L2, L5, P4, B1–B4) · [architecture.md](architecture.md) · [feature-design-s10-playability.md](feature-design-s10-playability.md) · safety-policy §8 (no PII) |

---

## 1. Summary

Introduce a **progress + gamification layer** that treats the content library as a cognitive training corpus (see [architecture.md §1](architecture.md)) and the child's play as an **exposure matrix**: which concepts have been encountered, how many times, through which perspectives, how recently. From that, derive XP/badges/streaks and — critically — a **due-for-revisit** surface that drives retention.

Ship it as a **self-contained, framework-agnostic module** (`app/progress/`) that any future Vaibhav-Pandey app can drop in. Storage is **localStorage-first** with a **pluggable adapter** so a backend can be added later without changing call sites.

Without this layer, the child has no sense of progression, no reason to return, and no way to resume — and more importantly, no spaced-revisit mechanism to drive long-term retention.

### What v2 changes from v1

v1 of this doc (2026-04-19) tracked **per-topic completion flags** — `{viewed, completed, attempts, bestScore}` per topic. That model doesn't capture the point of a training corpus: **same concept, many perspectives, many exposures over time**. v2 tracks at the **concept level** with an ordered list of attempts across all perspectives of that concept. Completion is no longer a flag; it's a quality score that decays with time since last exposure (the basis for "due for revisit").

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

### 3.1 Public API (v2 — concept-level)

```js
// app/progress/progress.js
export class ProgressStore {
  constructor({ adapter, rules, appId, schemaVersion }) { /* … */ }

  // ── Recording exposure ──────────────────────────────────────
  recordAttempt({ conceptId, topicId, perspective, score, total, durationMs })
    // Appends one attempt to the concept's exposure array. This is
    // the only "write" call animations fan into via postMessage.

  markTopicSeen({ conceptId, topicId, perspective })
    // Lightweight exposure marker — fires on anim:ready even before
    // the child interacts. Idempotent within a short window.

  // ── Reads ───────────────────────────────────────────────────
  getConcept(conceptId)
    // { attempts: [...], firstSeen, lastSeen, exposureCount,
    //   perspectivesTouched: Set, bestScorePerTopic: {...},
    //   masteryScore: 0..1 — a function of exposure + recency + score }

  getTopic(topicId)
    // Filtered view onto the parent concept's attempts array where
    // topicId matches. Returns { attempts, lastSeen, bestScore }.

  getSummary()
    // { xp, level, badges: [id], streakDays, lastConceptId, lastTopicId }

  listDueForRevisit({ now = Date.now(), limit = 5 })
    // The core retention query (§6). Concepts ranked by
    // `due-score = masteryScore × decay(now − lastSeen)`. Lower = more due.

  listNeverTouched({ year, subject })
    // Concepts that have no attempts yet — drives the "try something
    // new" surface on the home screen.

  // ── Lifecycle ───────────────────────────────────────────────
  reset()
  on(event, handler)   // 'xp', 'badge', 'levelup', 'concept-mastered'
  off(event, handler)
  export()             // returns JSON; basis for P7 export/import
  import(data)
}
```

Events fire **after** state is persisted so UI can react safely.

**Key API shift from v1:** writes are now `recordAttempt({ conceptId, topicId, perspective, … })` not `recordQuizAttempt(topicId, …)`. The animation's `postMessage` payload gains `conceptId` and `perspective`, which the app shell reads from `curriculum/status.csv` and passes to the store. Animations themselves don't need to know their own concept — the shell routes the message.

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

## 4. Storage schema (v2 — concept exposure matrix)

All keys are namespaced: `glm.v2.*` (app id `glm` = game-learn-mode). Schema version 2 supersedes v1; a migration function in the module promotes existing v1 payloads to v2 by remapping each `topic.{topicId}` row into a `concept.{conceptId}` row (looking up the mapping from `curriculum/status.csv` bundled as `app/curriculum.json`).

| Key | Shape |
|---|---|
| `glm.v2.meta` | `{ schemaVersion: 2, appId, createdAt, lastOpenedAt }` |
| `glm.v2.summary` | `{ xp, level, badges: [id], streakDays, streakLastDay, lastConceptId, lastTopicId }` |
| `glm.v2.concept.{conceptId}` | See below — the exposure record |
| `glm.v2.history` | Ring buffer (last 50 attempts across all concepts) for debugging / future sync replay |

### 4.1 The concept exposure record

```jsonc
{
  "conceptId": "rocks-fossils",           // from curriculum.md
  "firstSeen": 1714234567890,
  "lastSeen":  1714435567890,
  "attempts": [
    {
      "topicId":     "rocks-fossils",      // the identify perspective
      "perspective": "identify",
      "timestamp":   1714234567890,
      "score":       5,
      "total":       5,
      "durationMs":  94000
    },
    {
      "topicId":     "rock-properties-sort",
      "perspective": "sort",
      "timestamp":   1714321567890,
      "score":       4,
      "total":       5,
      "durationMs":  102000
    },
    {
      "topicId":     "fossil-formation",
      "perspective": "sequence",
      "timestamp":   1714435567890,
      "score":       5,
      "total":       5,
      "durationMs":  87000
    }
    // attempts array is append-only within a concept; can grow large
    // for a child who revisits. Trimmed to last 30 per concept.
  ],
  "perspectivesTouched": ["identify", "sort", "sequence"],
  "bestScorePerTopic": {
    "rocks-fossils": 5,
    "rock-properties-sort": 4,
    "fossil-formation": 5
  }
}
```

**Why append-only with trim:** every encounter matters; a child's 10th play of `rocks-fossils` is different signal from their 1st (mastery, boredom, drift). Keeping attempts (bounded at 30) lets the gamification engine compute spacing, improvement-over-time, and perspective breadth. Single "best score" buckets would throw this away.

### 4.2 Derived values (not stored, computed on read)

| Value | Formula |
|---|---|
| `exposureCount` | `attempts.length` |
| `perspectiveBreadth` | `perspectivesTouched.size / perspectivesAvailable(conceptId)` — from curriculum.json |
| `recencyMs` | `now − lastSeen` |
| `avgScore` | mean of `attempts[].score / attempts[].total` |
| `masteryScore` | `(perspectiveBreadth × 0.5) + (avgScore × 0.3) + (min(exposureCount / 5, 1) × 0.2)` — bounded 0..1 |
| `dueScore` | `masteryScore × exp(−recencyMs / τ)` where τ = 3 days — **low = due for revisit** |

Schema version bump triggers a migration function. Unknown version → reset with a backup copy in `glm.v1.backup.{timestamp}` before wipe.

---

## 5. Integration points in the current app

1. **Animation side (already implemented in exemplars):**
   ```js
   parent.postMessage({ type:'anim:ready',    topic:'{slug}' }, '*');
   parent.postMessage({ type:'anim:attempt',  topic:'{slug}', correct:true }, '*');
   parent.postMessage({ type:'anim:complete', topic:'{slug}', score:5, total:5 }, '*');
   ```
2. **[app/app.js](../app/app.js) — shell routes events to the store, enriching with concept + perspective looked up from `app/curriculum.json`:**
   ```js
   window.addEventListener('message', (e) => {
     if (e.origin !== location.origin) return;
     const { type, topic, score, total, ...rest } = e.data || {};
     const meta = curriculum.topicMeta(topic); // { conceptId, perspective, year, subject }
     if (type === 'anim:ready')    store.markTopicSeen({ ...meta, topicId: topic });
     if (type === 'anim:attempt')  { /* optional fine-grained log */ }
     if (type === 'anim:complete') store.recordAttempt({ ...meta, topicId: topic, score, total });
   });
   ```
3. **Home screen** — three surfaces driven by `ProgressStore`:
   - 📍 **Continue where you left off** — `summary.lastConceptId` + last-played topic.
   - ⏰ **Due for revisit** — `listDueForRevisit({ limit: 3 })` — concepts ranked by dueScore ascending.
   - ✨ **Try something new** — `listNeverTouched({ year })` — concepts without any attempts.
4. **Header** — level + XP bar, hidden until first `recordAttempt` to avoid empty-state.
5. **Topic page footer** — badges earned related to this concept; a tiny "perspectives seen" indicator (e.g. 2 of 4 filled).
6. **Settings → Reset progress** — clearly labelled, confirmation-gated. Export-then-reset is the safer default.

No changes to `animations/` — animations stay self-contained; the app shell enriches their messages with concept + perspective via the curriculum lookup. This keeps animations dumb and the store authoritative.

---

## 5a. Due-for-revisit algorithm (§6 in v1 renumbered below)

The core retention feature. Implementation sketch:

```js
listDueForRevisit({ now = Date.now(), limit = 5 }) {
  const concepts = this._adapter.keys()
    .filter(k => k.startsWith('glm.v2.concept.'))
    .map(k => this._adapter.read(k));

  const τ = 3 * 24 * 3600 * 1000;  // 3 days half-life

  return concepts
    .filter(c => c.attempts.length > 0)            // only touched concepts
    .map(c => ({
      conceptId: c.conceptId,
      mastery: this._mastery(c),                    // 0..1
      recencyMs: now - c.lastSeen,
      dueScore: this._mastery(c) * Math.exp(-(now - c.lastSeen) / τ),
    }))
    // Lower dueScore = more due (high mastery + long time since = ideal revisit)
    .sort((a, b) => a.dueScore - b.dueScore)
    .slice(0, limit);
}
```

**Why mastery × decay, not just recency:** a child who barely touched a concept once 5 days ago isn't "due for revisit" — they need a *fresh* first pass, which is handled by `listNeverTouched` or by the shell surfacing the next unseen perspective of a partially-touched concept. The decay formula targets concepts the child *has* engaged with and are at risk of fading, which is precisely the spaced-retrieval sweet spot.

**Tuning τ:** 3 days is a starting point. Real children's retention curves differ; τ should become a gamification rule (`rules.json`) tunable per deployment once we have real usage data.

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
| **2.0** | **2026-04-23** | **Vaibhav Pandey · Claude Opus 4.7** | **Re-scoped to the training-corpus / concept-exposure-matrix model.** Summary rewritten. Public API (§3.1) moves from per-topic completion flags to concept-level `recordAttempt({ conceptId, topicId, perspective, ... })` + queries. Storage schema (§4) replaces `glm.v1.topic.{topicId}` with `glm.v2.concept.{conceptId}` holding an append-only trimmed attempts array. Added §4.2 derived values (`masteryScore`, `dueScore`). Added §5a due-for-revisit algorithm (mastery × exponential-decay). Integration contract (§5) specifies shell-side event enrichment via `app/curriculum.json`. |
