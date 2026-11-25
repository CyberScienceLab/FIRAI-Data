#!/usr/bin/env python3
"""
Compile firai-data's src/ YAML sources into a single distributable FIRAI.yaml
(and a JSON mirror for site consumption).

Usage:
    python tools/compile.py

Writes:
    dist/FIRAI.yaml
    dist/FIRAI.json
"""
import glob
import json
import os
import sys
from datetime import datetime, timezone

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")


def read_version():
    """The release version, from the single VERSION file at the repo root.

    CITATION.cff, CHANGELOG.md and the website all follow this file; tests
    check that they agree with it.
    """
    with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as f:
        version = f.read().strip()
    parts = version.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        sys.exit(f"VERSION must be MAJOR.MINOR.PATCH, got {version!r}")
    return version


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f) or []


def load_all(pattern):
    items = []
    for path in sorted(glob.glob(os.path.join(SRC, pattern))):
        data = load_yaml(path)
        if isinstance(data, list):
            items.extend(data)
        elif data is not None:
            items.append(data)
    return items


def compute_counts(techniques, evidence_classes, gaps, readiness):
    parents = [t for t in techniques if not t.get("sub_of")]
    subs = [t for t in techniques if t.get("sub_of")]
    return {
        "techniques_total": len(techniques),
        "techniques_parent": len(parents),
        "techniques_sub": len(subs),
        "evidence_classes": len(evidence_classes),
        "gaps": len(gaps),
        "readiness_measures": len(readiness),
    }


def main():
    phases = load_yaml(os.path.join(SRC, "phases.yaml"))
    evidence_classes = load_yaml(os.path.join(SRC, "evidence-classes.yaml"))
    techniques = load_all("techniques/*.yaml")
    readiness = load_all("readiness/*.yaml")
    gaps = load_all("gaps/*.yaml")
    maturity = sorted(load_yaml(os.path.join(SRC, "maturity.yaml")), key=lambda m: m["order"])

    # -- basic referential checks (full validation lives in tests/, this is a
    #    fail-fast sanity gate so a broken compile never reaches dist/) --
    ec_ids = {e["id"] for e in evidence_classes}
    phase_ids = {p["id"] for p in phases}
    technique_ids = {t["id"] for t in techniques}
    readiness_ids = {r["id"] for r in readiness}
    errors = []

    for t in techniques:
        if t["phase"] not in phase_ids:
            errors.append(f"{t['id']}: unknown phase {t['phase']}")
        for ec in t.get("evidence_classes", []):
            if ec not in ec_ids and ec not in phase_ids:
                errors.append(f"{t['id']}: unknown evidence class {ec}")
        if t.get("sub_of") and t["sub_of"] not in technique_ids:
            errors.append(f"{t['id']}: sub_of references unknown technique {t['sub_of']}")
        for rm in t.get("readiness_measures", []):
            if rm["id"] not in readiness_ids:
                errors.append(f"{t['id']}: readiness_measures references unknown {rm['id']}")

    if errors:
        print("COMPILE FAILED - referential integrity errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    version = read_version()
    compiled = {
        "firai_version": version,
        # The schema is versioned with the release (MAJOR.MINOR) until a
        # release changes the schema without changing the data, or vice versa.
        "schema_version": ".".join(version.split(".")[:2]),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": compute_counts(techniques, evidence_classes, gaps, readiness),
        "maturity_scale": maturity,
        "phases": phases,
        "evidence_classes": evidence_classes,
        "techniques": techniques,
        "readiness_measures": readiness,
        "gaps": gaps,
    }

    os.makedirs(DIST, exist_ok=True)
    yaml_path = os.path.join(DIST, "FIRAI.yaml")
    json_path = os.path.join(DIST, "FIRAI.json")

    with open(yaml_path, "w") as f:
        yaml.dump(compiled, f, sort_keys=False, allow_unicode=True, width=100)
    with open(json_path, "w") as f:
        json.dump(compiled, f, indent=2, ensure_ascii=False)

    print(f"wrote {yaml_path}")
    print(f"wrote {json_path}")
    print(f"counts: {compiled['counts']}")


if __name__ == "__main__":
    main()
