from __future__ import annotations

import tempfile
from pathlib import Path

from claims_exact import extract_readme_claims, selected_readme


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "README.md").write_text(
        "Tests pass in CI and this release is production ready.\n"
        "Tests never run in CI and this release is not production ready.\n",
        encoding="utf-8",
    )
    claims = extract_readme_claims(root)
    assert len(claims) == 2
    assert claims[0]["claim"] != claims[1]["claim"]
    assert "not production ready" in claims[1]["claim"]
    assert all(item["state"] == "UNVERIFIED" for item in claims)
    assert claims[0]["notes"].startswith("README.md:1")
    assert claims[1]["notes"].startswith("README.md:2")

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "README.rst").write_text("Security tests are described here.\n", encoding="utf-8")
    assert selected_readme(root).name == "README.rst"
    claims = extract_readme_claims(root)
    assert len(claims) == 1
    assert claims[0]["source_ref"] == "readme"
    assert claims[0]["notes"].startswith("README.rst:1")
    assert claims[0]["state"] == "UNVERIFIED"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "README.txt").write_text("Release process is documented.\n", encoding="utf-8")
    claims = extract_readme_claims(root)
    assert len(claims) == 1
    assert claims[0]["notes"].startswith("README.txt:1")

print("Exact claim preservation tests passed")
