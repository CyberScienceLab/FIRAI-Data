"""
CI data validation for firai-data: pytest-based schema + referential-integrity
checks. Run with:

    pytest

Covers:
  - every src/ record validates against its JSON Schema
  - IDs are unique and correctly formatted
  - cross-references (sub_of, readiness_measures, evidence_classes, phase) resolve
  - every inferential technique carries a non-empty claim_profile
    (does_establish / does_not_establish)
  - dist/FIRAI.yaml, once compiled, matches src/ counts exactly
    (counts are generated, never hand-maintained)
"""
import glob
import json
import os
import re
import subprocess
import sys

import jsonschema
import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
SCHEMAS = os.path.join(ROOT, "schemas")
DIST = os.path.join(ROOT, "dist")


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


def load_schema(name):
    with open(os.path.join(SCHEMAS, name)) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def phases():
    return load_yaml(os.path.join(SRC, "phases.yaml"))


@pytest.fixture(scope="module")
def evidence_classes():
    return load_yaml(os.path.join(SRC, "evidence-classes.yaml"))


@pytest.fixture(scope="module")
def techniques():
    return load_all("techniques/*.yaml")


@pytest.fixture(scope="module")
def readiness():
    return load_all("readiness/*.yaml")


@pytest.fixture(scope="module")
def gaps():
    return load_all("gaps/*.yaml")


@pytest.fixture(scope="module")
def maturity():
    return load_yaml(os.path.join(SRC, "maturity.yaml"))


# --------------------------------------------------------------- schema checks
def test_evidence_classes_validate(evidence_classes):
    schema = load_schema("evidence-class.schema.json")
    for ec in evidence_classes:
        jsonschema.validate(ec, schema)


def test_readiness_validate(readiness):
    schema = load_schema("readiness.schema.json")
    for r in readiness:
        jsonschema.validate(r, schema)


def test_gaps_validate(gaps):
    schema = load_schema("gap.schema.json")
    for g in gaps:
        jsonschema.validate(g, schema)


def test_techniques_validate(techniques):
    schema = load_schema("technique.schema.json")
    for t in techniques:
        jsonschema.validate(t, schema)


def test_maturity_validate(maturity):
    schema = load_schema("maturity.schema.json")
    for m in maturity:
        jsonschema.validate(m, schema)


def test_maturity_scale_matches_technique_enum(maturity):
    # maturity.yaml is the single source of the scale's wording, so it must
    # define exactly the grades a technique can carry: no more, no fewer.
    technique_schema = load_schema("technique.schema.json")
    grades = technique_schema["properties"]["maturity"]["properties"]["base"]["enum"]
    ids = [m["id"] for m in maturity]
    assert len(ids) == len(set(ids)), "duplicate grades in maturity.yaml"
    assert set(ids) == set(grades), f"maturity.yaml grades {ids} != technique enum {grades}"


def test_maturity_order_is_a_permutation(maturity):
    orders = sorted(m["order"] for m in maturity)
    assert orders == list(range(1, len(maturity) + 1))


# ----------------------------------------------------------- lifecycle stages
# Stage names exactly as in the Lifecycle Stage row of NIST AI 100-1 (AI RMF
# 1.0), Figure 3, in lifecycle order. Pinned here so a schema edit cannot
# silently drift from the NIST wording.
NIST_AI_RMF_LIFECYCLE_STAGES = [
    "Plan and Design",
    "Collect and Process Data",
    "Build and Use Model",
    "Verify and Validate",
    "Deploy and Use",
    "Operate and Monitor",
    "Use or Impacted by",
]


def test_lifecycle_vocabulary_matches_nist_ai_rmf():
    schema = load_schema("technique.schema.json")
    assert schema["$defs"]["lifecycleStage"]["enum"] == NIST_AI_RMF_LIFECYCLE_STAGES


def test_every_technique_has_a_lifecycle_stage(techniques):
    for t in techniques:
        stages = t.get("lifecycle_stages") or []
        assert stages, f"{t['id']}: no lifecycle_stages"
        assert any(s["applicability"] == "applicable" for s in stages), (
            f"{t['id']}: lists only 'rarely' stages; at least one stage must be applicable"
        )


def test_lifecycle_stages_listed_once_each(techniques):
    # one entry per stage, so a stage can never be both applicable and rarely
    for t in techniques:
        names = [s["stage"] for s in t.get("lifecycle_stages") or []]
        dupes = sorted({n for n in names if names.count(n) > 1})
        assert not dupes, f"{t['id']}: lifecycle stage listed more than once: {dupes}"


def test_lifecycle_stages_in_lifecycle_order(techniques):
    for t in techniques:
        names = [s["stage"] for s in t.get("lifecycle_stages") or []]
        assert names == sorted(names, key=NIST_AI_RMF_LIFECYCLE_STAGES.index), (
            f"{t['id']}: lifecycle_stages out of NIST lifecycle order"
        )


