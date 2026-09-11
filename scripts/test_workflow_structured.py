from __future__ import annotations

import tempfile
from pathlib import Path

from workflow_structured import analyze_workflows


def write(root: Path, name: str, text: str) -> None:
    path = root / ".github" / "workflows" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    write(root, "safe.yml", """
on: [pull_request_target]
permissions:
  contents: read
jobs:
  label:
    steps:
      - uses: actions/labeler@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
      - run: echo safe
""")
    ci, security, release = analyze_workflows(root)
    by_kind = {}
    for item in security["signals"]:
        by_kind.setdefault(item["kind"], []).append(item)
    assert by_kind["privileged_pr_context"][0]["severity"] == "INFO"
    assert "privileged_untrusted_checkout" not in by_kind
    assert release["workflows"] == []
    assert ci["exact_subject_runs"] == []

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    write(root, "danger.yml", """
on: [pull_request_target]
permissions: write-all
jobs:
  dangerous:
    steps:
      - uses: actions/checkout@v4
        with:
          repository: ${{ github.event.pull_request.head.repo.full_name }}
          ref: ${{ github.event.pull_request.head.sha }}
      - run: |
          echo "${{ github.event.issue.title }}"
""")
    _, security, _ = analyze_workflows(root)
    kinds = {item["kind"] for item in security["signals"]}
    assert "privileged_pr_context" in kinds
    assert "privileged_untrusted_checkout" in kinds
    assert "untrusted_expression_shell" in kinds
    assert "broad_permissions" in kinds
    assert "mutable_action_ref" in kinds

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    write(root, "ci.yml", """
on: [push]
permissions:
  id-token: write
  contents: read
jobs:
  test:
    steps:
      - run: npm test
""")
    _, _, release = analyze_workflows(root)
    assert release["workflows"] == []
    assert release["trusted_publishing"] == []
    assert any(item["kind"] == "oidc_permission" for item in release["signals"])

print("Structured workflow adversarial tests passed")
