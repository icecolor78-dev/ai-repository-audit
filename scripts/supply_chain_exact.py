from __future__ import annotations

import json
import re
from pathlib import Path

LICENSE_NAMES = {"license", "license.md", "license.txt", "copying", "copying.md", "notice", "notice.md"}
UPDATE_NAMES = {"dependabot.yml", "dependabot.yaml", "renovate.json", "renovate.json5", "renovate-config.js"}
SBOM_HINT = re.compile(r"(?:^|/)(?:sbom|bom)(?:[._-]|$)|cyclonedx|spdx", re.I)
VENDOR_HINT = re.compile(r"(^|/)(?:vendor|vendored|generated|third_party|third-party)(/|$)", re.I)
REQ_PIN = re.compile(r"^([A-Za-z0-9_.-]+)==([^\s;]+)")
REQ_HASH = re.compile(r"--hash=([A-Za-z0-9_-]+:[A-Fa-f0-9]+)")
GO_SUM = re.compile(r"^(\S+)\s+(v\S+?)(?:/go\.mod)?\s+(h1:\S+)$")


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _all_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts)


def _requirements(path: Path, rel: str) -> tuple[list[str], list[str]]:
    resolved: list[str] = []
    provenance: list[str] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(("-r", "--requirement", "-c", "--constraint")):
            continue
        match = REQ_PIN.match(line)
        if match:
            resolved.append(f"python:{match.group(1)}=={match.group(2)} [{rel}:{line_number}]")
            hashes = REQ_HASH.findall(line)
            for item in hashes:
                provenance.append(f"python-integrity:{match.group(1)} {item} [{rel}:{line_number}]")
    return resolved, provenance


def _package_lock(path: Path, rel: str) -> tuple[list[str], list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return [], [f"parse-unavailable:{rel}"]
    resolved: list[str] = []
    provenance: list[str] = []
    packages = data.get("packages")
    if isinstance(packages, dict):
        for location, meta in sorted(packages.items()):
            if not location or not isinstance(meta, dict):
                continue
            name = meta.get("name") or Path(location).name
            version = meta.get("version")
            if isinstance(name, str) and isinstance(version, str):
                resolved.append(f"npm:{name}@{version} [{rel}]")
            integrity = meta.get("integrity")
            if isinstance(integrity, str) and integrity:
                provenance.append(f"npm-integrity:{name} {integrity} [{rel}]")
    return resolved, provenance


def _cargo_lock(path: Path, rel: str) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    resolved: list[str] = []
    provenance: list[str] = []
    for block in text.split("[[package]]")[1:]:
        name = re.search(r'(?m)^name\s*=\s*"([^"]+)"', block)
        version = re.search(r'(?m)^version\s*=\s*"([^"]+)"', block)
        checksum = re.search(r'(?m)^checksum\s*=\s*"([^"]+)"', block)
        if name and version:
            resolved.append(f"cargo:{name.group(1)}@{version.group(1)} [{rel}]")
            if checksum:
                provenance.append(f"cargo-checksum:{name.group(1)} {checksum.group(1)} [{rel}]")
    return resolved, provenance


def _go_sum(path: Path, rel: str) -> tuple[list[str], list[str]]:
    resolved: list[str] = []
    provenance: list[str] = []
    seen: set[tuple[str, str]] = set()
    for line_number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        match = GO_SUM.match(raw.strip())
        if not match:
            continue
        module, version, digest = match.groups()
        key = (module, version)
        if key not in seen:
            resolved.append(f"go:{module}@{version} [{rel}:{line_number}]")
            seen.add(key)
        provenance.append(f"go-integrity:{module}@{version} {digest} [{rel}:{line_number}]")
    return resolved, provenance


def analyze_supply_chain(root: Path) -> dict:
    files = _all_files(root)
    paths = [_rel(root, p) for p in files]
    manifests = [p for p in files if p.name in {"requirements.txt", "requirements-dev.txt", "package.json", "pyproject.toml", "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "build.gradle.kts", "Gemfile", "composer.json"}]
    lockfiles = [p for p in files if p.name in {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "Cargo.lock", "go.sum", "Gemfile.lock", "composer.lock", "poetry.lock", "uv.lock", "pdm.lock"}]

    dependencies = [f"manifest:{_rel(root, p)}" for p in manifests] + [f"lockfile:{_rel(root, p)}" for p in lockfiles]
    provenance: list[str] = []
    for path in files:
        rel = _rel(root, path)
        if path.name in {"requirements.txt", "requirements-dev.txt"}:
            resolved, integrity = _requirements(path, rel)
        elif path.name == "package-lock.json":
            resolved, integrity = _package_lock(path, rel)
        elif path.name == "Cargo.lock":
            resolved, integrity = _cargo_lock(path, rel)
        elif path.name == "go.sum":
            resolved, integrity = _go_sum(path, rel)
        else:
            continue
        dependencies.extend(resolved)
        provenance.extend(integrity)

    updates = [rel for rel in paths if Path(rel).name.casefold() in UPDATE_NAMES or rel.casefold().endswith(("/.github/dependabot.yml", "/.github/dependabot.yaml")) or rel.casefold() in {".github/dependabot.yml", ".github/dependabot.yaml"}]
    sbom = [rel for rel in paths if SBOM_HINT.search(rel)]
    licenses = [rel for rel in paths if Path(rel).name.casefold() in LICENSE_NAMES]
    vendor = [rel for rel in paths if VENDOR_HINT.search(rel)]

    unknowns = [
        "repository-visible dependency metadata does not establish current vulnerability absence",
        "resolved-version evidence is limited to supported deterministic lock/manifest parsers",
        "license-file presence does not establish dependency-license compatibility or legal clearance",
        "integrity/checksum presence does not by itself establish trusted provenance or artifact authenticity",
        "dependency freshness and abandonment require current external evidence",
    ]
    confidence = "PARTIAL" if dependencies or updates or sbom or licenses or vendor else "UNVERIFIED"
    return {
        "dependencies": sorted(set(dependencies)),
        "update_automation": sorted(set(updates)),
        "sbom": sorted(set(sbom)),
        "license_evidence": sorted(set(licenses)),
        "provenance": sorted(set(provenance + [f"generated-or-vendor-boundary:{x}" for x in vendor])),
        "confidence": confidence,
        "unknowns": unknowns,
    }
