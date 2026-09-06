# Provenance and Resource Model

The static snapshot has one canonical `Resource` registry. A resource is a
reusable URL-backed evidence record for a benchmark, model, or shared
evaluation source. Observations store `source_ids`; they do not duplicate
resource titles or URLs.

## Canonical artifacts

- `data/resources.json` is the generated resource registry.
- `data/models.json` is the generated reference-model evidence registry.
- `data/observations.jsonl` contains one canonical score observation per line.
- `data/evidence.jsonl` contains every accepted source row before exact-measurement merging.
- `site/data/benchmarks.json` is the canonical full-build validation snapshot.
- `site/data/index.json` is the lightweight initial frontend index.
- `site/data/benchmarks/<id>.json` is the complete lazy-loaded benchmark dossier,
  including derived frontier points that retain `observation_id` and `source_ids`.
- `site/data/resources.json` is the lazy-loaded public resource registry used by
  detail-page provenance links.

Snapshot schema version 2 separates immutable source evidence records from
deduplicated canonical measurements and uses semantic IDs for resources,
models, and observations.

Run:

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_provenance.py
```

## Date semantics

Observations preserve benchmark release date, model release date, evaluation
date, result-public date, source-publication date, and ingestion date as
separate fields. For one canonical measurement, `observation_date` is the
earliest available evaluation/run date, model release date, or score-publication
date. A publication date is eligible only when that source version actually
contains the score. Multiple sources remain attached to the observation even
when only the earliest date drives the timeline.

The lifecycle plot uses `max(benchmark_release_date, observation_date)`. A
pre-release observation therefore appears as `At release` with zero elapsed
time; its original date remains unchanged in provenance. Negative T50/T80/T90
durations are forbidden.

Raw source rows remain in `data/evidence.jsonl`. Canonical observations merge
only exact measurement identities and retain `evidence_ids`, `evidence_count`,
and every score source. Observation, model, and resource IDs are generated from
semantic identity rather than row position. This makes source reordering safe
while keeping all original evidence auditable.

## Update channels prepared by the model

In a future manual refresh, benchmark-scoped resources can be checked for new
model results, while resources attached to reference models can be checked for
new benchmark results. `watch` and `last_checked_at` are present for that
purpose. The required inventory and reconciliation procedure is documented in
[`MODEL_RELEASE_UPDATE_PROTOCOL.md`](MODEL_RELEASE_UPDATE_PROTOCOL.md). No
scheduler, crawler, or automatic update job is part of this layer.

## Known gaps

The current exports provide evaluation logs or aggregator links for many
observations, but not a model-specific official release resource or a
first-public result date for every score. These gaps are documented by
`scripts/validate_provenance.py` rather than filled with guessed metadata.
