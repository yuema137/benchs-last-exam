# Benchmark Observatory: Initial Design Synthesis

Status: draft, 2026-09-03

> Scope clarification: this document describes a lightweight static benchmark knowledge base. Earlier platform-oriented ideas such as backend APIs, databases, scheduled ingestion, and scalable infrastructure are deferred and are not MVP requirements.

## A. Research and product synthesis

### Product thesis

Benchmark Observatory is a benchmark-centric, longitudinal, versioned observatory. A benchmark is the primary navigable entity; model evaluations are timestamped evidence used to reconstruct the benchmark's measurement trajectory.

The product should expose several interpretable dimensions rather than one opaque health score:

- normalized progress and remaining headroom, where a defensible floor and ceiling exist;
- time to T50, T80, and T90;
- recent frontier velocity;
- recent-model score distribution and discrimination;
- reporting activity and adoption as a separate dimension;
- explainable lifecycle state.

The homepage is a compact benchmark leaderboard table: one benchmark occupies one row so users can compare lifecycle fields quickly. A benchmark detail page is the card-like research view; it contains the complete frontier curve, provenance, coverage breakdown, caveats, and secondary metrics.

The first product is simply a local **Leaderboard of Benchmarks**: curated source data, small Python metric scripts, generated JSON, and a static frontend. It should be easy to run locally and later deploy unchanged to GitHub Pages.

### Model-representative coverage

The observatory is intentionally not model-complete. It maintains a small, versioned `ReferenceModelPanel` whose members are representative probes of the capability frontier. A model enters the panel only when it materially improves temporal, organization, capability, openness, or domain coverage.

For benchmark `B`, the expected panel is `P_B(t) = P_core(t) ∪ P_domain(B)(t)`. The panel is time-dependent: a 2024 health snapshot uses the panel active in 2024 and must not be judged using models released later.

This creates two independent axes: **Benchmark Health** (headroom, thresholds, frontier velocity, discrimination, saturation, stagnation) and **Evaluation Coverage** (whether sufficiently current and capable probes actually evaluated the benchmark). Coverage is evidence about the reliability of a health conclusion, not a component of health itself. Low or stale coverage produces `UNDER_EVALUATED` / `UNKNOWN`, not `HEALTHY` or `STAGNATING`.

At minimum expose historical coverage and current frontier coverage separately. A simple metric is `C_B(t; Δ) = weighted evaluated panel members in the recent window / weighted eligible panel members`. Equal weights are acceptable initially; preserve role and organization so later weighting can distinguish frontier probes, specialists, open-weight probes, anchors, and correlated members of one family.

### Entity model

```text
Benchmark
  └── BenchmarkVersion
        ├── MetricDefinition
        ├── evaluation protocol
        └── ScoreObservation[]
              ├── Model
              └── SourceProvenance
```

Raw observations are immutable. Frontiers, metrics, and lifecycle evidence are derived artifacts with explicit versions and lineage. Incompatible benchmark versions or protocols must never be silently merged.

### Recommended MVP scope

Start with 12 curated benchmarks across general knowledge, math, coding, science/reasoning, multimodal, and agents. Support accuracy, pass@1, and success-rate-like bounded metrics first. Keep unbounded, lower-is-better, relative-scale, and continuously refreshed benchmarks in the registry, but return explicit `N/A` for normalized thresholds until semantics are defensible.

The first release should provide deterministic Python scripts and a generated JSON snapshot. A frontend should consume the snapshot; it should not contain scientific rules. Parquet, APIs, databases, scheduled refreshes, and scalable infrastructure are deferred.

### Hard methodological problems

