# Changelog

All notable changes to FIRAI are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/). The current version is in the
`VERSION` file.

## [0.1.0] - Unreleased

The first public release, published as a request for community comment.

### Added

- The FIRAI taxonomy: five forensic phases, seven AI evidence classes ordered
  by volatility, techniques and sub-techniques, forensic readiness measures and
  open gaps, each with a stable ID.
- A maturity scale (Established, Demonstrated, Proposed) in
  `src/maturity.yaml`, with each grade aligned to the reliability factors
  courts apply to expert evidence: *Daubert* in the United States, and
  *Mohan*, *J.-L.J.* and *White Burgess* in Canada.
- References for every technique graded above Proposed, each checked against
  the source.
- `lifecycle_stages` on every technique, using the AI lifecycle stages of
  NIST AI 100-1 (AI RMF 1.0). See `lifecycle-mapping.md`.
- Types, descriptions and technique links for all readiness measures.
- Links from technique notes to every open gap.
- `novelty-and-gap-method.md`, the search record behind absence claims.
- An optional `originality_rationale` field for Proposed techniques without
  references.
- `CITATION.cff`, this changelog and a single `VERSION` file.

### Changed

- Principle 7 now says that every technique *will* state what it does and does
  not establish. Claim profiles are being written during the comment period.

### Removed

- The unused `evidence_role` field from the technique schema.

### Validation

- CI fails when a technique graded above Proposed has no references, and warns
  when a Proposed technique has neither references nor an
  `originality_rationale`.
- CI checks the lifecycle vocabulary against NIST AI 100-1, readiness types and
  links, gap links, and that `CITATION.cff` and this changelog match `VERSION`.

[0.1.0]: https://github.com/CyberScienceLab/FIRAI-Data/releases/tag/v0.1.0
