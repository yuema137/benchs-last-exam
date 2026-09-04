# Curation queue

## Candidates requiring a score/protocol pass

- **AgentBench / WebArena / Mind2Web / WebShop / ALFWorld** — important agent benchmarks represented in the SciEval reference, but current BLE exports do not contain a complete source-linked longitudinal series. Add after canonical score tables and model release dates are reconciled.
- **InterCode / AppWorld / AndroidWorld** — useful environment benchmarks, but current evidence is sparse or the canonical task/configuration boundary needs another audit before adding a lifecycle curve. MLE-bench is now in the core using the original AIDE/All any-medal series.
- **BBEH and other newer hard-reasoning variants** — keep separate from BIG-Bench Hard; do not merge versions without a dedicated protocol review.

Sparse T50/T90 data alone is not a reason to defer. The queue is for unresolved identity, version, protocol, or observation provenance.

## Previously identified candidates

- **GeneBench-Pro** — important scientific-agent candidate, but new and currently too sparse for a trustworthy longitudinal series.
- **HumanEval** — added as the original fixed 164-problem Pass@1 measurement; HumanEval+ remains separate.
- **BigCodeBench** — added using the fixed Complete calibrated Pass@1 series; Instruct and Hard remain separate.
- **GAIA** — added to the core with the fixed 2023 release and official leaderboard export.
- **MMMU / MMMU-Pro** — added as separate fixed measurement objects; original validation and MMMU-Pro overall scores are not merged.
- **BFCL V4** — added with three source-linked rows from the fixed evaluator checkpoint; the wider live leaderboard remains outside this snapshot.
- **RULER / LiveBench / LiveCodeBench** — configuration-dependent or rolling measurement objects; they need explicit lifecycle semantics before entering the fixed-target core.
- **TUA-Bench** — official 120-task terminal-use benchmark with promising current rows, but the public release date is only month-level in the available source; do not invent a day for the capability timeline.
- **LAB-Bench** — important biology-research benchmark, but the available official materials do not yet provide a clean, source-linked longitudinal overall-score export for this snapshot.
- **WebArena / τ²-bench** — canonical agent environments, but this pass did not establish a sufficiently clean fixed-version, multi-generation score series with defensible model release dates.
