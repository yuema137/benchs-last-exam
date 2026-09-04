# Benchmark Integration Contract

Adding a benchmark is an end-to-end repository transaction, not a data-file edit.

The canonical active benchmark registry in `scripts/build_snapshot.py` is the source of truth. A complete addition provides:

1. canonical identity, version, release date, Evaluation Type, and Domain;
2. concise English and Chinese summary, task format, scoring explanation, and evaluation target;
3. benchmark resources and source-linked canonical observations;
4. resolvable models, dates, protocols, and capability-frontier lineage;
5. derived lifecycle metrics, coverage, and cost (`Unknown`, `N/A`, or `—` when evidence is insufficient);
6. generated leaderboard/detail data and automatic lifecycle-tab eligibility.

Leaderboard rows and lifecycle cards are generated views. No benchmark may be manually assigned to a story tab, and no chart-only score is allowed. Active benchmark IDs must be represented by generated leaderboard and detail data.

Run the acceptance check after every benchmark addition or observation update:

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_benchmark_integration.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Selection evidence such as citation counts belongs in curation documentation, with its source and check date. It is not a leaderboard metric. Missing longitudinal data is not by itself a reason to defer an important benchmark; unclear identity, version, metric, or incompatible measurement objects are.

