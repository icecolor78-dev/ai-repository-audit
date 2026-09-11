from __future__ import annotations

import tempfile
from pathlib import Path

from architecture_exact import analyze_architecture, analyze_contract_drift


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "pkg").mkdir()
    (root / "web").mkdir()
    (root / "api").mkdir()
    (root / "pkg" / "a.py").write_text("from pkg import b\n", encoding="utf-8")
    (root / "pkg" / "b.py").write_text("from pkg import c\n", encoding="utf-8")
    (root / "pkg" / "c.py").write_text("from pkg import a\n", encoding="utf-8")
    (root / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    (root / "web" / "a.ts").write_text("import x from './b'\n", encoding="utf-8")
    (root / "web" / "b.ts").write_text("export default 1\n", encoding="utf-8")
    (root / "api" / "openapi.yaml").write_text(
        "openapi: 3.1.0\ncomponents:\n  schemas:\n    X:\n      $ref: './missing.yaml'\n",
        encoding="utf-8",
    )

    arch = analyze_architecture(root)
    edges = "\n".join(arch["dependency_edges"])
    assert "pkg/a.py -> pkg/b.py" in edges
    assert "pkg/b.py -> pkg/c.py" in edges
    assert "pkg/c.py -> pkg/a.py" in edges
    assert "web/a.ts -> web/b.ts" in edges
    assert arch["cycles"]
    assert arch["confidence"] == "PARTIAL"
    assert arch["change_impact"] == "PARTIAL"
    assert "api/openapi.yaml" in arch["api_contract_signals"]
    assert arch["unknowns"]

    drift = analyze_contract_drift(root)
    assert drift["surfaces"] == ["api/openapi.yaml"]
    assert drift["broken_local_refs"] == ["missing-ref:api/openapi.yaml->./missing.yaml"]
    assert drift["confidence"] == "PARTIAL"
    assert drift["unknowns"]

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "schema.json").write_text('{"$schema":"x","$ref":"#/defs/X"}', encoding="utf-8")
    drift = analyze_contract_drift(root)
    assert drift["broken_local_refs"] == []
    assert drift["confidence"] == "PARTIAL"

with tempfile.TemporaryDirectory() as tmp:
    arch = analyze_architecture(Path(tmp))
    drift = analyze_contract_drift(Path(tmp))
    assert arch["confidence"] == "UNVERIFIED"
    assert drift["confidence"] == "UNVERIFIED"

print("Architecture and contract-drift tests passed")
