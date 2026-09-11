from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
WORKFLOW_SUFFIXES = {".yml", ".yaml"}
LANGUAGE_SUFFIXES = {".py": "Python", ".rs": "Rust", ".go": "Go", ".ts": "TypeScript", ".tsx": "TypeScript", ".js": "JavaScript", ".jsx": "JavaScript", ".java": "Java", ".kt": "Kotlin", ".rb": "Ruby", ".php": "PHP", ".cs": "C#", ".cpp": "C++", ".cc": "C++", ".c": "C", ".swift": "Swift", ".scala": "Scala"}
MANIFESTS = {"pyproject.toml", "setup.py", "setup.cfg", "package.json", "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "build.gradle.kts", "Gemfile", "composer.json", "requirements.txt"}
LOCKFILES = {"uv.lock", "poetry.lock", "pdm.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb", "Cargo.lock", "go.sum", "Gemfile.lock", "composer.lock"}
TEST_HINTS = {"pytest": "unit/integration", "unittest": "unit", "playwright": "end-to-end", "cypress": "end-to-end", "vitest": "unit/integration", "jest": "unit/integration", "tox": "compatibility", "nox": "compatibility", "fuzz": "fuzz", "benchmark": "performance", "contract": "contract", "smoke": "smoke", "e2e": "end-to-end"}
CLAIM_PATTERNS = [(re.compile(r"\bCI\b|continuous integration", re.I), "CI is present/used"), (re.compile(r"\btests?\b|tested", re.I), "tests are present/used"), (re.compile(r"release|publish|PyPI|npm", re.I), "release or publishing path is described"), (re.compile(r"security|secure|vulnerability", re.I), "security property or process is described")]


def files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts)


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def workflow_profile(root: Path, all_files: list[Path]) -> tuple[dict, list[dict]]:
    workflows = [p for p in all_files if ".github/workflows" in rel(root, p) and p.suffix in WORKFLOW_SUFFIXES]
    names, triggers, filters, matrices, conditionals, aggregates, permissions, action_refs, sources = [], [], [], [], [], [], [], [], []
    for path in workflows:
        text = path.read_text(encoding="utf-8", errors="replace")
        rp = rel(root, path)
        names.append(rp)
        for token in ("pull_request", "push", "workflow_dispatch", "workflow_run", "schedule", "release"):
            if re.search(rf"(?m)^\s*{re.escape(token)}\s*:", text): triggers.append(f"{rp}: {token}")
        if re.search(r"(?m)^\s*paths(?:-ignore)?\s*:", text): filters.append(f"{rp}: path filter present")
        if re.search(r"(?m)^\s*matrix\s*:", text): matrices.append(f"{rp}: matrix present")
        if re.search(r"(?m)^\s*if\s*:", text): conditionals.append(f"{rp}: conditional job/step present")
        if re.search(r"(?m)^\s*needs\s*:", text): aggregates.append(f"{rp}: dependency/aggregate signal present")
        for match in re.finditer(r"(?m)^\s*permissions\s*:\s*(.*)$", text): permissions.append(f"{rp}: permissions {match.group(1).strip() or 'mapping'}")
        for match in re.finditer(r"uses:\s*([^\s#]+)", text):
            ref = match.group(1)
            if ref.startswith("./"): continue
            action_refs.append(f"{rp}: {ref}" + (" [mutable-ref-signal]" if "@" in ref and not re.search(r"@[0-9a-f]{40}$", ref) else ""))
        sources.append({"id": f"workflow-{len(sources)+1}", "kind": "workflow_definition", "locator": rp, "supports": ["workflow definition", "CI profiler signals"], "limits": ["definition does not prove execution"]})
    confidence = "PARTIAL" if workflows else "UNVERIFIED"
    return {"workflows": names, "required_checks": [], "trigger_model": sorted(set(triggers)), "path_filters": sorted(set(filters)), "runtime_matrix": sorted(set(matrices)), "os_arch_matrix": [], "conditional_jobs": sorted(set(conditionals)), "aggregate_checks": sorted(set(aggregates)), "exact_subject_runs": [], "confidence": confidence, "unknowns": ["workflow execution and required-check enforcement require external exact-subject evidence"], "pr_confidence": confidence, "main_confidence": confidence, "release_confidence": "UNVERIFIED", "security_evidence_freshness": "UNVERIFIED", "_permissions": permissions, "_action_refs": action_refs}, sources


