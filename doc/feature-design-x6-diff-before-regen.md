# Feature Design — X6 Diff-Before-Regen Guard

| | |
|---|---|
| **Document** | `doc/feature-design-x6-diff-before-regen.md` |
| **Version** | 1.0 |
| **Date** | 2026-04-23 |
| **Authors** | Vaibhav Pandey (Owner) · Claude Opus 4.7 (AI pair) |
| **Status** | **Delivered** — manifest + CLI + git hook live |
| **Related** | [BACKLOG.md](../BACKLOG.md) (X6) · [topic-build-runbook.md](topic-build-runbook.md) · [.github/agents/orchestrator.agent.md](../.github/agents/orchestrator.agent.md) |

---

## 1. Summary

Hand-built, child-validated exemplars exist in this repo (`plants-functions-y3`). The agent pipeline (`@orchestrator`) currently does not know they are special — a `--force` run would happily regenerate the exemplar file, destroying validated work and reverting to the old quiz-only template.

X6 makes that impossible. It ships as **defence in depth**:

1. **Data** — a JSON manifest listing protected paths, their slugs, and their current SHA-256.
2. **Agent-level guard** — a CLI tool (`tools/guard_exemplar.py`) the orchestrator calls before writing. Refuses the write unless an explicit override token is passed.
3. **Tooling-level backstop** — a git pre-commit hook that reads the same manifest and blocks commits that change a protected file unless the commit message contains `--overwrite-exemplar={slug}`.

If an agent ignores layer 2, layer 3 catches it. If a human tries to commit a regression by hand, layer 3 catches that too. Protection is enforced at the tooling level, not the politeness level.

---

## 2. Goals & non-goals

### Goals
- Make it **impossible** to commit an overwrite of a protected exemplar without deliberate, explicit opt-in.
- Keep the protected list as **data** (a manifest file), not prose in agent specs — easy to add/remove entries as exemplars are validated.
- Auto-validate via SHA-256: any silent change to a protected file (even from a human editor) is caught unless explicitly acknowledged.
- Zero runtime dependencies beyond Python 3 and git. No external packages.
- Override path exists but requires a specific token (`--overwrite-exemplar={slug}`) — cannot be triggered by a blanket `--force`.

### Non-goals
- Not a full content-diff engine — this is a **path-level** guard, not a semantic-diff of content quality. If you overwrite with the override token, we trust you.
- Not a CI/CD check (could be added later as a GitHub Action calling the same CLI; not needed for local-only repos).
- Not a replacement for human review — it's a floor, not a ceiling.

---

## 3. The manifest

Location: `tools/protected-exemplars.json`

```json
{
  "version": 1,
  "description": "Hand-built, child-validated exemplars. See doc/feature-design-x6-diff-before-regen.md.",
  "protected": [
    {
      "slug": "plants-functions-y3",
      "paths": [
        "content/year-3/science/plants-functions-y3.md",
        "animations/year-3/science/plants-functions-y3.html"
      ],
      "sha256": {
        "content/year-3/science/plants-functions-y3.md": "…",
        "animations/year-3/science/plants-functions-y3.html": "…"
      },
      "validated_date": "2026-04-23",
      "validated_by": "real 7-year-old, unprompted engagement",
      "reason": "Gold-standard reference for topic-build-runbook"
    }
  ]
}
```

SHAs are refreshed via `python tools/guard_exemplar.py update {slug}` — that updates the manifest after an intentional change. Any unrefreshed drift is treated as suspicious.

---

## 4. The CLI tool

`tools/guard_exemplar.py` — single Python file, no dependencies.

### Commands

| Command | Purpose |
|---|---|
| `guard_exemplar.py check {path}` | Exit 0 if path is safe to write; exit 1 with message if protected. Used by agents before writing. |
| `guard_exemplar.py check {path} --allow {slug}` | Exit 0 if path is protected under that exact slug AND the slug matches. Agents pass this only when the user's invocation explicitly authorised overwrite. |
| `guard_exemplar.py verify` | Re-hashes every protected file, compares to manifest. Exit 0 if clean; exit 1 listing drifted files. |
| `guard_exemplar.py update {slug}` | Re-hash the slug's paths and write new SHAs to the manifest. Used after a deliberate update. Requires confirmation prompt. |
| `guard_exemplar.py list` | Print protected slugs + paths. |
| `guard_exemplar.py changed-files <file> [<file>…]` | Batch-check multiple paths (used by git hook). Exit 1 if any protected path is in the list without a matching allow marker. |

### Output contract

Structured single-line messages for agent parsing:
```
OK: path not protected
OK: path protected but --allow matches slug
BLOCKED: path {p} is protected exemplar ({slug}) — use --allow {slug} to override
DRIFT: path {p} sha mismatch; manifest {old}, file {new}
ERROR: {message}
```

---

## 5. The git hook

Location: `tools/hooks/pre-commit` (committed) + installed into `.git/hooks/pre-commit` via `tools/install-hooks.sh` (run once per clone).

### Behaviour

On every `git commit`:
1. List files staged for commit: `git diff --cached --name-only`.
2. Call `python tools/guard_exemplar.py changed-files {files…}`.
3. If guard returns BLOCKED:
   - Read the last line of `.git/COMMIT_EDITMSG` (the commit message in progress).
   - If it contains `--overwrite-exemplar={slug}` matching the blocked slug, allow the commit.
   - Otherwise, abort the commit and print the guard's message.

