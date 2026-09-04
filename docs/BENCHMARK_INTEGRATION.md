# Benchmark Integration Contract

Adding a benchmark is an end-to-end repository transaction, not a data-file edit.

The canonical active benchmark registry in `scripts/build_snapshot.py` is the source of truth. A complete addition provides:

1. canonical identity, version, release date, Evaluation Type, and Domain;
2. concise English and Chinese summary, task format, scoring explanation, and evaluation target;
3. benchmark resources and source-linked canonical observations;
4. resolvable models, dates, protocols, and capability-frontier lineage;
5. derived lifecycle metrics, coverage, and cost (`Unknown`, `N/A`, or `—` when evidence is insufficient);
6. generated leaderboard/detail data and automatic lifecycle-tab eligibility.

Lifecycle synchronization is a build invariant. Every build regenerates the membership IDs for all four story views (`test-of-time`, `still-frontier`, `fastest-solved`, and `recently-saturated`) from the same canonical benchmark metrics. The frontend consumes those generated IDs; it must not keep a separate manual list or selector that can become stale. Adding or updating a benchmark is incomplete until all four generated views and their empty/non-empty states validate together.

Leaderboard rows and lifecycle cards are generated views. No benchmark may be manually assigned to a story tab, and no chart-only score is allowed. Active benchmark IDs must be represented by generated leaderboard and detail data.

Run the acceptance check after every benchmark addition or observation update:

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_benchmark_integration.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The integration validator checks that every generated story-view list exists, contains unique IDs, and resolves to active benchmarks. A benchmark may legitimately be absent from a view; it may not be unresolved or omitted because only another tab was refreshed.

Selection evidence such as citation counts belongs in curation documentation, with its source and check date. It is not a leaderboard metric. Missing longitudinal data is not by itself a reason to defer an important benchmark; unclear identity, version, metric, or incompatible measurement objects are.
