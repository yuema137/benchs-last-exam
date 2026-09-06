# Benchmark Integration Contract

Adding a benchmark is an end-to-end repository transaction, not a data-file edit.

The canonical active benchmark registry is the set of typed records under:

```text
data/benchmarks/<benchmark-id>.json
```

There is exactly one source record per active benchmark/version. The filename must equal the benchmark ID. `src/benchmark_observatory/registry.py` validates every record before any snapshot computation begins; `scripts/build_snapshot.py` contains computation only and must not contain benchmark/card declarations. There is no separate handwritten leaderboard or lifecycle-tab inclusion list.

`registry_order` is a unique contiguous integer used to preserve deterministic ingestion and tie-breaking. New records use the next integer. It does not control story-tab membership or leaderboard sorting.

A complete addition provides:

1. canonical identity, version, release date, Evaluation Type, and Domain;
2. concise English and Chinese summary, task format, scoring explanation, and evaluation target;
3. benchmark resources and source-linked canonical observations;
4. resolvable models, dates, protocols, and capability-frontier lineage;
5. derived lifecycle metrics, coverage, and cost (`Unknown`, `N/A`, or `—` when evidence is insufficient);
6. generated leaderboard/detail data and automatic lifecycle-tab eligibility.

Lifecycle synchronization is a build invariant. Every build regenerates the membership IDs for all four story views (`test-of-time`, `still-frontier`, `fastest-solved`, and `recently-saturated`) from the same canonical benchmark metrics. The frontend consumes those generated IDs; it must not keep a separate manual list or selector that can become stale. Adding or updating a benchmark is incomplete until all four generated views and their empty/non-empty states validate together.

Selector semantics and visible card semantics must also match. `Still Frontier` means right-censored T50 with normalized progress below 50% and sufficient evidence. Its card therefore leads with normalized progress. A raw score above 50% can still correspond to normalized progress below 50% when the benchmark has a non-zero chance/reference baseline; raw score may be shown as a separately labeled supporting value, never as the value behind the “below 50%” claim.

## Canonical and auxiliary score contract

Each active benchmark/version has exactly one `canonical_score` record. It pins the metric, task set, evaluation protocol, direction, score format/unit, and progress baseline/target. Canonical observations carry the matching `score_series_id` and `score_role: canonical`. All cross-benchmark metrics and views consume only this series.

Any additional score belongs in `auxiliary_score_series`, even when it shares the benchmark family name. Typical examples are a different task subset, pass@k setting, voting/scaffolding protocol, alternate judge, secondary metric, or an unverified leaderboard task set. Auxiliary observations remain canonical provenance records, but each series must:

- declare `role: auxiliary` and `lifecycle_eligible: false`;
- identify its own metric, protocol, and task set;
- explain why it differs from the canonical score in English and Chinese;
- preserve observation IDs and source lineage;
- render only on the detail page with a distinct legend/color treatment;
- remain excluded from the canonical frontier, leaderboard sorting, T50/T80/T90, headroom, velocity, and all lifecycle selectors.

The generated snapshot, integration validator, frontend defensive selector, and regression tests all enforce this boundary. A benchmark with no auxiliary data still emits an empty `auxiliary_score_series` list so the contract is explicit.

## Evidence and canonical measurement identity

One imported source row is an immutable evidence record, not automatically a
new scientific measurement. Evidence IDs are based on a source row ID when one
exists, otherwise on normalized row content; CSV position is never identity.

Evidence rows may merge into one canonical observation only when all of these
match exactly:

```text
benchmark version
model configuration
normalized model/display setting
score series and role
protocol
task set
normalized score
```

This deliberately keeps different prompting labels, harnesses, task subsets,
and metrics separate. A merged observation retains every evidence ID and score
resource. The generated `data/evidence.jsonl` must reconcile one-to-one with
the evidence IDs referenced by canonical observations: no evidence may be
orphaned or linked to multiple measurements.

Leaderboard rows and lifecycle cards are generated views. No benchmark may be manually assigned to a story tab, and no chart-only score is allowed. Active benchmark IDs must be represented by generated leaderboard and detail data.

Run the acceptance check after every benchmark addition or observation update:

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_score_semantics.py
python3 scripts/validate_benchmark_integration.py
python3 scripts/audit_observation_dates.py
python3 scripts/audit_canonical_identity.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The integration validator checks that every generated story-view list exists, contains unique IDs, and resolves to active benchmarks. A benchmark may legitimately be absent from a view; it may not be unresolved or omitted because only another tab was refreshed.

Selection evidence such as citation counts belongs in curation documentation, with its source and check date. It is not a leaderboard metric. Missing longitudinal data is not by itself a reason to defer an important benchmark; unclear identity, version, metric, or incompatible measurement objects are.

## Add or edit one benchmark

1. Create or edit only its `data/benchmarks/<id>.json` declaration for identity, taxonomy, bilingual copy, canonical score, protocol, normalization, and source-file binding.
2. Add or update the corresponding `data/raw/<file>.csv` evidence rows.
3. Do not edit `site/data/benchmarks.json`, leaderboard rows, detail-page objects, or lifecycle memberships by hand.
4. Run the acceptance sequence above. The build discovers every registry file, produces its leaderboard/detail representation, and derives all story views from canonical metrics.

The typed loader rejects missing EN/ZH copy, unsupported types/units, unknown fields, duplicate IDs or measurement identities, missing raw files, non-HTTP sources, and non-contiguous registry order. The integration validator requires the generated benchmark IDs to match the registry IDs in the same deterministic order.
