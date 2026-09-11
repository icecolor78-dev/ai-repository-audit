from __future__ import annotations

import json
import tempfile
from pathlib import Path

from supply_chain_exact import analyze_supply_chain


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / ".github").mkdir()
    (root / "vendor").mkdir()
    (root / "requirements.txt").write_text(
        "alpha==1.2.3 --hash=sha256:abcdef\nbeta>=2\n",
        encoding="utf-8",
    )
    (root / "package-lock.json").write_text(
        json.dumps({
            "lockfileVersion": 3,
            "packages": {
                "": {"name": "fixture", "version": "1.0.0"},
                "node_modules/demo": {"version": "2.3.4", "integrity": "sha512-AAAA"},
            },
        }),
        encoding="utf-8",
    )
    (root / "Cargo.lock").write_text(
        'version = 3\n[[package]]\nname = "cratex"\nversion = "0.4.2"\nchecksum = "deadbeef"\n',
        encoding="utf-8",
    )
    (root / "go.sum").write_text(
        "example.com/mod v1.2.0 h1:abc=\nexample.com/mod v1.2.0/go.mod h1:def=\n",
        encoding="utf-8",
    )
    (root / ".github" / "dependabot.yml").write_text("version: 2\nupdates: []\n", encoding="utf-8")
    (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (root / "sbom.spdx.json").write_text("{}\n", encoding="utf-8")
    (root / "vendor" / "copied.py").write_text("x = 1\n", encoding="utf-8")

    result = analyze_supply_chain(root)
    deps = "\n".join(result["dependencies"])
    provenance = "\n".join(result["provenance"])
    assert "python:alpha==1.2.3" in deps
    assert "python:beta" not in deps
    assert "npm:demo@2.3.4" in deps
    assert "cargo:cratex@0.4.2" in deps
    assert "go:example.com/mod@v1.2.0" in deps
    assert "python-integrity:alpha sha256:abcdef" in provenance
    assert "npm-integrity:demo sha512-AAAA" in provenance
    assert "cargo-checksum:cratex deadbeef" in provenance
    assert "go-integrity:example.com/mod@v1.2.0 h1:abc=" in provenance
    assert any("dependabot.yml" in x for x in result["update_automation"])
    assert result["sbom"] == ["sbom.spdx.json"]
    assert result["license_evidence"] == ["LICENSE"]
    assert any(x.startswith("generated-or-vendor-boundary:vendor/") for x in result["provenance"])
    assert result["confidence"] == "PARTIAL"
    assert result["unknowns"]

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "package-lock.json").write_text("{not-json", encoding="utf-8")
    result = analyze_supply_chain(root)
    assert any(x == "parse-unavailable:package-lock.json" for x in result["provenance"])
    assert result["confidence"] == "PARTIAL"
    assert not any(x.startswith("npm:") for x in result["dependencies"])

with tempfile.TemporaryDirectory() as tmp:
    result = analyze_supply_chain(Path(tmp))
    assert result["confidence"] == "UNVERIFIED"
    assert result["dependencies"] == []

print("Supply-chain evidence tests passed")
