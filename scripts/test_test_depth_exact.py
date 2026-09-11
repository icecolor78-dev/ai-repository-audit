from __future__ import annotations

import tempfile
from pathlib import Path

from test_depth_exact import profile_tests


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "tests").mkdir()
    for index in range(120):
        (root / "tests" / f"test_{index:03d}.py").write_text("def test_x(): pass\n", encoding="utf-8")
    profile = profile_tests(root)
    assert len(profile["suites"]) == 120
    assert profile["exact_subject_execution"] == []
    assert profile["confidence"] == "PARTIAL"
    assert profile["subsystem_map"]

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "tests").mkdir()
    (root / "tests" / "spec.txt").write_text("not an executable test suite\n", encoding="utf-8")
    (root / "tests" / "integration_api.py").write_text("def test_api(): pass\n", encoding="utf-8")
    (root / "README-spec.md").write_text("specification only\n", encoding="utf-8")
    profile = profile_tests(root)
    assert "tests/spec.txt" not in profile["suites"]
    assert "README-spec.md" not in profile["suites"]
    assert "tests/integration_api.py" in profile["suites"]
    assert "integration" in profile["types"]
    assert profile["exact_subject_execution"] == []

print("Exact test-depth tests passed")
