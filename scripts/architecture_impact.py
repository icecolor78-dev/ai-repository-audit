from __future__ import annotations

import ast
from collections import Counter, defaultdict
from pathlib import Path

CODE_SUFFIXES = {'.py','.js','.jsx','.ts','.tsx','.go','.rs','.java','.kt','.rb','.php','.cs','.c','.cc','.cpp','.swift'}


def _rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def _python_imports(path: Path):
    try:
        tree = ast.parse(path.read_text(encoding='utf-8', errors='replace'))
    except SyntaxError:
        return []
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out.extend(alias.name.split('.')[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            out.append(node.module.split('.')[0])
    return sorted(set(out))


def analyze(root: Path, revision: str) -> dict:
    files = sorted(p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts and p.suffix.lower() in CODE_SUFFIXES)
    top = sorted({Path(_rel(root,p)).parts[0] for p in files if len(Path(_rel(root,p)).parts) > 1 and not Path(_rel(root,p)).parts[0].startswith('.')})
    edges = []
    inbound = Counter()
    for p in files:
        if p.suffix.lower() != '.py':
            continue
        source = _rel(root,p)
        for target in _python_imports(p):
            if target in top:
                edges.append({'from':source,'to':target,'kind':'python_import'})
                inbound[target] += 1
    large = sorted(({'path':_rel(root,p),'bytes':p.stat().st_size} for p in files if p.stat().st_size > 100000), key=lambda x:x['bytes'], reverse=True)
    hotspots = [{'boundary':name,'inbound_static_refs':count} for name,count in inbound.most_common()]
    generated = sorted(_rel(root,p) for p in files if any(part.lower() in {'generated','vendor','dist','build'} for part in p.parts))
    return {
        'schema_version':'architecture-impact/v1',
        'subject_revision':revision,
        'top_level_boundaries':top,
        'dependency_edges':edges,
        'hotspots':hotspots,
        'large_files':large[:50],
        'generated_or_vendor_boundaries':generated[:100],
        'cycles':{'state':'UNVERIFIED','reason':'Cross-language static cycle detection is not established by this bounded analyzer.'},
        'change_impact':{'state':'PARTIAL' if top else 'UNVERIFIED','reason':'Static boundaries/imports indicate possible blast radius; history/runtime coupling is not inferred.'},
        'confidence':'PARTIAL' if files else 'UNVERIFIED',
        'unknowns':['Static imports and file layout do not prove runtime dependency direction, ownership, failure isolation, or defect probability.'],
    }
