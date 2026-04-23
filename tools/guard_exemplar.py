#!/usr/bin/env python3
"""
X6 — Exemplar guard CLI.

Defends hand-built, child-validated exemplars from unintended overwrite.
Reads `tools/protected-exemplars.json`; used by the orchestrator before
writes and by the pre-commit git hook as a backstop.

See doc/feature-design-x6-diff-before-regen.md for the full design.

Usage:
    guard_exemplar.py check <path> [--allow <slug>]
    guard_exemplar.py verify
    guard_exemplar.py update <slug>
    guard_exemplar.py list
    guard_exemplar.py changed-files <file> [<file>…] [--allow <slug>]

Exit codes:
    0  success / not protected / override accepted
    1  blocked (protected path without matching --allow)
    2  drift detected (verify)
    3  usage error / manifest error
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "tools" / "protected-exemplars.json"


# ---------------------------------------------------------------- helpers
def _load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        _err(f"manifest not found: {MANIFEST_PATH}")
        sys.exit(3)
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _err(f"manifest is not valid JSON: {exc}")
        sys.exit(3)


def _save_manifest(data: dict) -> None:
    MANIFEST_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _sha256_lf(path: Path) -> str | None:
    """Return SHA-256 of the file with line endings normalised to LF, or
    None if the file does not exist."""
    if not path.exists():
        return None
    raw = path.read_bytes()
    normalised = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalised).hexdigest()


def _norm_path(p: str) -> str:
    """Normalise a path for comparison — forward slashes, relative to repo root."""
    # Accept absolute paths, paths with backslashes, or already-relative.
    pp = Path(p)
    if pp.is_absolute():
        try:
            pp = pp.resolve().relative_to(ROOT)
        except ValueError:
            pass  # outside repo — keep as-is, won't match
    return str(pp).replace("\\", "/")


def _find_protected_entry(path: str, manifest: dict) -> dict | None:
    """Return the manifest entry whose `paths` list contains `path`, or None."""
    n = _norm_path(path)
    for entry in manifest.get("protected", []):
        if n in entry.get("paths", []):
            return entry
    return None


def _err(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def _block(msg: str) -> None:
    print(f"BLOCKED: {msg}")


def _ok(msg: str) -> None:
    print(f"OK: {msg}")


# ---------------------------------------------------------------- commands
def cmd_check(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    entry = _find_protected_entry(args.path, manifest)
    if entry is None:
        _ok(f"{args.path} not protected")
        return 0
    slug = entry["slug"]
    if args.allow and args.allow == slug:
        _ok(f"{args.path} protected ({slug}) but --allow matches; override accepted")
        return 0
    _block(
        f"{args.path} is protected exemplar ({slug}) -- "
        f"pass --allow {slug} or include '--overwrite-exemplar={slug}' in commit message to override"
    )
    return 1


def cmd_verify(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    drifted = []
    missing = []
    for entry in manifest.get("protected", []):
        for p in entry["paths"]:
            expected = entry["sha256"].get(p)
            actual = _sha256_lf(ROOT / p)
            if actual is None:
                missing.append(p)
                continue
            if expected != actual:
                drifted.append((p, expected, actual))
    if missing:
        for p in missing:
            print(f"MISSING: {p} listed in manifest but file not found")
    if drifted:
        for p, exp, act in drifted:
            print(f"DRIFT: {p} sha mismatch; manifest {exp[:12]}..., file {act[:12]}...")
    if missing or drifted:
        return 2
    _ok("manifest in sync with files")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    entry = next(
        (e for e in manifest.get("protected", []) if e["slug"] == args.slug),
        None,
    )
    if entry is None:
        _err(f"slug not found in manifest: {args.slug}")
        return 3
    changes = []
    for p in entry["paths"]:
        actual = _sha256_lf(ROOT / p)
        if actual is None:
            _err(f"file missing: {p}")
            return 3
        if entry["sha256"].get(p) != actual:
            changes.append((p, entry["sha256"].get(p, "<absent>"), actual))
        entry["sha256"][p] = actual
    if not changes:
        _ok(f"{args.slug}: no SHA changes")
        return 0
    print(f"Updating manifest for slug '{args.slug}':")
    for p, old, new in changes:
        print(f"  {p}")
        print(f"    {old} -> {new}")
    _save_manifest(manifest)
    _ok(f"manifest updated for {args.slug}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    for entry in manifest.get("protected", []):
        print(f"{entry['slug']}  (validated {entry.get('validated_date','?')})")
        for p in entry["paths"]:
            print(f"  {p}")
    return 0


def cmd_changed_files(args: argparse.Namespace) -> int:
    """Batch check. Used by the pre-commit hook — reads files from argv."""
    manifest = _load_manifest()
    blocked = []
    for f in args.files:
        entry = _find_protected_entry(f, manifest)
        if entry is None:
            continue
        slug = entry["slug"]
        if args.allow and args.allow == slug:
            continue
        blocked.append((f, slug))
    if not blocked:
        _ok(f"no protected files in {len(args.files)} changed file(s)")
        return 0
    for f, slug in blocked:
        _block(
            f"{f} is protected exemplar ({slug}) -- "
            f"include '--overwrite-exemplar={slug}' in commit message to override"
        )
    return 1


# ---------------------------------------------------------------- entrypoint
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="guard_exemplar.py",
        description="X6 exemplar-overwrite guard. See doc/feature-design-x6-diff-before-regen.md.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="Check if a path is protected")
    p_check.add_argument("path")
    p_check.add_argument("--allow", help="Override slug (only accepted if it matches the protected entry)")
    p_check.set_defaults(func=cmd_check)

    p_verify = sub.add_parser("verify", help="Verify all protected files match their recorded SHAs")
    p_verify.set_defaults(func=cmd_verify)

    p_update = sub.add_parser("update", help="Refresh SHAs in the manifest for a slug (after intentional edit)")
    p_update.add_argument("slug")
    p_update.set_defaults(func=cmd_update)

    p_list = sub.add_parser("list", help="List all protected slugs and paths")
    p_list.set_defaults(func=cmd_list)

    p_cf = sub.add_parser("changed-files", help="Batch-check multiple paths (used by git hook)")
    p_cf.add_argument("files", nargs="+")
    p_cf.add_argument("--allow", help="Override slug (matches any protected file with that slug)")
    p_cf.set_defaults(func=cmd_changed_files)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