Rationale for using commit-message token (not env var): auditable in git history. A year from now, `git log` shows exactly which commits overwrote an exemplar and why.

---

## 6. Orchestrator integration

Two places in [.github/agents/orchestrator.agent.md](../.github/agents/orchestrator.agent.md):

### 6.1 Before any subject-agent / animation-generator dispatch (Step 2b, 2e)

```
Before dispatching the generator:
  result = bash("python tools/guard_exemplar.py check {content_path}")
  if result.exit_code != 0:
    if user's invocation contains "--overwrite-exemplar={slug}":
      log "EXEMPLAR OVERRIDE: {slug}"
      proceed
    else:
      log "SKIPPED-PROTECTED: {content_path}"
      mark todo skipped-protected
      continue with next topic
```

### 6.2 At pipeline start (Step 0.5 — new)

```
Before parsing curriculum:
  result = bash("python tools/guard_exemplar.py verify")
  if result.exit_code != 0:
    print "Manifest drift detected. Exemplar files differ from recorded SHAs."
    print result.stdout
    abort pipeline — user must resolve.
```

The verify step catches silent drift (e.g. someone edited the exemplar without updating the manifest). The run refuses to proceed until the drift is explained (either refresh manifest via `update {slug}` or revert the change).

---

## 7. Failure modes + responses

| Scenario | Layer that catches it | Response |
|---|---|---|
| Agent dispatches generator on protected path | Layer 2 (CLI called by orchestrator) | Guard exits 1, orchestrator logs SKIPPED-PROTECTED |
| Agent ignores CLI and writes directly | Layer 3 (git hook) | Hook blocks commit; no destructive change reaches `main` |
| Human edits exemplar carelessly | Layer 3 (git hook, via SHA drift check) | Hook blocks commit, prompts for either revert or `--overwrite-exemplar={slug}` |
| User actually wants to iterate the exemplar | Layer 3 accepts token | Commit succeeds with the override in the message; `git log` records why |
| Manifest itself is edited without a real change | Layer 2 `verify` at pipeline start | Catches drift; user must resolve |
| CI/CD runs without git hook | Deferred | Future: same CLI can run as a GitHub Action step |

---

## 8. Adding a new exemplar

When a hand-built topic passes child-validation:

```bash
# 1. Add to manifest (edit tools/protected-exemplars.json — add entry with placeholder SHAs)
# 2. Populate SHAs from current file state
python tools/guard_exemplar.py update {new-slug}
# 3. Verify
python tools/guard_exemplar.py verify
# 4. Commit the manifest update
git add tools/protected-exemplars.json
git commit -m "exemplar: mark {new-slug} as protected"
```

Runbook §5 is the source of truth for which exemplars *should* be protected (✅ status). The manifest is the enforcement.

---

## 9. Removing protection

Rare, but possible — e.g. an exemplar is deprecated in favour of a better one:

```bash
# 1. Delete the entry from tools/protected-exemplars.json
# 2. Commit
git commit -m "exemplar: remove {slug} protection — superseded by {new-slug}"
```

No special ceremony. Protection is data; removing it is a data change with a normal review trail.

---

## 10. Risks & open questions

| # | Risk / question | Mitigation |
|---|---|---|
| R1 | Developer forgets to install the git hook on fresh clone → layer 3 silently disabled | `tools/install-hooks.sh` runs in < 1s; called out in CLAUDE.md onboarding. Consider adding a repo-level `core.hooksPath` → `tools/hooks/` so the hook activates automatically without install, for the "just works" path |
| R2 | Agent strips `--overwrite-exemplar={slug}` from user's message and bypasses layer 2 | Layer 3 catches it on commit. Defence in depth is the point |
| R3 | SHA-256 collision / false drift | Negligible probability; false drift from line-ending changes is the real risk — manifest stores LF-normalised SHA, guard normalises before compare |
| R4 | Guard tool itself becomes a single point of failure (bugs in the Python) | Tool is ~150 lines, unit-testable. Bugs cause false-positive blocks (safer than false-negative bypass) |
| Q1 | Should we protect `.github/agents/*.agent.md` the same way? Tampering with agent specs is also high-blast-radius | Defer. Agent specs change more often than exemplars. Revisit if we see pipeline agents being corrupted |
| Q2 | Should layer 3 run on push rather than commit? | Commit is earlier and cheaper. Pre-push is extra work. Stick with pre-commit; add pre-push later if needed |

---

## 11. Acceptance

- [x] Design doc merged (this file).
- [x] `tools/protected-exemplars.json` exists with `plants-functions-y3` entry + real SHAs.
- [x] `tools/guard_exemplar.py` implements all 6 commands (check / check --allow / verify / update / list / changed-files).
- [x] `tools/hooks/pre-commit` hook implemented and `tools/install-hooks.sh` installs it.
- [x] Orchestrator spec calls the guard before dispatch and at pipeline start.
- [x] Self-test: attempt to overwrite `plants-functions-y3.html` with arbitrary content and confirm:
    - (a) `guard_exemplar.py check` blocks it.
    - (b) Commit attempt without override token blocks it.
    - (c) Commit with override token succeeds.
- [x] BACKLOG.md X6 marked done with links.

---

## 12. Change log

| Version | Date | Authors | Change |
|---|---|---|---|
| 1.0 | 2026-04-23 | Vaibhav Pandey · Claude Opus 4.7 | Initial delivery. Three-layer guard (manifest + CLI + git hook) with `--overwrite-exemplar={slug}` token as the only explicit override. Self-tested on `plants-functions-y3`. |
