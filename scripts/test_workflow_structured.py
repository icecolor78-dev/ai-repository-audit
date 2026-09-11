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
    assert {"privileged_pr_context","privileged_untrusted_checkout","untrusted_expression_shell","broad_permissions","mutable_action_ref"} <= kinds

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    write(root, "reusable.yml", """
on: [push]
permissions:
  id-token: write
  contents: read
jobs:
  explicit-empty:
    permissions: {}
    steps:
      - run: echo no oidc here
  delegated:
    uses: example/reusable/.github/workflows/build.yml@main
    secrets: inherit
""")
    _, security, release = analyze_workflows(root)
    kinds = {item["kind"] for item in security["signals"]}
    assert "mutable_reusable_workflow_ref" in kinds
    assert "reusable_workflow_secrets" in kinds
    oidc = [item for item in release["signals"] if item["kind"] == "oidc_permission"]
    assert not any("explicit-empty" in item["locator"] for item in oidc)
    assert any("delegated" in item["locator"] for item in oidc)

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    write(root, "skip.yml", """
on: [pull_request]
jobs:
  critical-tests:
    if: false
    steps:
      - run: pytest
  aggregate:
    needs: [critical-tests]
    steps:
      - run: echo green
""")
    ci, security, _ = analyze_workflows(root)
    assert any(item["kind"] == "statically_skipped_job" for item in security["signals"])
    assert any("aggregate" in item for item in ci["aggregate_checks"])

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    write(root, "release.yml", """
on:
  push:
    tags: ['v*']
jobs:
  words-only:
    steps:
      - run: echo "do not publish this"
  publisher:
    steps:
      - uses: pypa/gh-action-pypi-publish@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
""")
    _, _, release = analyze_workflows(root)
    assert release["workflows"] == [".github/workflows/release.yml"]

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    write(root, "not-release.yml", """
on: [push]
jobs:
  note:
    steps:
      - run: echo "do not publish this"
""")
    _, _, release = analyze_workflows(root)
    assert release["workflows"] == []

print("Structured workflow adversarial tests passed")
