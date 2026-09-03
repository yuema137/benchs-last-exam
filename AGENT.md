# Benchmark Observatory Repository Constitution

## Purpose

Benchmark Observatory tracks the lifecycle and measurement usefulness of benchmarks. It is not a model leaderboard and it must not make model ranking the primary product abstraction.

## Scope clarification

This is a lightweight personal benchmark knowledge base and **Leaderboard of Benchmarks**, not an evaluation platform or product infrastructure project.

Preferred architecture:

```text
curated source data → small Python scripts → generated JSON → static frontend → GitHub Pages
```

Optimize for simplicity, readability, maintainability, static deployment, and easy manual curation. Do not introduce a backend server, database, public API, user accounts, cloud services, telemetry system, or complex ingestion framework unless a later explicit decision requires one. If a local script and generated JSON solve the problem, they are the default choice.

The repository should remain a credible, inspectable research infrastructure project. Scientific correctness, provenance, reproducibility, and explicit uncertainty take priority over coverage or visual polish.

## Model coverage principle

The system is not intended to be model-complete. It must be model-representative. Models are measurement probes selected because they add temporal, organization, capability, openness, or domain coverage.

Benchmark health and evaluation coverage are independent dimensions. Low or stale coverage must produce `under_evaluated` or `unknown`, not `healthy` or `stagnating`. A lack of score movement is not evidence of stagnation when current frontier probes have not been evaluated.

Every reference model panel is versioned and time-dependent. Historical health at time `t` uses the panel active at `t`, not today's panel retroactively.

## Source of truth

- English documentation is canonical.
- Raw benchmark observations are immutable.
- Benchmark versions, metric definitions, protocols, and provenance are first-class records.
- Reference model panels and panel memberships are first-class, versioned records.
- Derived frontiers, metrics, lifecycle labels, and UI data are versioned outputs; they must be reproducible from the raw inputs.
- A public number without traceable provenance is not publishable.

## Cards and analytical views

- Each benchmark version has one benchmark-centric card or detail view.
- Cards document the benchmark and its current longitudinal evidence.
- Cross-benchmark questions belong in comparison and research views, not in individual factual fields.
- Activity/adoption, provenance quality, validity, and measurement health must remain separate dimensions.
- Use `N/A` when a metric is not scientifically applicable; use `?` or an explicit verification status when the required evidence is not yet known.

## Evidence rules

- Prefer the original paper, official benchmark repository, official leaderboard, or official project page.
- Verify titles, dates, URLs, metrics, settings, and numerical claims against the source.
- Never invent scores, release dates, ceilings, baselines, or uncertainty.
- Preserve conflicting observations instead of silently overwriting them.
- Record corrections, retractions, contamination findings, and protocol changes as validity/provenance events.
- If a value cannot yet be verified, use `TODO(reference)` or an explicit unavailable reason.

## Bilingual documentation

English is always the canonical tree. Chinese mirrors the same structure under `zh/`.

Working cycle:

1. Complete and review one English batch.
2. Synchronize the corresponding Chinese pages immediately.
3. Check that claims, formulas, labels, links, numbers, caveats, and N/A reasons match.
4. Read the Chinese page independently for naturalness and ambiguity.
5. Validate that every English page has exactly one expected Chinese counterpart.

Translation is semantic, not word-for-word. Benchmark names, model names, paper titles, project names, proper nouns, code identifiers, formulas, and stable metric labels remain unchanged unless a documented Chinese label is necessary. Chinese prose may restructure English sentences, but it may not strengthen, weaken, omit, or add a claim.

The Chinese mirror is not a second source of truth. Edit English first, then synchronize Chinese.

## Explanation style

Use the principles in `EXPLANATION_STYLE.md`. DongbeiGPT-style rhythm is restrained and accessible: it may make a user-facing explanation warmer and easier to follow, but it must never become dialect performance, jokes, catchphrases, or a change in scientific meaning.

The style applies to conversational explanations and explicitly selected explanatory prose. It does not apply automatically to code, code comments, schemas, tests, configuration, Git messages, API fields, or formal research claims.

## Engineering boundaries

- Keep source data, schema, validation, normalization, frontier computation, metrics, generated JSON, and UI modular.
- Prefer a small scripts/data/frontend structure over service boundaries. API and database layers are deferred and are not part of the current architecture.
- Keep scientific rules out of frontend components.
- Add tests with every metric implementation.
- Do not add a composite health score to the MVP.
- Do not assign lifecycle thresholds before inspecting empirical distributions.
- Preserve right-censored benchmarks for later survival analysis.
- Do not expand to 10–20 benchmarks or GitHub Pages deployment until the first 3–5 benchmark local slice has been used and validated.
