from __future__ import annotations

import ast
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

JS_IMPORT = re.compile(r"(?:from\s+|import\s*\(\s*|require\s*\(\s*)['\"]([^'\"]+)['\"]")
YAML_REF = re.compile(r"\$ref\s*:\s*['\"]?([^'\"\s#]+)")
CONTRACT_NAMES = re.compile(r"(?:openapi|swagger|asyncapi|schema|graphql|\.proto$)", re.I)
SOURCE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx"}


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _source_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.casefold() in SOURCE_SUFFIXES and ".git" not in p.parts)


def _module_index(root: Path, files: list[Path]) -> dict[str, str]:
    index: dict[str, str] = {}
    for path in files:
        rp = _rel(root, path)
        if path.suffix == ".py":
            parts = list(path.relative_to(root).with_suffix("").parts)
            if parts and parts[-1] == "__init__":
                parts = parts[:-1]
            if parts:
                index[".".join(parts)] = rp
        else:
            stem = path.relative_to(root).with_suffix("").as_posix()
            index[stem] = rp
            if stem.endswith("/index"):
                index[stem[:-6]] = rp
    return index


def _python_edges(root: Path, path: Path, index: dict[str, str]) -> list[tuple[str, str]]:
    source = _rel(root, path)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return []
    edges: set[tuple[str, str]] = set()
    current_parts = list(path.relative_to(root).with_suffix("").parts)
    if current_parts and current_parts[-1] == "__init__":
        current_parts = current_parts[:-1]
    package = current_parts[:-1]
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                prefix = package[: max(0, len(package) - node.level + 1)]
                base = ".".join([*prefix, *([base] if base else [])])
            if base:
                names.append(base)
        for name in names:
            parts = name.split(".")
            while parts:
                candidate = ".".join(parts)
                if candidate in index:
                    target = index[candidate]
                    if target != source:
                        edges.add((source, target))
                    break
                parts.pop()
    return sorted(edges)


def _resolve_js(root: Path, source: Path, spec: str, index: dict[str, str]) -> str | None:
    if not spec.startswith("."):
        return None
    base = (source.parent / spec).resolve()
    try:
        rel = base.relative_to(root.resolve()).as_posix()
    except ValueError:
        return None
    candidates = [rel, f"{rel}/index"]
    for suffix in ("", ".js", ".jsx", ".ts", ".tsx"):
        key = rel + suffix if suffix else rel
        p = root / key
        if p.is_file() and p.suffix.casefold() in SOURCE_SUFFIXES:
            return _rel(root, p)
    for key in candidates:
        if key in index:
            return index[key]
    return None


def _js_edges(root: Path, path: Path, index: dict[str, str]) -> list[tuple[str, str]]:
    source = _rel(root, path)
    text = path.read_text(encoding="utf-8", errors="replace")
    edges: set[tuple[str, str]] = set()
    for spec in JS_IMPORT.findall(text):
        target = _resolve_js(root, path, spec, index)
        if target and target != source:
            edges.add((source, target))
    return sorted(edges)


def _cycles(edges: list[tuple[str, str]]) -> list[str]:
    graph: dict[str, set[str]] = defaultdict(set)
    for src, dst in edges:
        graph[src].add(dst)
    found: set[tuple[str, ...]] = set()
    visiting: list[str] = []
    active: set[str] = set()
    done: set[str] = set()

    def visit(node: str) -> None:
        if node in done:
            return
        active.add(node); visiting.append(node)
        for nxt in sorted(graph.get(node, ())):
            if nxt in active:
                start = visiting.index(nxt)
                cycle = visiting[start:] + [nxt]
                body = cycle[:-1]
                if body:
                    rotations = [tuple(body[i:] + body[:i]) for i in range(len(body))]
                    canonical = min(rotations)
                    found.add(canonical)
            elif nxt not in done:
                visit(nxt)
        visiting.pop(); active.remove(node); done.add(node)

    for node in sorted(graph):
        visit(node)
    return [" -> ".join([*cycle, cycle[0]]) for cycle in sorted(found)]