1. **Availability date:** release, evaluation, publication, and ingestion dates answer different questions. Use earliest defensible public availability for the default frontier date while preserving all timestamps.
2. **Comparability:** prompt, shot count, tools, sampling, grader, subset, and protocol changes can make two scores non-comparable.
3. **Normalization:** theoretical ceilings are not human baselines, and observed maxima are not fixed ceilings.
4. **Discrimination:** a spread among recent models is confounded by model-family duplication, protocol variation, and measurement error.
5. **SOTA significance:** a tiny new maximum may be noise. Preserve uncertainty and avoid “meaningful” claims when uncertainty is absent.
6. **Validity:** contamination, broken items, grading errors, and later corrections require validity flags and recomputation without deleting history.
7. **Censoring:** benchmarks that have not crossed T90 are right-censored, not failed observations; preserve this for later survival analysis.

### Prior-work position

The Benchmark Health Index motivates evaluating benchmarks themselves, but Observatory should expose the components separately rather than reproduce a composite index. Epoch AI is a useful possible data source and documents repeated evaluations and uncertainty; it remains a source adapter, not the product abstraction. Existing benchmark hubs remain useful evidence sources, but Observatory's primary unit is benchmark lifecycle.

### Lessons from `scientific-eval-environments`

The referenced repository is a useful adjacent design reference. Its strongest reusable ideas are:

- one lightweight factual card per primary object;
- source files as the source of truth and the interactive explorer as a generated read layer;
- separate navigation axes instead of forcing one taxonomy to answer every question;
- explicit first-public-appearance dates with linked provenance;
- conservative `N/A` and `?` semantics for non-applicable versus not-yet-verified fields;
- generated indexes and validation checks that keep cross-links consistent;
- factual cards separated from synthesis pages and chronological reports;
- human review in the update loop rather than trusting automated extraction.

For Observatory, adapt rather than copy that architecture. Immutable structured observations and benchmark/version registry records should be the source of truth; each benchmark card should be a generated or queryable presentation of them. Preserve the “card first, indexes second” mental model, but add snapshot IDs to every derived view. A Chinese mirror should not be introduced unless this repository later explicitly requires one. The reference project's separation of coverage from rigor is also a useful warning: measurement health, provenance quality, and community activity should remain separate dimensions.

### Risks

- apparent progress may reflect protocol or scaffold changes;
- published score coverage is selective and lab-dependent;
- a fixed ceiling can be scientifically wrong for open-ended tasks;
- activity can be mistaken for health;
- current frontier data may be sparse, duplicated, or unreproducible;
- benchmark quality and measurement health are related but distinct dimensions.

## B. Canonical schema proposal

The following is a logical schema; implementation may use Pydantic models and JSON Schema generated from them.

