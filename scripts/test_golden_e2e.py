from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from audit_v2 import compose_v2
from render_customer_report import render_customer_report

OBSERVED = "2026-09-11T19:20:00Z"


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    git(root, "init")
    git(root, "config", "user.email", "golden@example.invalid")
    git(root, "config", "user.name", "Golden Fixture")
    git(root, "remote", "add", "origin", "https://github.com/example/golden.git")

    (root / ".github/workflows").mkdir(parents=True)
    (root / "api").mkdir()
    (root / "src").mkdir()

    (root / "README.md").write_text(
        "# Golden fixture\nCI and release readiness are reviewed.\n",
        encoding="utf-8",
    )
    (root / "src/app.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "requirements.txt").write_text("requests>=2\n", encoding="utf-8")
    (root / "api/openapi.yaml").write_text(
        "openapi: 3.1.0\ncomponents:\n  schemas:\n    Thing:\n      $ref: './missing-schema.yaml#/Thing'\n",
        encoding="utf-8",
    )
    (root / ".github/workflows/ci.yml").write_text(
        "name: ci\n"
        "on: [push]\n"
        "jobs:\n"
        "  critical:\n"
        "    if: false\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - run: python -m pytest\n"
        "  reused:\n"
        "    uses: example/shared/.github/workflows/reuse.yml@main\n"
        "    secrets: inherit\n",
        encoding="utf-8",
    )

    git(root, "add", ".")
    git(root, "commit", "-m", "golden adversarial fixture")
    revision = git(root, "rev-parse", "HEAD")

    bundle = {
        "version": "audit-evidence/v1",
        "subject": {"repository": "example/golden", "revision": revision},
        "observed_at": OBSERVED,
        "workflow_runs": [
            {
                "name": "ci",
                "revision": revision,
                "status": "completed",
                "conclusion": "success",
                "source": "https://github.com/example/golden/actions/runs/1",
            }
        ],
        "test_runs": [],
        "release_runs": [],
        "runtime_measurements": [
            {
                "kind": "latency",
                "value": 42,
                "unit": "ms",
                "sample_count": 3,
                "environment": "public-ci-fixture",
                "revision": revision,
                "source": "https://github.com/example/golden/actions/runs/1",
            }
        ],
        "observability_artifacts": [
            {
                "kind": "logs",
                "revision": revision,
                "source": "https://github.com/example/golden/actions/runs/1",
            }
        ],
    }

    first = compose_v2(root, "example/golden", revision, "main", OBSERVED, bundle)
    second = compose_v2(root, "example/golden", revision, "main", OBSERVED, bundle)
    assert first == second

    assert first["subject"]["repository"] == "example/golden"
    assert first["subject"]["revision"] == revision
    assert first["external_execution_evidence"]["trust"] == "SUPPLIED_EXACT"
    assert first["runtime_evidence"]["trust"] == "SUPPLIED_EXACT"
    assert first["runtime_evidence"]["confidence"] == "PARTIAL"
    assert first["overall_portrait"]["verdict"] != "PASS"

    serialized = str(first)
    assert "if: false" in serialized or "if:false" in serialized or "skipped" in serialized.casefold()
    assert "@main" in serialized
    assert "missing-schema.yaml" in serialized
    assert "requirements.txt" in serialized

    report_first = render_customer_report(first)
    report_second = render_customer_report(second)
    assert report_first == report_second
    assert f"`{revision}`" in report_first
    assert "`example/golden`" in report_first
    assert "SUPPLIED_EXACT" in report_first
    assert "**PASS**" not in report_first
    assert "global_score" not in report_first
    assert "Explicit unknowns" in report_first
    assert "Interpretation boundary" in report_first

print("Golden adversarial end-to-end Audit tests passed")