def _contract_surfaces(root: Path) -> list[str]:
    out: list[str] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts):
        rp = _rel(root, path)
        if CONTRACT_NAMES.search(path.name) or path.suffix.casefold() in {".proto", ".graphql", ".gql"}:
            out.append(rp)
    return out


def analyze_contract_drift(root: Path) -> dict:
    surfaces = _contract_surfaces(root)
    missing_refs: list[str] = []
    parse_unknowns: list[str] = []
    for rp in surfaces:
        path = root / rp
        if path.suffix.casefold() in {".yaml", ".yml"}:
            for ref in YAML_REF.findall(path.read_text(encoding="utf-8", errors="replace")):
                if "://" in ref or ref.startswith("#"):
                    continue
                target = (path.parent / ref).resolve()
                try:
                    target.relative_to(root.resolve())
                except ValueError:
                    missing_refs.append(f"escaping-ref:{rp}->{ref}")
                    continue
                if not target.exists():
                    missing_refs.append(f"missing-ref:{rp}->{ref}")
        elif path.suffix.casefold() == ".json":
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                parse_unknowns.append(f"parse-unavailable:{rp}")
                continue
            stack = [data]
            while stack:
                item = stack.pop()
                if isinstance(item, dict):
                    ref = item.get("$ref")
                    if isinstance(ref, str) and not ref.startswith("#") and "://" not in ref:
                        target = (path.parent / ref).resolve()
                        try:
                            target.relative_to(root.resolve())
                        except ValueError:
                            missing_refs.append(f"escaping-ref:{rp}->{ref}")
                        else:
                            if not target.exists():
                                missing_refs.append(f"missing-ref:{rp}->{ref}")
                    stack.extend(item.values())
                elif isinstance(item, list):
                    stack.extend(item)
    return {
        "surfaces": surfaces,
        "broken_local_refs": sorted(set(missing_refs)),
        "confidence": "PARTIAL" if surfaces else "UNVERIFIED",
        "unknowns": sorted(set(parse_unknowns + [
            "contract-file presence does not prove producer/consumer runtime compatibility",
            "dynamic/generated contracts and external consumers are not inferred from static repository files",
        ])),
    }


def analyze_architecture(root: Path) -> dict:
    files = _source_files(root)
    index = _module_index(root, files)
    edges: set[tuple[str, str]] = set()
    for path in files:
        if path.suffix == ".py":
            edges.update(_python_edges(root, path, index))
        else:
            edges.update(_js_edges(root, path, index))
    edge_list = sorted(edges)
    incoming = Counter(dst for _, dst in edge_list)
    outgoing = Counter(src for src, _ in edge_list)
    nodes = sorted({_rel(root, p) for p in files})
    top = sorted({Path(node).parts[0] for node in nodes if len(Path(node).parts) > 1 and not Path(node).parts[0].startswith(".")})
    coupling = [
        f"{node}:fan-in={incoming[node]},fan-out={outgoing[node]}"
        for node in sorted(set(incoming) | set(outgoing))
        if incoming[node] + outgoing[node] >= 3
    ]
    cycles = _cycles(edge_list)
    contracts = _contract_surfaces(root)
    return {
        "top_level_boundaries": top,
        "api_contract_signals": contracts,
        "dependency_edges": [f"{src} -> {dst}" for src, dst in edge_list],
        "change_impact": "PARTIAL" if edge_list else "UNVERIFIED",
        "cycles": cycles,
        "coupling": coupling,
        "confidence": "PARTIAL" if nodes or contracts else "UNVERIFIED",
        "unknowns": [
            "static import edges do not prove runtime call flow or production blast radius",
            "dynamic imports, reflection, generated code, external services and unsupported languages may add unseen edges",
            "fan-in/fan-out is an observed dependency signal, not a maintainability or quality score",
        ],
    }
