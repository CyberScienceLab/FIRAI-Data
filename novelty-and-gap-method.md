# Novelty and gap method

This file is the search record that [Principle 11](CONTRIBUTING.md) requires:

> No categorical absence claim ships without a dated search behind it.

A FIRAI record makes an absence claim when it says, directly or by its grade, that no adequate published method exists. This covers:

- every **Proposed** technique, since Proposed means no validated method was found;
- every **gap** (`G####`);
- any notes or profile text along the lines of "first", "only" or "no method exists".

Each claim needs an entry here. A claim is only as strong as the search behind it, so each entry records the search honestly, including what was *not* recorded.

## What an entry records

| Field | What to write |
|---|---|
| **Claim** | The absence or novelty claim, in one sentence, and the record it supports. |
| **Date** | When the search was run. Use a month if the exact day is unknown, and mark it as approximate. |
| **Sources searched** | Databases, sites and indexes, e.g. Google Scholar, IEEE Xplore, ACM DL, arXiv, DFRWS / FSI: Digital Investigation, NIST CSRC, IETF. |
| **Search terms** | The exact strings used. |
| **Other routes** | Citation chasing (backward or forward), expert suggestions, known-item lookups. |
| **Inclusion criteria** | What counted as a match: venue type, date range, language, scope. |
| **Result** | What was found, what was rejected and why, and the resulting claim. |
| **Limitations** | Anything that weakens the search. Unrecorded fields are written as **not recorded**, never reconstructed. |

When the record is published, its claim is scoped to the search: "as of `<date>`, within the search documented in `novelty-and-gap-method.md`", not as an unqualified absolute.

---

## Entries

### 1. T0104.001 AI Artifact Volatility Ordering (Proposed)

- **Claim:** apart from the FIRAI process-model paper (Dehghantanha & Homayoun), no published source orders AI-specific evidence by volatility. Classical guidance orders conventional system state only.
- **Date:** approximately August 2026. The exact date was not recorded.
- **Sources searched:** general web search (Google). Specific databases were not recorded.
- **Search terms:** not recorded.
- **Other routes:**
  - Candidate sources were partly suggested by the project lead.
  - Each was located and checked by web search.
  - The status of RFC 3227 was confirmed on the IETF Datatracker: Best Current Practice (BCP 55), February 2002, with no "Obsoleted by" or "Updated by" notice.
- **Inclusion criteria:** not recorded.
- **Result:**
  - Classical ancestry: RFC 3227 §2.1 (order of volatility), NIST SP 800-86 and ISO/IEC 27037. All three cover conventional system state, not AI artifacts.
  - AI-specific: the only source found was Dehghantanha & Homayoun, *AI Forensics Across White-, Grey-, and Black-Box Access: A Process Model and Research Agenda for Post-Incident Investigation of AI Systems*.
- **Limitations:**
  - An informal search with no recorded terms, databases or criteria, so it cannot be reproduced.
  - The only AI-specific source found is by the framework's own authors.
  - The absence claim should be treated as **provisional** until the search is re-run under this protocol.

### 2. T0403 Training Data Membership & Provenance Testing (review behind the grade split)

- **Claim:** this is not an absence claim. It is the reliability review that set the grades:
  - instance-level membership inference on LLMs (T0403.001) is **Proposed**, downgraded from Demonstrated;
  - dataset-level inference (T0403.002) is **Demonstrated only under stated control conditions**.
- **Date:** approximately August 2026. The exact date was not recorded.
- **Sources searched:** general web search (Google). Specific databases were not recorded.
- **Search terms:** not recorded.
- **Other routes:** candidate papers were partly suggested by the project lead. Each was located and read.
- **Inclusion criteria:** not recorded. In practice the review covered recent (2024–2025) evaluations of membership inference on LLMs.
- **Result:** papers reviewed, all cited on T0403:
  - Duan et al. (2024), *Do Membership Inference Attacks Work on Large Language Models?* MIA performs near random in most domains.
  - Das, Zhang, Tramèr (2024), *Blind Baselines Beat Membership Inference Attacks for Foundation Models.* Benchmarks are confounded by member/non-member distribution shift.
  - Zhang, Das, Kamath, Tramèr (2024), *Position: Membership Inference Attacks Cannot Prove that a Model Was Trained On Your Data.*
  - Maini et al. (2024), *LLM Dataset Inference: Did you train on my dataset?* Dataset-level inference works under IID validation-set conditions.
  - Puerto et al. (2025), *Scaling Up Membership Inference: When and How Attacks Succeed on Large Language Models.*
  - Hayes et al. (2025), *Exploring the limits of strong membership inference attacks on large language models.*
- **Limitations:**
  - No recorded search protocol.
  - The review relied on expert-suggested papers rather than a systematic search, so relevant contrary work may have been missed.

---

## Not yet documented

The records below make an absence claim through their grade or definition. They have no search entry yet. Until they do, their claims should be read as unverified.

**Proposed techniques:**

| Record | Name | Entry |
|---|---|---|
| T0102 | Access Level Determination | not yet documented |
| T0103 | System Composition Mapping | not yet documented |
| T0104 | Evidence Source Inventory | not yet documented |
| T0105 | Reproducibility Pre-Assessment | not yet documented |
| T0204 | Retrieval Corpus & Index Snapshot | not yet documented |
| T0206 | Black-Box Interaction Capture | not yet documented |
| T0208.001 | Custody of Behavioral/Dynamic Evidence | not yet documented |
| T0302.001 | Multi-Agent Trace Correlation & Actor Resolution | not yet documented |
| T0403.001 | Instance-Level Membership Inference | covered by entry 2 |
| T0404 | Behavioral Deviation Analysis | not yet documented |
| T0405 | Internal Mechanism Attribution | not yet documented |
| T0406 | Contributing-Factor Assessment | not yet documented |
| T0501 | Structured Claim Formulation | not yet documented |

**Gaps:**

| Record | Name | Entry |
|---|---|---|
| G0001 | Performance, Error & Uncertainty Characterization | not yet documented |
| G0002 | Black-Box Attribution Methodology | not yet documented |
| G0003 | Post-Incident Index Drift | not yet documented |
| G0004 | AI Artifact Examination Tooling | not yet documented |
| G0005 | Provider-Controlled Evidence Availability | not yet documented |
| G0006 | Evidence/Tool Poisoning & Safe AI-Artifact Examination | not yet documented |
