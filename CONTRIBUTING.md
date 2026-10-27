# Contributing to BLE

BLE is deliberately selective. It follows a small set of classic, widely
followed benchmarks and aims to show frontier progress with relatively little
information. It does not aim for comprehensive coverage. A benchmark that is
new, niche or sparsely evaluated may be valuable, but it belongs in the
curation queue until the evidence below exists.

Before contributing, read [`AGENT.md`](AGENT.md), the
[Benchmark Integration Contract](docs/BENCHMARK_INTEGRATION.md) and the
[Data Provenance and Licensing Policy](docs/DATA_PROVENANCE_POLICY.md).

## Inclusion criteria (initial policy)

These thresholds are the initial policy. They will be revised once they have
been applied to the existing registry. A benchmark/version qualifies for the
site only when it meets **all** of the following:

1. **Fixed task set with a clear score.** The benchmark has a pinned, versioned
   task set and one defensible canonical score with a declared direction and
   unit. Rolling or mutable task sets need an explicit versioned snapshot
   first.
2. **Widely followed.** At least one of:
   - results for the benchmark appear in the official launch materials (model
     card, system card, technical report or release post) of models from at
     least **two** different reference organizations listed in
     `data/organizations.json` (currently OpenAI, Anthropic, Google, DeepSeek,
     Qwen, Meta and xAI), within the 18 months before the proposal; or
   - the benchmark is tracked by a major independent leaderboard that runs or
     compiles results across labs (for example the Epoch AI Benchmarking Hub
     or Stanford HELM).
3. **Current frontier results.** At least **three** source-linked canonical
   observations for models released in the 12 months before the proposal,
   from at least **two** different reference organizations.
4. **Traceable provenance.** Every observation cites its original paper,
   leaderboard, evaluation log or vendor release, as required by the
   provenance policy. A discovery tool such as benchmark-radar is never a
   source.

A benchmark without that evidence goes to
[`CURATION_QUEUE.md`](CURATION_QUEUE.md), not to the site. Record which
criterion is missing so the entry can be re-checked later.

These criteria govern new additions. Benchmarks already in the registry are
reviewed against them separately. This policy does not by itself remove an
existing card.

## How to contribute

- **New observation for an existing benchmark:** add a row to the benchmark's
  `data/raw/*.csv` file, read from the original source, with its source link
  and dates. If you found the result through a discovery tool, you may name it
  in a `discovered_via` column; that column is attribution only.
- **New benchmark:** add one complete typed record under
  `data/benchmarks/<benchmark-id>.json` that satisfies the Benchmark
  Integration Contract, plus its raw observation file.
- **Corrections:** preserve the conflicting observation and record the
  correction as a validity/provenance event; never silently overwrite.
- **Documentation:** English is canonical. Update the Chinese mirror under
  `zh/` in the same change.

Run the full integration gate listed in the [README](README.md) before
submitting.

## Licensing of contributions

By contributing, you agree that code you contribute is licensed under the MIT
License ([`LICENSE`](LICENSE)), and that data and writing you contribute are
licensed under CC BY-SA 4.0 ([`LICENSE-DATA`](LICENSE-DATA)). Third-party
results you add keep their original terms; cite them, and do not bulk-import a
dataset whose terms forbid it.
