#!/usr/bin/env python3
"""Self-check for the advisory audit wrapper: python3 tests/test_audit.py"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent / "scripts" / "audit.py"


def run(*paths):
    return subprocess.run(
        [sys.executable, str(AUDIT), "--", *paths],
        text=True,
        capture_output=True,
    )


def test_findings_report_is_advisory_and_exits_zero():
    completed = run(str(HERE / "fixtures" / "sample.md"))
    assert completed.returncode == 0, completed.stderr
    report = json.loads(completed.stdout)
    assert report["advisory"] is True
    assert report["authority"] == "none"
    scans = {scan["name"]: scan for scan in report["files"][0]["scans"]}
    assert set(scans) == {"banned_phrases", "structure", "silhouette", "readability"}
    assert scans["banned_phrases"]["finding_status"] == "findings"


def test_unscannable_file_is_a_tool_failure_not_findings():
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp) / "empty.md"
        empty.write_text("   \n")
        completed = run(str(empty))
    assert completed.returncode == 3, completed.stdout
    assert "could not scan the file" in completed.stderr
    assert completed.stdout == ""


def test_non_markdown_input_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        other = Path(tmp) / "notes.txt"
        other.write_text("hello\n")
        completed = run(str(other))
    assert completed.returncode == 2, completed.stdout


if __name__ == "__main__":
    for name, case in sorted(globals().items()):
        if name.startswith("test_"):
            case()
            print("ok", name)
