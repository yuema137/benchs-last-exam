# Benchmark Observatory

Benchmark Observatory is a lightweight **Leaderboard of Benchmarks**.

Traditional benchmark leaderboards use benchmarks to rank models. This project reverses the viewpoint: a small, representative reference model panel provides historical observations that describe and compare the benchmarks themselves.

The current scope is deliberately small:

```text
curated source data → Python metric scripts → generated JSON → static frontend
```

The first goal is a local, readable benchmark knowledge base. After the data and presentation stabilize, the same static output can be deployed to GitHub Pages.

The project does not currently aim to provide a backend, database, public API, accounts, cloud ingestion, or exhaustive model coverage.

## Local development

The local demo will be added under `site/` and will be driven by generated JSON. Metric logic belongs in Python scripts, not in frontend components.

## Documentation

- [Design synthesis](docs/design-synthesis.md)
- [Vertical slice plan](docs/vertical-slice-plan.md)
- [Repository constitution](AGENT.md)
- [Explanation style](EXPLANATION_STYLE.md)
- [Chinese design mirror](zh/docs/design-synthesis.md)