```yaml
Benchmark:
  id: string
  canonical_name: string
  aliases: [string]
  domains: [string]
  modality: [text, image, audio, video, code, multimodal]
  description: string
  maintainer: string|null
  versions: [benchmark_version_id]

BenchmarkVersion:
  id: string
  benchmark_id: string
  version_label: string
  release_date: date|null
  dataset_uri: string|null
  scoring_protocol: string
  metric_definition_id: string
  validity_status: enum[active, superseded, disputed, invalidated]
  comparability_notes: string|null

MetricDefinition:
  id: string
  name: string
  direction: enum[higher_is_better, lower_is_better]
  unit: string
  bounded: boolean
  floor: {value: number, type: enum[zero, random_chance, naive, human, benchmark_specific, unknown], provenance_id: string|null}|null
  ceiling: {value: number, type: enum[theoretical, human, empirical, unknown], provenance_id: string|null}|null
  normalization_policy_version: string

Model:
  id: string
  canonical_name: string
  family_id: string|null
  release_date: date|null
  provider: string|null
  model_card_uri: string|null
  organization: string|null
  roles: [historical_anchor, contemporary_frontier, domain_specialist, open_weight_frontier]
  domains: [string]
  panel_start: date|null
  panel_end: date|null
  inclusion_reason: string
  predecessor_id: string|null

ReferenceModelPanel:
  id: string
  label: string
  valid_from: date
  valid_until: date|null
  scope: enum[core, domain]
  domain: string|null
  member_ids: [string]
  methodology_version: string

PanelMembership:
  panel_id: string
  model_id: string
  role: enum[historical_anchor, contemporary_frontier, domain_specialist, open_weight_frontier]
  organization: string|null
  weight: number
  valid_from: date
  valid_until: date|null
  inclusion_reason: string

SourceProvenance:
  id: string
  source_type: enum[primary, trusted_aggregator, secondary]
  url: string
  title: string|null
  publisher: string|null
  publication_date: date|null
  retrieved_at: datetime
  source_revision: string|null
  citation: string|null

ScoreObservation:
  id: string
  benchmark_version_id: string
  model_id: string
  score: number
  score_unit: string
  evaluation_date: date|null
  reported_date: date|null
  public_available_date: date|null
  evaluation_protocol: string
  setting: string|null
  reported_uncertainty: {lower: number|null, upper: number|null, kind: string}|null
  provenance_ids: [string]
  validity_status: enum[unverified, verified, disputed, retracted]
  notes: string|null
  ingested_at: datetime
  parser_version: string

FrontierPoint:
  benchmark_version_id: string
  as_of_date: date
  frontier_score: number
  source_observation_ids: [string]
  direction: enum[higher_is_better, lower_is_better]
  derivation_version: string

DerivedBenchmarkMetrics:
  benchmark_version_id: string
  snapshot_id: string
  current_frontier: number|null
  normalized_progress: number|null
  normalized_headroom: number|null
  threshold_days: {T50: number|null, T80: number|null, T90: number|null}
  velocity: {d30: number|null, d90: number|null, d180: number|null, d365: number|null}
  discrimination: object|null
  last_frontier_change_date: date|null
  activity: object
  evaluation_coverage: {historical: object, current_frontier: object, eligible_panel_ids: [string]}
  unavailable_reasons: [string]

LifecycleState:
  label: enum[emerging, healthy, rapidly_solving, saturating, saturated, stagnating, dormant, insufficient_data]
  rule_version: string

LifecycleEvidence:
  benchmark_version_id: string
  snapshot_id: string
  state: LifecycleState
  evidence: [{metric: string, value: any, rule: string, explanation: string}]

DataSnapshot:
  id: string
  as_of: datetime
  raw_input_revisions: [string]
  transformation_version: string
  metric_definition_version: string
  lifecycle_rule_version: string
  artifact_uri: string
  created_at: datetime
```

## C. Metric specification

Let `F` be the benchmark floor, `C` its defensible ceiling, `s(t)` the step-function historical frontier, and `r` the release/public-availability date.

| Metric | Definition | Applicability / edge cases | Output and tests |
|---|---|---|---|
| Current frontier | `max(score)` for higher-is-better; `min(score)` for lower-is-better | Valid, comparable observations only; never merge versions | Score in native unit. Test direction, ties, invalid and out-of-order rows |
| Normalized progress | `(s-F)/(C-F)` for higher-is-better; `(C-s)/(C-F)` for lower-is-better | Requires fixed meaningful `F`, `C`, and `C != F`; flag out-of-range values | Unit interval, with explicit clamp/flag policy. Test zero/random floor, missing bounds, lower-is-better |
| Normalized headroom | `1 - progress` | Same as progress | Unit interval. Test exact ceiling/floor |
| T50/T80/T90 | Earliest `t >= r` where normalized progress `>= q` | `N/A` without defensible fixed bounds; threshold exact hits count; no crossing is censored | Duration from `r`, plus crossing date. Test exact crossing, never reached, same-day reports |
| Frontier velocity (30/90/180/365d) | `(s(now)-s(now-window))/window`; use a documented step-function boundary policy | Sparse data returns `N/A` or a flagged estimate; native and normalized variants should be distinct | Score points/day or normalized progress/month. Test no boundary observation and no prior observation |
| Recent frontier discrimination | For a configured recent qualified cohort, emit `n`, median, IQR, standard deviation, top-minus-k spread, and raw observations | Do not collapse to one number; cohort definition, family deduplication, protocol class, and uncertainty must be visible | Native score units. Test fewer-than-minimum observations, duplicate family, uncertainty present |
| Days since last SOTA | `as_of - last frontier change date` | Report raw delta; do not call it meaningful without a configured threshold or uncertainty | Days plus last-change date. Test ties and retractions |
| Recent activity | Counts of observations, distinct model families, and reports in 30/90/180d | Separate from measurement health; preserve source and deduplication policy | Counts/rates. Test duplicate reports and multiple observations per model |
| Evaluation coverage | Weighted or equal-weight fraction of eligible, time-appropriate panel members evaluated within a stated window; report by role, organization, and domain | Requires a versioned panel and a capability/time window; low/stale coverage blocks strong lifecycle claims | Unit interval plus counts and freshness. Test historical panel selection, panel end dates, missing evaluations, and domain specialists |