def test_profile(root: Path, all_files: list[Path]) -> dict:
    candidates, types = [], set()
    for path in all_files:
        rp = rel(root, path)
        low = rp.lower()
        if any(part in low for part in ("test", "spec", "__tests__")):
            candidates.append(rp)
        for hint, kind in TEST_HINTS.items():
            if hint in low: types.add(kind)
    confidence = "PARTIAL" if candidates else "UNVERIFIED"
    return {"suites": candidates[:100], "types": sorted(types), "subsystem_map": [], "exact_subject_execution": [], "confidence": confidence, "unknowns": ["file/config discovery does not prove execution or semantic completeness"]}


def claims(root: Path) -> list[dict]:
    docs = [p for p in [root / "README.md", root / "README.rst", root / "README.txt"] if p.is_file()]
    items = []
    for path in docs:
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, label in CLAIM_PATTERNS:
            if pattern.search(text):
                items.append({"claim": label, "source_ref": "readme", "state": "UNVERIFIED", "supporting_refs": [], "contradicting_refs": [], "notes": "Claim discovered from README text; evidence binding requires a separate matcher."})
    return items


def extract(root: Path, repository: str, revision: str, default_branch: str, observed_at: str) -> dict:
    if not SHA_RE.fullmatch(revision): raise SystemExit("revision must be a lowercase full 40-hex SHA")
    all_files = files(root)
    langs = sorted({LANGUAGE_SUFFIXES[p.suffix.lower()] for p in all_files if p.suffix.lower() in LANGUAGE_SUFFIXES})
    manifests = sorted(rel(root, p) for p in all_files if p.name in MANIFESTS)
    lockfiles = sorted(rel(root, p) for p in all_files if p.name in LOCKFILES)
    modules = sorted(p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
    ci, workflow_sources = workflow_profile(root, all_files)
    permissions, action_refs = ci.pop("_permissions"), ci.pop("_action_refs")
    test = test_profile(root, all_files)
    source_rows = [{"id": "readme", "kind": "repository_file", "locator": "README.md", "supports": ["public claims"], "limits": ["claim text does not prove claim"]}] if (root / "README.md").is_file() else []
    source_rows += workflow_sources
    for row in source_rows:
        row.update({"subject_revision": revision, "observed_at": observed_at, "freshness": {"state": "exact", "reason": "local tree supplied for exact subject"}, "access": {"state": "accessible"}})
    portrait = {
      "schema_version": "rem/v1", "subject": {"provider": "github", "repository": repository, "revision": revision, "default_branch": default_branch, "observed_at": observed_at, "visibility": "public"},
      "inventory": {"languages": langs, "manifests": manifests, "lockfiles": lockfiles, "modules": modules, "generated_or_vendor_boundaries": []},
      "ci": ci,
      "tests": test,
      "security": {"workflow_permissions": permissions, "credential_persistence": [], "action_pinning": action_refs, "static_analysis": [], "dependency_security": [], "secret_scanning_evidence": [], "freshness": [], "confidence": "PARTIAL" if permissions or action_refs else "UNVERIFIED", "unknowns": ["workflow text signals do not establish vulnerability absence or scanner freshness"]},
      "release": {"workflows": [w for w in ci["workflows"] if re.search(r"release|publish", w, re.I)], "artifact_handoffs": [], "source_artifact_binding": [], "trusted_publishing": [], "signing_or_attestation": [], "smoke_or_release_tests": [], "rollback_or_recovery": [], "confidence": "UNVERIFIED", "unknowns": ["release success and artifact provenance require execution evidence"]},
      "supply_chain": {"dependencies": manifests + lockfiles, "update_automation": [], "sbom": [], "license_evidence": [], "provenance": [], "confidence": "PARTIAL" if manifests or lockfiles else "UNVERIFIED", "unknowns": ["dependency presence is not a vulnerability, license or provenance audit"]},
      "claims": {"items": claims(root)},
      "provenance": {"ai_assisted_changes": [], "generated_code": [], "external_build_or_test_services": [], "confidence": "UNVERIFIED", "unknowns": ["change authorship/provenance requires explicit evidence"]},
      "coverage": {"dimensions": ["inventory", "workflow definitions", "test discovery", "README claim discovery"], "explicit_unknowns": ["workflow executions", "required-check enforcement", "external security freshness", "release success", "runtime behavior", "claim verification"], "excluded_scope": ["penetration testing", "certification", "production runtime behavior"]},
      "sources": source_rows
    }
    return portrait


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path); parser.add_argument("--repository", required=True); parser.add_argument("--revision", required=True); parser.add_argument("--default-branch", default="main"); parser.add_argument("--observed-at", default=None)
    args = parser.parse_args()
    observed = args.observed_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    print(json.dumps(extract(args.root.resolve(), args.repository, args.revision, args.default_branch, observed), indent=2, sort_keys=True))

if __name__ == "__main__": main()
