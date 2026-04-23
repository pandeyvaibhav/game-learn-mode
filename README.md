# Game Learn Mode

Agent-authored primary-school learning platform for UK KS1–KS2. Each topic ships as a **byte-sized description + interactive SVG illustration + visual exercise**, built to a validated pattern tested with real children.

Everything is **static files**: vanilla HTML/CSS/JS, no build step, no npm, no CDNs. Works offline.

---

## Quick start

### 1. Clone and run locally

```bash
git clone <repo-url>
cd game-learn-mode

# One-time: install the exemplar-protection git hook (X6)
sh tools/install-hooks.sh

# Serve the app
python -m http.server 3000

# Open in browser
# http://localhost:3000/app/
```

The install step is **one-time per clone**. It sets up a `commit-msg` git hook that prevents accidental overwrite of hand-built, child-validated exemplars. Without it, you can still work on the repo — but committing changes to a protected file won't be guarded.

### 2. Try the reference topic

Open the validated exemplar to see what "good" looks like:

```
http://localhost:3000/app/#/year/3/science/plants-functions-y3
```

That file is the pattern every other topic should look like. See [doc/topic-build-runbook.md](doc/topic-build-runbook.md).

---

## What's in here

| Path | What |
|---|---|
| [app/](app/) | Host app shell (single-page, routes `/year/{N}/{subject}/{slug}`) |
| [animations/](animations/) | One self-contained HTML file per topic (the game) |
| [animations/_shared/child-baseline.css](animations/_shared/child-baseline.css) | Shared design tokens (V1 palette, type, motion, tap sizes) |
| [content/](content/) | One markdown file per topic (byte-sized description + sources) |
| [curriculum/](curriculum/) | UK National Curriculum topic list driving generation |
| [doc/](doc/) | Design docs (methodology, visual standard, animation system, progress/gamification, X6 guard) |
| [.github/agents/](.github/agents/) | Agent specs — subject agents, animation generator, reviewers (S1/S2/S10), orchestrator |
| [tools/](tools/) | CLI guards + install scripts (X6 exemplar protection, Y3 palette swap) |
| [CLAUDE.md](CLAUDE.md) | Primary context pointer for any coding agent |
| [BACKLOG.md](BACKLOG.md) | Priorities + status across all workstreams |

---

## Reading order for a new contributor

1. [CLAUDE.md](CLAUDE.md) — what's validated, what's in flight, decision principles.
2. [doc/topic-build-runbook.md](doc/topic-build-runbook.md) — how to build a topic.
3. [animations/year-3/science/plants-functions-y3.html](animations/year-3/science/plants-functions-y3.html) + [paired .md](content/year-3/science/plants-functions-y3.md) — the reference implementation.
4. [doc/feature-design-child-visual-standard.md](doc/feature-design-child-visual-standard.md) — V1 design language (inline SVG previews of palette, type, icons, easing curves, Bix mascot, feedback states).
5. [BACKLOG.md](BACKLOG.md) — what's next.

---

## For AI coding agents (GHCP, Claude, …)

If you are a coding agent working on this repo, **start at [CLAUDE.md](CLAUDE.md)**. It is the front door specifically for you.

Ready-to-paste prompt packs live in [doc/ghcp-prompts-y3-science.md](doc/ghcp-prompts-y3-science.md).

---

## Protected exemplars (X6)

Hand-built, child-validated topics are listed in [tools/protected-exemplars.json](tools/protected-exemplars.json) and guarded by:

- `python tools/guard_exemplar.py verify` — audit SHA-256 drift
- `python tools/guard_exemplar.py list` — see protected slugs
- The `commit-msg` git hook (installed via `sh tools/install-hooks.sh`)

Commits that modify a protected file are rejected unless the commit message contains `--overwrite-exemplar={slug}`. See [doc/feature-design-x6-diff-before-regen.md](doc/feature-design-x6-diff-before-regen.md).

---

## Non-negotiables

- **Offline-first.** No CDNs, no npm, no build step. Every animation is one self-contained HTML file.
- **No PII.** Never store, request, or transmit a child's name, age, school, or any personal data. See [.github/agents/_shared/safety-policy.md](.github/agents/_shared/safety-policy.md) §8.
- **Shame-free feedback.** Wrong answers get `○` + "Not quite", never `✗` + "Wrong".
- **Content-first, generator-second.** Hand-build one exemplar per subject, validate with a real child, then scale via agents. Never the other way around.
- **A real child is the final judge.** Passing S1 (safety) + S2 (factual) + S10 (playability) is necessary, not sufficient.

---

## Status (2026-04-23)

- ✅ **1 topic validated** — `plants-functions-y3` (science, Year 3), play-tested with a 7-year-old
- 🟡 **18 Year 3 topics queued** — see runbook §5 for per-topic briefs
- ⚪ **Years 1, 2, 4, 5, 6** — content exists but is pre-methodology vintage; awaiting uplift after Y3 is shipped

See [BACKLOG.md](BACKLOG.md) top-priorities section for the execution order.
