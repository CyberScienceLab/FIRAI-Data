# firai-data

The YAML knowledge base behind **FIRAI** (Forensic Investigation Reference
for AI): phases, evidence classes, techniques, forensic-readiness measures,
and GAP records, plus the schemas and scripts that validate and compile them.

## Layout

```
src/
  phases.yaml              # P01-P05
  maturity.yaml            # the maturity scale and its Daubert / Canadian alignment
  evidence-classes.yaml    # EC01-EC07, with the asserted volatility ordering
  techniques/
    P01.yaml ... P05.yaml  # one file per phase; parents + sub-techniques
  readiness/
    readiness.yaml         # R0001-R0011
  gaps/
    gaps.yaml               # G0001-G0006
schemas/                   # JSON Schema for every record type
tools/
  compile.py                # src/ -> dist/FIRAI.yaml + dist/FIRAI.json
tests/
  test_validate.py          # pytest: schema + referential-integrity + CI rules
dist/                       # generated, gitignored — never commit this
lifecycle-mapping.md        # how techniques map onto the NIST AI RMF lifecycle stages
```

## Working with the data

```bash
pip install -r requirements.txt

# validate everything (schema conformance, cross-references, claim-profile
# completeness on written pages, guard-string checks, count parity)
pytest

# compile src/ into a single distributable file
python tools/compile.py
# -> dist/FIRAI.yaml, dist/FIRAI.json
```

CI (`.github/workflows/ci.yml`) runs both on every push/PR. A broken
cross-reference or a schema violation fails the build.

## Adding or editing a technique

1. Edit the relevant `src/techniques/P0X.yaml` file (or add a new record).
2. Fill in `claim_profile` (does_establish / does_not_establish /
   alternative_propositions / corroboration_requirements /
   quality_controls / stop_conditions) for anything but the thinnest stub —
   `tests/test_validate.py` enforces this on flagship pages and will grow to
   cover more IDs as pages are written.
3. Set `lifecycle_stages` (required): each NIST AI RMF lifecycle stage in
   which the technique applies, marked `applicable` or `rarely`. See
   `lifecycle-mapping.md` for the definitions and the patterns in use.
4. `pytest` locally before opening a PR.
5. Bump `maturity.base` only via the safer-grade rule (take the lower grade
   when ambiguous; the community disputes upward).

## Maturity scale

Every technique carries a `maturity.base` grade: `Established`,
`Demonstrated` or `Proposed`. A grade is a research-and-validation summary —
never a legal conclusion, and never described as one. The ladder is, however,
deliberately aligned with the reliability factors courts apply to expert
evidence — the *Daubert* factors in the United States, and the reliability
inquiry under *R v Mohan*, *R v J.-L.J.* and *White Burgess* in Canada — so
that findings built on FIRAI are legible to courts. `src/maturity.yaml`
records what each grade means and how it aligns with those factors; the
website renders the scale from that file.

## ID scheme

`P##` phases · `EC##` evidence classes · `T####` techniques (first two
digits name the home phase) · `T####.###` sub-techniques · `G####` GAPs ·
`R####` forensic readiness measures. IDs are never reused; retirement uses
`status: {draft|active|deprecated|superseded|withdrawn}` plus `aliases`,
`supersedes`, `replaced_by`.

## License

Content: CC BY 4.0. Tooling (`tools/`, `tests/`, `schemas/`): MIT. See
`LICENSE-CONTENT.md`.
