# Provenance and Resource Model

The static snapshot has one canonical `Resource` registry. A resource is a
reusable URL-backed evidence record for a benchmark, model, or shared
evaluation source. Observations store `source_ids`; they do not duplicate
resource titles or URLs.

## Canonical artifacts

- `data/resources.json` is the generated resource registry.
- `data/models.json` is the generated reference-model evidence registry.
- `data/observations.jsonl` contains one canonical score observation per line.
- `site/data/benchmarks.json` is the frontend snapshot, including derived
  frontier points that retain `observation_id` and `source_ids`.

Run:

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_provenance.py
```

## Date semantics

Observations preserve benchmark release date, model release date, evaluation
date, result-public date, source-publication date, and ingestion date as
separate fields. The current pilot export does not provide result-public dates.
Its displayed curve is explicitly labelled as an operational evaluation
timeline and must not be interpreted as a historical public-result frontier.

## Update channels prepared by the model

In a future manual refresh, benchmark-scoped resources can be checked for new
model results, while resources attached to reference models can be checked for
new benchmark results. `watch` and `last_checked_at` are present for that
purpose. No scheduler, crawler, or automatic update job is part of this layer.

## Known gaps

The current exports provide evaluation logs or aggregator links for many
observations, but not a model-specific official release resource or a
first-public result date for every score. These gaps are documented by
`scripts/validate_provenance.py` rather than filled with guessed metadata.
