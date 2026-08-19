#!/usr/bin/env python3
"""Self-check for the advisory audit wrapper and the rewrite-preservation gate:
python3 tests/test_audit.py
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent / "scripts" / "audit.py"
VALIDATE = HERE.parent / "scripts" / "validate_preservation.py"

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

SPANISH_UNIFORM_CADENCE = """# Informe

El equipo revisa los registros del sistema durante la jornada laboral completa.
El equipo documenta las incidencias detectadas durante la jornada laboral completa.
El equipo comunica los resultados obtenidos durante la jornada laboral completa.
El equipo verifica los parametros aprobados durante la jornada laboral completa.
El equipo confirma los inventarios recibidos durante la jornada laboral completa.

El equipo coordina las respuestas emitidas durante la jornada laboral completa.
El equipo registra las decisiones tomadas durante la jornada laboral completa.
El equipo publica los informes semanales durante la jornada laboral completa.
El equipo archiva los expedientes cerrados durante la jornada laboral completa.
El equipo actualiza los procedimientos vigentes durante la jornada laboral completa.
"""

BUZZWORDS = """# Roadmap

## Q3

- Leverage synergies
- Streamline workflows
- Unlock value
- Drive alignment
- Empower stakeholders
- Optimize throughput
- Accelerate delivery
- Maximize impact
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


def test_runs_with_an_isolated_module_path_and_through_a_symlink():
    with tempfile.TemporaryDirectory() as tmp:
        link = Path(tmp) / "unslop-audit"
        link.symlink_to(AUDIT)
        completed = subprocess.run(
            [sys.executable, str(link), "--", str(HERE / "fixtures" / "sample.md")],
            text=True,
            capture_output=True,
            env=dict(os.environ, PYTHONSAFEPATH="1"),
        )
    assert completed.returncode == 0, completed.stderr
    _, scans = scans_by_name(completed)
    assert scans["banned_phrases"]["finding_status"] == "findings"


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


def test_mixed_verdict_preserves_language_aware_findings():
    with tempfile.TemporaryDirectory() as tmp:
        buzzwords = Path(tmp) / "roadmap.md"
        buzzwords.write_text(BUZZWORDS)
        completed = run("--", str(buzzwords))
    assert completed.returncode == 0, completed.stderr
    _, scans = scans_by_name(completed)

    assert scans["structure"]["result"]["non_english"] is True
    assert scans["silhouette"]["result"]["non_english"] is True

    banned = scans["banned_phrases"]
    assert banned["finding_status"] == "findings"
    assert not banned["result"].get("non_english")
    assert [v["phrase"] for v in banned["result"]["violations"]] == ["leverage synerg"]


def test_readability_is_declined_even_when_another_scanner_flags():
    with tempfile.TemporaryDirectory() as tmp:
        spanish = Path(tmp) / "informe.md"
        spanish.write_text(SPANISH_UNIFORM_CADENCE)
        completed = run("--", str(spanish))
    assert completed.returncode == 0, completed.stderr
    _, scans = scans_by_name(completed)

    structure = scans["structure"]
    assert structure["finding_status"] == "findings"
    assert not structure["result"].get("non_english")
    assert {flag["metric"] for flag in structure["result"]["flags"]} == {
        "sentence_burstiness",
        "opener_repetition",
    }

    readability = scans["readability"]
    assert readability["finding_status"] == "clean_or_declined"
    assert readability["result"]["non_english"] is True
    assert readability["result"]["flags"] == []
    assert "flesch_kincaid_grade" not in readability["result"]


def test_english_text_keeps_its_readability_metrics():
    completed = run("--", str(HERE / "fixtures" / "sample.md"))
    assert completed.returncode == 0, completed.stderr
    _, scans = scans_by_name(completed)
    readability = scans["readability"]
    assert not readability["result"].get("non_english")
    assert "flesch_kincaid_grade" in readability["result"]


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


ORIGINAL = """# Launch notes

In today's fast-paced world, it's not just about shipping - it's about
delivering value. We leverage synergies across the stack to unlock outcomes.

The migration runs on 2026-03-14 and moves 42 tables to Postgres 16.
Run `pg_dump --format=custom` first; a failed cutover may lose writes.
"""

FACT_DESTROYING_REWRITE = """# Launch notes

Shipping matters less than the value we deliver.

The migration moves the tables to Postgres. Run a dump first.
"""

MINIMAL_REPAIR = """# Launch notes

This release is not only about shipping the code - it is also about
delivering value. We reuse the same queue layer across the stack to cut work.

The migration runs on 2026-03-14 and moves 42 tables to Postgres 16.
Run `pg_dump --format=custom` first; a failed cutover may lose writes.
"""


def validate(*args):
    return subprocess.run(
        [sys.executable, str(VALIDATE), *args],
        text=True,
        capture_output=True,
    )


def test_a_rewrite_that_drops_facts_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        original = Path(tmp) / "original.md"
        proposed = Path(tmp) / "proposed.md"
        original.write_text(ORIGINAL)
        proposed.write_text(FACT_DESTROYING_REWRITE)
        completed = validate(str(original), str(proposed))
    assert completed.returncode == 1, completed.stdout
    result = json.loads(completed.stdout)
    assert result["passed"] is False
    lost = {item["value"] for item in result["missing"]}
    assert "2026-03-14" in lost
    assert "`pg_dump --format=custom`" in lost


def test_a_minimal_repair_passes_strict_validation():
    with tempfile.TemporaryDirectory() as tmp:
        original = Path(tmp) / "original.md"
        proposed = Path(tmp) / "proposed.md"
        original.write_text(ORIGINAL)
        proposed.write_text(MINIMAL_REPAIR)
        completed = validate("--strict", str(original), str(proposed))
    assert completed.returncode == 0, completed.stdout
    result = json.loads(completed.stdout)
    assert result["passed"] is True
    assert result["missing"] == []
    assert result["warnings"] == []
    assert result["preserved"] == result["total_constraints"] > 0


if __name__ == "__main__":
    for name, case in sorted(globals().items()):
        if name.startswith("test_"):
            case()
            print("ok", name)
