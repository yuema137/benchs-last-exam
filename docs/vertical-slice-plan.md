# Vertical Slice Plan

Status: in progress, 2026-09-03

## Baseline

Git baseline: `00bc31e Establish methodology and typed schema baseline`.

## Pilot selection

The first slice uses four benchmark records from the Epoch AI public data export:

| Benchmark | Role in slice | Metadata | Raw observations | Initial metrics |
|---|---|---|---:|---|
| MMLU | old, broad benchmark | fixed accuracy scale; random-choice floor | 249 | frontier, progress, headroom, thresholds, velocity, coverage |
| GSM8K | math trajectory | exact-match accuracy; fixed bounds | 235 | frontier, progress, headroom, thresholds, velocity, coverage |
| GPQA Diamond | difficult science reasoning | accuracy; four-choice floor | 311 | frontier, progress, headroom, thresholds, velocity, coverage |
| SWE-bench Verified | higher-burden coding/agent benchmark | issue-resolution rate; variant-specific | 35 | frontier, progress, headroom, thresholds, velocity, coverage |

The counts above are an ingestion audit of the downloaded export, not product claims about benchmark quality. The export was retrieved from [Epoch AI's data page](https://epoch.ai/benchmarks/use-this-data) on 2026-09-03. Its included README states the data license and citation requirements.

## Data-source audit

- Primary benchmark metadata remains linked to each benchmark's original paper or official project.
- Epoch AI is treated as a trusted aggregator for this first slice, with `SourceProvenance.source_type = trusted_aggregator`.
- Internal and external runs remain distinguishable.
- Observations with missing model dates, missing source links, or incompatible settings are not silently discarded; normalization will emit a validation reason.
- The export's “Best score (across scorers)” field is not automatically interchangeable with every external score. Protocol class and source fields must be retained.

## Scope of the first local product

Implement one static snapshot and a vanilla browser read layer first. It must support:

- benchmark cards with compact SOTA frontier curves;
- calendar-age and since-release x-axis modes;
- raw and normalized y-axis modes when bounds exist;
- sorting by age, frontier, headroom, T50, T90, velocity, and current coverage;
- benchmark detail view with frontier provenance;
- distinct reached, right-censored, not-applicable, and unknown threshold states;
- separate health and evaluation coverage fields.

Discrimination, cost, adoption, and sophisticated lifecycle rules remain explicit `N/A` or `insufficient_data` until their raw inputs are available.
