# Curation queue

## Candidates requiring a score/protocol pass

- **AgentBench / WebArena / Mind2Web / WebShop / ALFWorld** — important agent benchmarks represented in the SciEval reference, but current BLE exports do not contain a complete source-linked longitudinal series. Add after canonical score tables and model release dates are reconciled.
- **MLE-bench / InterCode / AppWorld / AndroidWorld** — useful environment benchmarks, but current evidence is sparse or the canonical task/configuration boundary needs another audit before adding a lifecycle curve.
- **BBEH and other newer hard-reasoning variants** — keep separate from BIG-Bench Hard; do not merge versions without a dedicated protocol review.

Sparse T50/T90 data alone is not a reason to defer. The queue is for unresolved identity, version, protocol, or observation provenance.

## Previously identified candidates

- **GeneBench-Pro** — important scientific-agent candidate, but new and currently too sparse for a trustworthy longitudinal series.
- **HumanEval** — canonical historical coding anchor; add when a clean source-linked model-generation export is curated.
- **BigCodeBench** — valuable realistic code generation benchmark; keep separate from HumanEval and verify its configuration before adding.
- **GAIA** — important general assistant benchmark; freeze the version/scaffold and source-linked observations first.
- **MMMU / MMMU-Pro** — important multimodal objects; keep variants and splits separate and add only with a stable score series.
- **RULER / LiveBench / LiveCodeBench** — configuration-dependent or rolling measurement objects; they need explicit lifecycle semantics before entering the fixed-target core.
