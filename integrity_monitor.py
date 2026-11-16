#!/usr/bin/env python3
"""
File Integrity Monitor (FIM)
Creates a SHA-256 baseline for files in a chosen directory, then compares
the current files against that baseline to detect additions, changes, and
deletions.

Usage:
    python integrity_monitor.py baseline ./demo_files
    python integrity_monitor.py check ./demo_files
"""
import argparse
import hashlib
import json
from pathlib import Path

DEFAULT_BASELINE = Path("integrity_baseline.json")

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def collect_hashes(folder: Path):
    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"Directory does not exist: {folder}")
    results = {}
    for item in sorted(folder.rglob("*")):
        if item.is_file():
            results[str(item.relative_to(folder))] = sha256_file(item)
    return results

def create_baseline(folder: Path, baseline: Path):
    current = collect_hashes(folder)
    baseline.write_text(json.dumps(current, indent=2), encoding="utf-8")
    print(f"Baseline created: {baseline.resolve()}")
    print(f"Files recorded: {len(current)}")

def check_baseline(folder: Path, baseline: Path):
    if not baseline.exists():
        raise SystemExit(f"Baseline not found: {baseline}. Run the baseline command first.")
    try:
        known = json.loads(baseline.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Could not read baseline: {exc}")

    current = collect_hashes(folder)
    old_paths, new_paths = set(known), set(current)
    added = sorted(new_paths - old_paths)
    deleted = sorted(old_paths - new_paths)
    changed = sorted(path for path in old_paths & new_paths if known[path] != current[path])

    print("\n=== FILE INTEGRITY REPORT ===")
    print(f"Directory: {folder.resolve()}")
    print(f"Unchanged files: {len(old_paths & new_paths) - len(changed)}")
    print(f"Added files: {len(added)}")
    print(f"Modified files: {len(changed)}")
    print(f"Deleted files: {len(deleted)}")
    for label, paths in (("ADDED", added), ("MODIFIED", changed), ("DELETED", deleted)):
        for path in paths:
            print(f"  [{label}] {path}")
    if not (added or changed or deleted):
        print("Result: No changes detected.")
    else:
        print("Result: Changes detected. Verify whether each change was authorized.")
    print("Note: Protect the baseline file; an attacker who can alter it may hide changes.")

def main():
    parser = argparse.ArgumentParser(description="Monitor file changes using SHA-256 hashes.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("baseline", "check"):
        cmd = sub.add_parser(name)
        cmd.add_argument("directory", type=Path, help="Directory to monitor")
        cmd.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE,
                         help=f"Baseline JSON file (default: {DEFAULT_BASELINE})")
    args = parser.parse_args()
    if args.command == "baseline":
        create_baseline(args.directory, args.baseline)
    else:
        check_baseline(args.directory, args.baseline)

if __name__ == "__main__":
    main()
