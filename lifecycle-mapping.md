# Lifecycle mapping

Every technique carries `lifecycle_stages`. This field records the stages of the AI lifecycle in which the technique applies.

## Vocabulary

The stage names come exactly from the "Lifecycle Stage" row of NIST AI 100-1, *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, Figure 3 (p. 11). They are listed here in lifecycle order:

1. Plan and Design
2. Collect and Process Data
3. Build and Use Model
4. Verify and Validate
5. Deploy and Use
6. Operate and Monitor
7. Use or Impacted by

The schema enforces this list (`$defs.lifecycleStage`), and `test_lifecycle_vocabulary_matches_nist_ai_rmf` pins it to the NIST wording.

NIST provides the vocabulary. **The assignment of techniques to stages is FIRAI's own interpretation.** NIST does not prescribe it.

## What a stage entry means

A stage is listed when the technique's **evidence prerequisites can exist and the technique can meaningfully operate** while the AI system is in that stage. This is structural applicability: it says whether the technique can apply in that stage. It does not estimate how likely the evidence is to be available in any particular investigation.

| Applicability | Meaning |
|---|---|
| `applicable` | The required evidence can ordinarily be generated, retained or accessed in this stage, under a plausible implementation. |
| `rarely` | The evidence may be available, but only under atypical retention, access or architectural conditions. |
| *(not listed)* | The technique's evidence prerequisites are generally not met in this stage. |

Each stage appears at most once per technique, so a stage cannot be both `applicable` and `rarely`. Every technique must list at least one `applicable` stage.

The mapping is about where the evidence prerequisites *can exist*, not where the evidence was *generated*. Training data generated during Collect and Process Data can still be acquired later, and logs can be analysed after a system is decommissioned. The mapping asks a narrower question: in which stages does the material the technique needs ordinarily exist in a usable form?

## Scope: Plan and Design and Use or Impacted by

No technique is currently mapped to **Plan and Design** or **Use or Impacted by**. Both stay in the vocabulary.

- **Plan and Design.** FIRAI's evidence classes (EC01 to EC07) describe evidence from an instantiated AI system. Before implementation there is no such system to examine. An incident involving manipulated requirements or design documents is a valid investigation, but its evidence is not yet modelled as an evidence class.
- **Use or Impacted by.** This NIST stage describes affected people and communities: complaints, downstream decisions and impact records. FIRAI v0.1 is scoped to technical evidence from the AI system itself, so socio-technical impact investigation is out of scope for now.

Extending FIRAI to either kind of investigation would mean defining the evidence first, then mapping techniques such as T0101, T0104, T0208, T0406, T0407 and T0501 to T0503 onto these stages.

## Patterns used

| Pattern | Stages | Used for |
|---|---|---|
| Any investigation | Collect and Process Data → Operate and Monitor | Identification techniques (T0101 to T0104.001), custody (T0208), and the analysis and reporting techniques that apply to any incident (T0406, T0407, T0501 to T0503) |
| Model onward | Build and Use Model → Operate and Monitor | Techniques that need a trained model or a running process. This includes model files, live memory, inference configuration, fingerprinting and membership testing. |
| Runtime, with Build as `rarely` | Verify and Validate → Operate and Monitor; Build and Use Model as `rarely` | Techniques that need recorded interactions, retrieval stores or behavioural baselines. These ordinarily exist from validation onward, and during model building only where test runs are recorded. |
| Training data | Collect and Process Data, Build and Use Model, Verify and Validate; Deploy and Use and Operate and Monitor as `rarely` | T0207 |

## Borderline decisions

| Technique | Decision | Rationale |
|---|---|---|
| T0105 Reproducibility Pre-Assessment | Model onward | Reproducibility can be assessed as soon as a model can be run with recorded configuration. That includes during building and validation. |
| T0202 Live Process/Accelerator Memory Acquisition | Model onward | Model processes run during training, evaluation and validation as well as in production. Their memory can be captured in any of these stages. |
| T0301 In-Memory AI Artifact Extraction & Reconstruction | Model onward | Works on the memory images that T0202 acquires, so it follows T0202. |
| T0203 Interaction Log Acquisition | Runtime; Build `rarely` | Test and validation runs produce inference logs. During model building, logs exist only where test interactions are recorded. |
| T0204 Retrieval Corpus & Index Snapshot | Runtime; Build `rarely` | Retrieval stores are populated for validation and production. They are integrated during model building only in some architectures. |
| T0205 Inference Configuration Capture | Model onward | Any time a model is run, including in development and test environments, it runs under a configuration that can be captured. |
| T0206 Black-Box Interaction Capture | Runtime; Build `rarely` | Needs a callable interface. This is ordinary from validation onward, and during building only where a model endpoint is exposed. |
| T0207 Training Data Acquisition | CD, BM, VV; DU and OM `rarely` | Training data is held during preparation, training and fine-tuning. It is also needed in validation for lineage, contamination and membership claims. After deployment it is usually reachable only with provider cooperation or legal process (see T0207's notes and reference). |
| T0208.001 Custody of Behavioral/Dynamic Evidence | Model onward | Dynamic evidence such as behavioural snapshots and replayed sessions can be generated whenever the model is exercised. |
| T0302 / T0302.001 Trace Reconstruction | Runtime; Build `rarely` | Execution traces ordinarily exist from validation onward. During model building they exist only where agent runs are recorded. |
| T0401 / .001 / .002 Replay | Runtime; Build `rarely` | Replay needs the incident's runtime prerequisites: configuration, retrieval snapshot and orchestration. These are ordinarily fixed from validation onward. |
| T0402.004 Behavioral Fingerprinting | Model onward | Elicitation needs only a callable model, and a callable model exists from building onward. |
| T0403 / .001 / .002 Membership Testing | Model onward | Works on training data, but needs a trained model to test against. It therefore starts at Build and Use Model, not at Collect and Process Data. |
| T0404 Behavioral Deviation Analysis | Runtime; Build `rarely` | Needs a behavioural baseline. A baseline is ordinarily established during validation, and exists during building only in some cases. |

Model files can be imported or selected rather than trained locally, and a checkpoint need not exist at every point in training. "Model onward" therefore means that model artifacts *can* exist from Build and Use Model onward. It does not mean they always do.
