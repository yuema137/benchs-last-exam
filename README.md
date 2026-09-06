# Benchmark Observatory

Benchmark Observatory is a lightweight **Leaderboard of Benchmarks**.

## View the website

**[Open the live Benchmark Observatory →](https://yuema137.github.io/ble/)**

The website is the public-facing frontend. This repository contains its curated benchmark data, provenance, metric logic, and static-site source.

Traditional benchmark leaderboards use benchmarks to rank models. This project reverses the viewpoint: a small, representative reference model panel provides historical observations that describe and compare the benchmarks themselves.

The current scope is deliberately small:

```text
curated source data → Python metric scripts → generated JSON → static frontend
```

The same static output is published to GitHub Pages at [yuema137.github.io/ble](https://yuema137.github.io/ble/).

The project does not currently aim to provide a backend, database, public API, accounts, cloud ingestion, or exhaustive model coverage.

## Local development

The local frontend lives under `site/` and is driven by generated JSON. Metric logic belongs in Python scripts, not in frontend components.

Each active benchmark/version is maintained independently in
`data/benchmarks/<benchmark-id>.json`; its source observations live in the
referenced `data/raw/*.csv` file. The typed registry loader discovers these
records automatically, and the build derives the leaderboard, detail cards,
frontiers, metrics, and all lifecycle tabs from them.

Run the complete integration gate after changing any benchmark or observation:

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_score_semantics.py
python3 scripts/validate_benchmark_integration.py
python3 scripts/audit_observation_dates.py
python3 scripts/audit_canonical_identity.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Documentation

- [Design synthesis](docs/design-synthesis.md)
- [Vertical slice plan](docs/vertical-slice-plan.md)
- [Repository constitution](AGENT.md)
- [Benchmark integration contract](docs/BENCHMARK_INTEGRATION.md)
- [Explanation style](EXPLANATION_STYLE.md)
- [Chinese design mirror](zh/docs/design-synthesis.md)
