#!/usr/bin/env python3
"""Self-check for the advisory audit wrapper: python3 tests/test_audit.py"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent / "scripts" / "audit.py"

SPANISH = """# Guia de despliegue

La configuracion del servidor requiere una revision cuidadosa antes de cualquier
despliegue en produccion. Cada parametro debe verificarse contra el inventario
aprobado por el equipo responsable.

Los registros del sistema se conservan durante noventa dias. El equipo de
operaciones revisa los informes semanales y documenta cualquier incidencia
detectada durante ese periodo.

Cuando una incidencia afecta a los clientes, la comunicacion se envia dentro de
las primeras dos horas. El responsable de guardia coordina la respuesta y
registra las decisiones tomadas.
"""


def run(*args):
    return subprocess.run(
        [sys.executable, str(AUDIT), *args],
        text=True,
        capture_output=True,
    )


def scans_by_name(completed):
    report = json.loads(completed.stdout)
    return report, {s["name"]: s for s in report["files"][0]["scans"]}


def test_findings_report_is_advisory_and_exits_zero():
    completed = run("--", str(HERE / "fixtures" / "sample.md"))
    assert completed.returncode == 0, completed.stderr
    report, scans = scans_by_name(completed)
    assert report["advisory"] is True
    assert report["authority"] == "none"
    assert set(scans) == {"banned_phrases", "structure", "silhouette", "readability"}
    assert scans["banned_phrases"]["finding_status"] == "findings"


def test_unscannable_file_is_a_tool_failure_naming_the_path():
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp) / "empty.md"
        empty.write_text("   \n")
        completed = run("--", str(empty))
        assert completed.returncode == 3, completed.stdout
        assert "could not scan" in completed.stderr
        assert str(empty) in completed.stderr
        assert completed.stdout == ""


def test_batch_failure_names_the_offending_file():
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp) / "seventh.md"
        empty.write_text("\n")
        completed = run("--", str(HERE / "fixtures" / "sample.md"), str(empty))
        assert completed.returncode == 3, completed.stdout
        assert str(empty) in completed.stderr
        assert "sample.md" not in completed.stderr


def test_non_english_input_is_declined_by_every_scanner():
    with tempfile.TemporaryDirectory() as tmp:
        spanish = Path(tmp) / "es.md"
        spanish.write_text(SPANISH)
        completed = run("--", str(spanish))
    assert completed.returncode == 0, completed.stderr
    _, scans = scans_by_name(completed)
    for name, scan in scans.items():
        assert scan["finding_status"] == "clean_or_declined", name
        assert scan["result"]["non_english"] is True, name
        assert not scan["result"].get("flags"), name
        assert not scan["result"].get("violations"), name


def test_genre_reaches_the_genre_aware_scanners():
    sample = str(HERE / "fixtures" / "sample.md")
    default_report, default_scans = scans_by_name(run("--", sample))
    social_report, social_scans = scans_by_name(run("--genre", "social", "--", sample))
    assert default_report["genre"] == "docs"
    assert social_report["genre"] == "social"
    for name in ("structure", "silhouette"):
        assert default_scans[name]["result"]["genre"] == "docs", name
        assert social_scans[name]["result"]["genre"] == "social", name


def test_unsupported_genre_is_rejected():
    completed = run("--genre", "legalese", "--", str(HERE / "fixtures" / "sample.md"))
    assert completed.returncode == 2, completed.stdout
    assert completed.stdout == ""


def test_non_markdown_input_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        other = Path(tmp) / "notes.txt"
        other.write_text("hello\n")
        completed = run("--", str(other))
    assert completed.returncode == 2, completed.stdout


if __name__ == "__main__":
    for name, case in sorted(globals().items()):
        if name.startswith("test_"):
            case()
            print("ok", name)