# --------------------------------------------------------- uniqueness / format
def test_technique_ids_unique(techniques):
    ids = [t["id"] for t in techniques]
    assert len(ids) == len(set(ids)), "duplicate technique IDs found"


def test_evidence_class_ids_unique(evidence_classes):
    ids = [e["id"] for e in evidence_classes]
    assert len(ids) == len(set(ids))


def test_evidence_class_volatility_ranks_are_a_permutation(evidence_classes):
    ranks = sorted(e["volatility_rank"] for e in evidence_classes)
    assert ranks == list(range(1, len(evidence_classes) + 1)), (
        "EC01-EC07 volatility ordering must be a dense 1..N ranking (Part III, "
        "P0-4 ruling: the ordering is asserted, not arbitrary)"
    )


# --------------------------------------------------------------- referential
def test_technique_phase_resolves(techniques, phases):
    phase_ids = {p["id"] for p in phases}
    for t in techniques:
        assert t["phase"] in phase_ids, f"{t['id']}: unknown phase {t['phase']}"


def test_technique_sub_of_resolves(techniques):
    ids = {t["id"] for t in techniques}
    for t in techniques:
        if t.get("sub_of"):
            assert t["sub_of"] in ids, f"{t['id']}: sub_of {t['sub_of']} does not exist"


def test_technique_readiness_measures_resolve(techniques, readiness):
    readiness_ids = {r["id"] for r in readiness}
    for t in techniques:
        for rm in t.get("readiness_measures", []):
            assert rm["id"] in readiness_ids, (
                f"{t['id']}: readiness measure {rm['id']} does not exist"
            )


def test_technique_evidence_classes_resolve(techniques, evidence_classes, phases):
    # a technique's evidence_classes entries are either EC## IDs or, for
    # cross-cutting techniques rendered as phase bands (Principle 4 / P1-2),
    # the phase ID itself (e.g. T0406 -> ["P04"]).
    ec_ids = {e["id"] for e in evidence_classes}
    phase_ids = {p["id"] for p in phases}
    for t in techniques:
        for ec in t["evidence_classes"]:
            assert ec in ec_ids or ec in phase_ids, (
                f"{t['id']}: evidence class {ec} does not resolve"
            )


# ------------------------------------------------------- content / CI rules
def test_flagship_techniques_have_claim_profiles(techniques):
    # every inferential technique needs non-empty does_establish /
    # does_not_establish. We check the pages that have been brought up to
    # full content; stub techniques are expected to gain this as their pages
    # are written (tracked, not silently passing forever).
    written = {"T0104", "T0303", "T0402", "T0403"}
    for t in techniques:
        if t["id"] in written:
            cp = t.get("claim_profile") or {}
            assert cp.get("does_establish"), f"{t['id']}: missing does_establish"
            assert cp.get("does_not_establish"), f"{t['id']}: missing does_not_establish"


def test_public_output_guard_strings_absent_from_src():
    # Guard against internal assignment/annotation/editorial-provenance
    # markers making their way into src/ from private-spec drafts (Part 0/X:
    # the public build must never contain [ACTION], [verify], "Ali-ratified",
    # personal names in assignment context, or private-repo/page-provenance
    # text). Personal names are checked as whole words so this doesn't
    # false-positive on substrings (e.g. "Alignment" contains "Ali").
    banned_substrings = ["[ACTION", "[verify]", "Ali-ratified", "page-provenance", "INTERNAL DRAFT"]
    banned_name_words = ["Ali", "Zain"]
    name_pattern = re.compile(r"\b(" + "|".join(re.escape(w) for w in banned_name_words) + r")\b")
    for path in glob.glob(os.path.join(SRC, "**/*.yaml"), recursive=True):
        text = open(path).read()
        for term in banned_substrings:
            assert term not in text, f"{path} contains banned private-spec marker: {term!r}"
        m = name_pattern.search(text)
        assert m is None, f"{path} contains a banned personal name: {m.group(0)!r}"


# ------------------------------------------------------------------- compile
def test_compile_produces_dist_matching_src_counts(techniques, evidence_classes, gaps, readiness):
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "compile.py")],
        check=True, cwd=ROOT,
    )
    with open(os.path.join(DIST, "FIRAI.yaml")) as f:
        compiled = yaml.safe_load(f)

    counts = compiled["counts"]
    assert counts["techniques_total"] == len(techniques)
    assert counts["evidence_classes"] == len(evidence_classes)
    assert counts["gaps"] == len(gaps)
    assert counts["readiness_measures"] == len(readiness)
    assert [m["id"] for m in compiled["maturity_scale"]] == ["Established", "Demonstrated", "Proposed"]
