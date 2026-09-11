from __future__ import annotations

import re
from pathlib import Path

FULL_SHA = re.compile(r"@[0-9a-f]{40}(?:\s|$)")


def _rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def _risk(kind: str, locator: str, detail: str, severity: str = "MEDIUM") -> dict:
    return {"kind": kind, "locator": locator, "detail": detail, "severity": severity, "confidence": "HIGH"}


def analyze(root: Path, revision: str) -> dict:
    workflows = sorted(p for p in root.glob('.github/workflows/*') if p.suffix in {'.yml', '.yaml'})
    profiles, risks = [], []
    for path in workflows:
        rp = _rel(root, path)
        text = path.read_text(encoding='utf-8', errors='replace')
        path_filters = bool(re.search(r"(?m)^\s*paths(?:-ignore)?\s*:", text))
        conditionals = bool(re.search(r"(?m)^\s*if\s*:", text))
        matrix = bool(re.search(r"(?m)^\s*matrix\s*:", text))
        permissions = bool(re.search(r"(?m)^\s*permissions\s*:", text))
        pull_request_target = bool(re.search(r"(?m)^\s*pull_request_target\s*:", text))
        release_only = bool(re.search(r"(?mi)^\s*(release|workflow_dispatch)\s*:", text)) and not bool(re.search(r"(?mi)^\s*pull_request\s*:", text))
        action_refs = re.findall(r"(?m)^\s*uses:\s*([^\s#]+)", text)
        mutable = [ref for ref in action_refs if not ref.startswith('./') and not re.search(r"@[0-9a-f]{40}$", ref)]
        if path_filters: risks.append(_risk('path_filter_false_green', rp, 'Path filters can leave repository changes outside this workflow.'))
        if conditionals: risks.append(_risk('conditional_false_green', rp, 'Conditional jobs/steps can produce green workflow status without executing all intended evidence.'))
        if mutable: risks.append(_risk('mutable_action_ref', rp, f"Mutable third-party refs observed: {', '.join(mutable[:8])}", 'LOW'))
        if pull_request_target: risks.append(_risk('privileged_pr_context', rp, 'pull_request_target executes in a privileged base-repository context.', 'HIGH'))
        if release_only: risks.append(_risk('release_only_gap', rp, 'Release/manual-only evidence is not equivalent to pull-request evidence.', 'LOW'))
        profiles.append({
            'workflow': rp,
            'path_filters': path_filters,
            'conditionals': conditionals,
            'matrix': matrix,
            'permissions_declared': permissions,
            'pull_request_target': pull_request_target,
            'release_only': release_only,
            'action_refs': action_refs,
            'mutable_action_refs': mutable,
        })
    risk_order = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
    max_risk = max((risk_order[r['severity']] for r in risks), default=0)
    return {
        'schema_version': 'ci-evidence-profile/v1',
        'subject_revision': revision,
        'workflows': profiles,
        'false_green_risks': risks,
        'false_green_risk': {0: 'UNVERIFIED', 1: 'LOW', 2: 'MEDIUM', 3: 'HIGH'}[max_risk],
        'required_checks': {'state': 'UNVERIFIED', 'reason': 'Repository workflow files do not prove branch/ruleset enforcement.'},
        'exact_subject_runs': [],
        'confidence': 'PARTIAL' if workflows else 'UNVERIFIED',
        'unknowns': ['Workflow definitions do not prove that a check was required, executed, successful, or bound to this exact revision.'],
    }
