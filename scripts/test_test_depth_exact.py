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

print("Exact test-depth tests passed")
