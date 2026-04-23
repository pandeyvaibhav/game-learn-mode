# CLAUDE.md — Agent Front Door

This file is the primary context pointer for any coding agent (Claude Code, GitHub Copilot, another contributor) working on **game-learn-mode**, an agent-authored primary-school learning platform for UK KS1–KS2.

**Read this file before writing anything.** Then follow the links it points at.

---

## The one rule

Every topic on this platform is built to a **single validated pattern**. Before you produce any content or animation, you read:

1. [**doc/topic-build-runbook.md**](doc/topic-build-runbook.md) — the prescriptive methodology (3-part topic structure, visual rules, content shape, acceptance checklist).
2. [**animations/year-3/science/plants-functions-y3.html**](animations/year-3/science/plants-functions-y3.html) + [**content/year-3/science/plants-functions-y3.md**](content/year-3/science/plants-functions-y3.md) — the **reference implementation**. This is the *only* pattern. It has been validated with a real 7-year-old who engaged with it unprompted.

Your output must match the runbook's §7 acceptance checklist. If any box is unticked, the file does not ship.

---

## What's validated, what's in flight

- ✅ **1 topic** — `plants-functions-y3` (science, Year 3) — hand-built and play-tested successfully.
- 🟡 **18 Year 3 topics remaining** — see runbook §5 for per-topic briefs, grouped by subject.
- ⚪ **Years 1, 2, 4, 5, 6** — content exists but is pre-methodology vintage; not yet uplifted.

**Execution order is subject-by-subject**, science next. Don't stack new subjects onto unvalidated patterns. See runbook §5.7.

---

## Don't do this

- Don't produce verbose `content.md` (key-words tables, duplicated quizzes, "Learning Checklist" checkboxes). The animation is the lesson; the `.md` is 3 paragraphs + `## Sources`.
- Don't use ASCII-art "diagrams" in `<pre>` blocks. A real 7-year-old could not identify soil in one. If the answer is a diagram, it must be an SVG.
- Don't copy-paste the older quiz-only animation template. Start from `plants-functions-y3.html`.
- Don't let `--force` pipeline runs overwrite hand-built exemplars. **X6 is now enforced** by [`tools/guard_exemplar.py`](tools/guard_exemplar.py) + a `commit-msg` git hook. Commits that modify protected files are rejected unless the message contains `--overwrite-exemplar={slug}`. See [doc/feature-design-x6-diff-before-regen.md](doc/feature-design-x6-diff-before-regen.md).
- Don't skip `## Sources`. Backlog item **X5** (mechanical §9 check in S2) is incoming; without it, 98/117 files shipped without Sources because the reviewer wasn't enforcing its own rule.

---

## One-time setup on a fresh clone

```bash
sh tools/install-hooks.sh
```

Installs the X6 `commit-msg` hook into `.git/hooks/`. Without this, commits can still destroy protected exemplars. Script is idempotent — safe to re-run. Check status anytime with `python tools/guard_exemplar.py verify`.

---

## Where everything lives

| Area | Path | Purpose |
|---|---|---|
| Methodology | [doc/topic-build-runbook.md](doc/topic-build-runbook.md) | How to build a topic (read first) |
| Visual standard | [doc/feature-design-child-visual-standard.md](doc/feature-design-child-visual-standard.md) | Palette, type, motion, Bix, feedback |
| Animation system | [doc/feature-design-animation-system.md](doc/feature-design-animation-system.md) | 12-archetype catalogue design |
| Progress/gamification | [doc/feature-design-progress-gamification.md](doc/feature-design-progress-gamification.md) | P3/L2 reusable module design |
| Playability reviewer | [doc/feature-design-s10-playability.md](doc/feature-design-s10-playability.md) | S10 agent spec |
| Safety + mobile baseline | [doc/feature-design-p0-safety-mobile.md](doc/feature-design-p0-safety-mobile.md) | P0 gates |
| Safety policy | [.github/agents/_shared/safety-policy.md](.github/agents/_shared/safety-policy.md) | §§1–12 — banned topics, tone, PII, motion |
| Agent specs | [.github/agents/](.github/agents/) | Subject agents, reviewers, orchestrator |
| GHCP handoff prompts | [doc/ghcp-prompts-y3-science.md](doc/ghcp-prompts-y3-science.md) | Ready-to-paste prompts for Y3 science |
| Reference artefact | [animations/year-3/science/plants-functions-y3.html](animations/year-3/science/plants-functions-y3.html) | The gold standard |
| Shared CSS baseline | [animations/_shared/child-baseline.css](animations/_shared/child-baseline.css) | Tap targets, V1 tokens |
| Backlog | [BACKLOG.md](BACKLOG.md) | Priorities + status across all workstreams |

---

## Decision principles

When in doubt:

- **Content-first, generator-second.** If the pattern isn't validated by a real child on at least one exemplar in that subject, don't scale it. Hand-build one, validate, then refactor the agent.
- **Byte-sized over verbose.** A child doesn't read 200 lines of markdown. The animation teaches; the `.md` gives 3 paragraphs of context and cites its sources.
- **Shame-free feedback.** Wrong answers get `○` + "Not quite", never `✗` + "Wrong". Reveal the correct answer in green so the child learns from the mistake.
- **Offline-first, static-only.** No CDNs, no npm, no build step. Every animation is one self-contained HTML file.
- **Reality check beats internal review.** Passing S1/S2/S10 is necessary, not sufficient. The final judge is a child. If three sessions in a row answer "no, but we specced X better" to *"can a child now do something they couldn't?"* — the ratio is off.

---

## Next actionable thing

As of 2026-04-23, the next executable batch is three Y3 science topics — prompts ready to paste into GHCP: [doc/ghcp-prompts-y3-science.md](doc/ghcp-prompts-y3-science.md).

After science ships and plays well, the runbook §5.2 maths table drives the next batch.