Lifecycle labels should initially remain `insufficient_data` or `under_evaluated` until empirical distributions and panel coverage are inspected. `under_evaluated` takes precedence when current frontier coverage is below the evidence threshold. `stagnating` requires adequate recent coverage, substantial remaining headroom, and low frontier movement over a sustained period. Rules must emit evidence and explanations, for example: “current frontier coverage 82%; 92% normalized progress; 1.2 pp recent IQR; +0.4 pp frontier gain in 180d.” No composite health score is required for MVP.

## D. Pilot benchmark proposal

The table proposes candidates and authoritative metadata sources; it intentionally does not fill scores or unverified release dates. Dates should be extracted into the registry from the cited primary source during ingestion.

| Benchmark / version candidate | Domain | Metric | Floor / ceiling candidate | Release-date source | Data-source candidates | Normalized T metrics |
|---|---|---|---|---|---|---|
| MMLU | General knowledge | Accuracy | Random-choice floor and perfect-score ceiling, subject to version/protocol | [original paper](https://arxiv.org/abs/2009.03300) | Official repo, technical reports, Epoch | Valid for fixed compatible version |
| GSM8K | Math | Exact-answer accuracy | Zero or documented baseline; perfect ceiling | [original paper](https://arxiv.org/abs/2110.14168) | Official repo, Epoch, reports | Valid if exact-answer protocol is fixed |
| MATH / MATH-500 | Math | Accuracy | Distinguish original and curated versions; ceiling is perfect score | [MATH paper](https://arxiv.org/abs/2103.03874) | Official data, reports, Epoch | Version-specific |
| HumanEval | Coding | pass@1 | Zero / perfect ceiling; sampling protocol is essential | [Codex paper](https://arxiv.org/abs/2107.03374) | Official repo, reports, Epoch | Valid only within a fixed pass@k protocol |
| GPQA Diamond | Science reasoning | Accuracy | Four-choice random floor only if the subset and scoring are fixed; perfect ceiling | [GPQA paper](https://arxiv.org/abs/2311.12022) | Official repo, reports, Epoch | Valid with strong data-quality caveats |
| SWE-bench | Agents/coding | Issue resolution rate | Zero / perfect ceiling, but repository and test protocol matter | [original paper](https://arxiv.org/abs/2310.06770) | Official leaderboard, verified variants, reports | Separate each variant; never merge silently |
| MMMU | Multimodal knowledge | Accuracy | Multiple-choice floor depends on item format; perfect ceiling | [MMMU paper](https://arxiv.org/abs/2311.16502) | Official repo, reports, Epoch | Version/protocol-specific |
| MathVista | Multimodal math | Accuracy | Item-format-specific floor; perfect ceiling | [MathVista paper](https://arxiv.org/abs/2310.02255) | Official repo, reports | Likely valid per fixed version |
| SimpleQA | Factuality | Exact-match / graded accuracy | Ceiling may be perfect; floor depends on grading and abstention policy | [SimpleQA paper](https://arxiv.org/abs/2410.02052) | Official repo, reports, structured aggregators | Conditional on stable grader |
| Humanity's Last Exam | Broad expert knowledge | Accuracy | Do not assume a clean floor or error-free ceiling; preserve audit metadata | [HLE paper](https://arxiv.org/abs/2501.14249) | Official release, reports, trusted aggregators | Provisional; validity uncertainty is central |
| ARC-AGI-1 | Abstract reasoning | Task success rate | Zero / perfect ceiling for fixed task set | [ARC-AGI paper](https://arxiv.org/abs/1911.01547) | Official benchmark/repo, reports | Valid per fixed task-set version |
| ARC-AGI-2 | Abstract reasoning | Task success rate | Fixed-version bounds only | [ARC Prize](https://arcprize.org/arc-agi-2) | Official leaderboard, reports | Validate release/version semantics first |
| FrontierMath | Advanced math | Accuracy / task success | Ceiling and floor require benchmark-owner metadata; private test semantics | [Epoch benchmark context](https://epoch.ai/benchmarks) | Official source, Epoch where available | N/A until bounds are defensible |

This is a candidate set, not a claim that every row is immediately ingestible. A benchmark enters the first published snapshot only after metadata, protocol comparability, and provenance checks pass.

## E. Implementation plan

The immediate implementation is a vertical slice, not a horizontal framework build:

```text
real observations → small metric script → JSON snapshot → static cards → sorting and chart toggles
```

### Milestone 1: repository and contracts

Files: `README.md`, `docs/design-synthesis.md`, `src/schema/`, `pyproject.toml`.

Acceptance: schemas validate examples and reject missing provenance, invalid directions, and incompatible bound definitions. Add schema tests.

### Milestone 2: curated registry and raw fixtures

Files: `data/benchmark_registry/`, `data/fixtures/`, `src/validation/`, `src/provenance/`.

Acceptance: 3–5 initially verified benchmark versions have source-backed metadata; raw observations are immutable and every public row has provenance. Add validation and duplicate/conflict tests.

### Milestone 3: frontier and metric engine

Files: `src/frontier/`, `src/metrics/`, `tests/test_frontier.py`, `tests/test_metrics.py`.

Acceptance: deterministic frontier, normalization, threshold, velocity, discrimination, activity, and last-SOTA computations; all metric edge cases in section C pass.

### Milestone 4: snapshot CLI

Files: `src/snapshots/`, `scripts/build_snapshot.py`, `data/snapshots/`.

Acceptance: one command produces a versioned artifact containing raw references, derived records, unavailable reasons, and transformation versions; rerunning the same inputs is byte-stable or has documented ordering normalization.

### Milestone 5: pilot expansion and manual audit

Files: registry and fixtures for the full pilot, `docs/methodology.md`.

Acceptance: 10–20 benchmarks are included only where their metadata and protocol are defensible; manually inspect every frontier curve and publish a limitations report.

### Milestone 6: static benchmark cards and comparison table

Files: `site/`, static JSON loader, and browser UI modules.

Acceptance: benchmark-centric cards show current frontier, headroom, thresholds, velocity, discrimination distribution, activity, lifecycle evidence, and clickable provenance. No frontend-local metric logic.

### Milestone 7: global lifetime analysis

Files: `src/analysis/`, `apps/web/` global views, tests.

Acceptance: release date vs T90 plot distinguishes crossed and right-censored benchmarks; filters by domain and metric applicability; no fabricated values.

### Milestone 8: source adapters and refresh (deferred)

Files: `src/ingestion/`, adapter-specific tests, refresh CLI/workflow.

Acceptance: fetch → parse → normalize → validate → conflict report → snapshot is reproducible for at least one structured source. Adapter quirks do not leak into metric code.

This milestone is not required for the first local demo. Manual curation and a checked-in source export are preferred until the vertical slice proves useful.

## Initial decisions and open decisions

Decide now: benchmark/version identity, immutable raw observations, source tiers, explicit `N/A`, and separate activity from health.

Defer until pilot data inspection: lifecycle thresholds, family deduplication, minimum frontier cohort size, “meaningful” SOTA delta, interpolation policy, and whether to use the term “half-life.”
