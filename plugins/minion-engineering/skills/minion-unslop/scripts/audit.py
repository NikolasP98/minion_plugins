#!/usr/bin/env python3
"""Run vendored UNSLOP scanners without treating findings as failures."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

HERE = Path(__file__).resolve().parent
GENRES = ("prose", "docs", "social")
SCANNERS = (
    ("banned_phrases", "banned_phrase_scan.py", False),
    ("structure", "structure_scan.py", True),
    ("silhouette", "silhouette_scan.py", True),
    ("readability", "readability_metrics.py", False),
)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Advisory-only deterministic audit of Markdown files."
    )
    parser.add_argument("files", nargs="+", help="Markdown files to scan")
    parser.add_argument(
        "--genre",
        choices=GENRES,
        default="docs",
        help="threshold profile for the structure and silhouette scans (default: docs)",
    )
    return parser.parse_args(argv)


def run_scanner(
    name: str, script: str, genre_aware: bool, path: Path, genre: str
) -> Dict[str, Any]:
    options = ["--genre", genre] if genre_aware else []
    command = [sys.executable, str(HERE / script), *options, str(path)]
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(command, text=True, capture_output=True, env=environment)
    if completed.returncode not in (0, 1):
        detail = completed.stderr.strip() or completed.stdout.strip() or "no diagnostic"
        raise RuntimeError(
            f"{name} failed on {path} with exit {completed.returncode}: {detail}"
        )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{name} emitted invalid JSON for {path}: {exc}") from exc
    if not isinstance(result, dict):
        raise RuntimeError(f"{name} emitted a non-object JSON result for {path}")
    if result.get("error"):
        raise RuntimeError(f"{name} could not scan {path}: {result['error']}")
    return {
        "name": name,
        "finding_status": "findings" if completed.returncode == 1 else "clean_or_declined",
        "result": result,
    }


def enforce_english_only(scans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """UNSLOP judges English prose only. Once any language-aware scanner has
    declined a file, no scanner may report findings against it."""
    if not any(scan["result"].get("non_english") for scan in scans):
        return scans
    for scan in scans:
        if scan["result"].get("non_english"):
            continue
        scan["finding_status"] = "clean_or_declined"
        scan["result"] = {
            "non_english": True,
            "flags": [],
            "note": "scanner is not language-aware; declined because the "
            "language-aware scanners found non-English input",
        }
    return scans


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    paths = [Path(raw) for raw in args.files]
    for path in paths:
        if not path.is_file():
            print(f"error: not a readable file: {path}", file=sys.stderr)
            return 2
        if path.suffix.lower() not in (".md", ".markdown"):
            print(f"error: expected a Markdown file: {path}", file=sys.stderr)
            return 2

    report: Dict[str, Any] = {
        "advisory": True,
        "authority": "none",
        "genre": args.genre,
        "files": [],
    }
    try:
        for path in paths:
            scans = [
                run_scanner(name, script, genre_aware, path, args.genre)
                for name, script, genre_aware in SCANNERS
            ]
            report["files"].append(
                {"path": str(path), "scans": enforce_english_only(scans)}
            )
    except (OSError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
