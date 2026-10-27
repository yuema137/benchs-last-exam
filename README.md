# Benchmark Observatory

Benchmark Observatory is a lightweight **Leaderboard of Benchmarks**.

**BLE evaluates benchmarks themselves, not where their results are reported.**
It examines each benchmark along dimensions such as discriminative power,
headroom and saturation speed, coverage and freshness, protocol comparability,
cost and contamination resistance. BLE is deliberately selective: it includes
only classic, widely followed benchmarks and aims to show frontier progress
with relatively little information, not comprehensive coverage. See the
[inclusion criteria](CONTRIBUTING.md#inclusion-criteria-initial-policy).

### Acknowledgement

BLE thanks [benchmark-radar](https://github.com/ktwu01/benchmark-radar) by
Koutian Wu, which tracks where AI benchmark and evaluation results are
reported. We use it only as a reference for discovering sources: every number
in BLE is re-read from the original paper, leaderboard or vendor release and
cited there, and no benchmark-radar content is copied or redistributed.

The two projects answer different questions. benchmark-radar helps you find
benchmarks and the places their results appear, across a very large
collection. BLE is deliberately selective: it follows a small set of classic,
widely followed benchmarks and evaluates the benchmarks themselves, along
dimensions such as discriminative power, headroom and saturation speed,
coverage and freshness, protocol comparability, cost and contamination
resistance, so you can judge what a benchmark still tells you about frontier
models.

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

The runtime loads a small `site/data/index.json` for the leaderboard and story
views. Complete benchmark dossiers are split under
`site/data/benchmarks/<benchmark-id>.json` and fetched only when opened.

Homepage filtering distinguishes one mutually exclusive `domain` from controlled, many-to-many capability `labels`. Label definitions are bilingual and canonical; selecting multiple labels requires all selected capabilities to match.

Each active benchmark/version is maintained independently in
`data/benchmarks/<benchmark-id>.json`; its source observations live in the
referenced `data/raw/*.csv` file. The typed registry loader discovers these
records automatically, and the build derives the leaderboard, detail cards,
frontiers, metrics, and all lifecycle tabs from them.

Run the complete integration gate after changing any benchmark or observation:

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_score_semantics.py
python3 scripts/validate_provenance.py
python3 scripts/validate_benchmark_integration.py
python3 scripts/audit_observation_dates.py
python3 scripts/audit_canonical_identity.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Licensing

- **Code** (site, scripts, pipeline, tests): [MIT](LICENSE).
- **BLE's own data and writing** (the scores, rankings, frontiers, lifecycle
  metrics and classifications BLE computes; benchmark cards; documentation):
  [CC BY-SA 4.0](LICENSE-DATA).
- **Third-party results and materials** (source rows in `data/raw/`, linked
  papers, leaderboards, evaluation logs and vendor releases) stay under their
  original terms. Attribution for Epoch AI data and other bulk sources is in
  [`NOTICE`](NOTICE).

Copyright 2026 Yue Ma. See the
[Data Provenance and Licensing Policy](docs/DATA_PROVENANCE_POLICY.md) for the
third-party terms BLE found and the open licensing items. To cite BLE, use
[`CITATION.cff`](CITATION.cff).

## Documentation

- [Design synthesis](docs/design-synthesis.md)
- [Vertical slice plan](docs/vertical-slice-plan.md)
- [Repository constitution](AGENT.md)
- [Benchmark integration contract](docs/BENCHMARK_INTEGRATION.md)
- [Data provenance and licensing policy](docs/DATA_PROVENANCE_POLICY.md)
- [Contributing and inclusion criteria](CONTRIBUTING.md)
- [Explanation style](EXPLANATION_STYLE.md)
- [Chinese design mirror](zh/docs/design-synthesis.md)
