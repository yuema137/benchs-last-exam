# Model-Release Update Protocol

This project is a curated **Leaderboard of Benchmarks**, not an exhaustive
model or literature database. When a new model release page, model card, or
system card is used to update benchmark observations, the update must begin
with a source-level inventory.

The required order is:

```text
inventory the source
→ reconcile with the benchmark registry
→ update canonical observations
→ rebuild derived data
→ validate completeness and provenance
```

## 1. Inventory before editing data

Enumerate every externally reported benchmark or evaluation shown by the
source, including results exposed through:

- accessible HTML text and tables;
- tabs, carousels, and linked model/system cards explicitly referenced by the
  release page;
- embedded JSON or script data;
- SVG or other chart DOM data;
- browser network responses or JavaScript state when available;
- images or canvas charts, using visual extraction only as a fallback.

The temporary inventory should record:

```text
benchmark/evaluation
score, if extractable
metric
source location
extraction method
```

Structured extraction is preferred to visual transcription. A chart that is
not present in the initial page text is not evidence that its data are absent.

## 2. Reconcile with the curated registry

Match the complete source inventory against the tracked benchmark registry.
Each matched item must end in exactly one state:

```text
UPDATED
ALREADY CURRENT
SKIPPED_WITH_REASON
EXTRACTION_FAILED
NOT TRACKED
```

The reconciliation must balance:

```text
tracked source results
= UPDATED + ALREADY CURRENT + SKIPPED_WITH_REASON + EXTRACTION_FAILED
```

`NOT TRACKED` is reported separately because it identifies a possible future
curation candidate rather than an update to an existing benchmark.

No matched result may silently disappear between inventory and report.

## 3. Canonical observation requirements

Every accepted score is a canonical observation in the curated source data.
It must include or resolve to:

- benchmark and benchmark version;
- model/system and model family;
- score and metric;
- protocol or evaluation setting;
- model release date for the capability timeline;
- evaluation and result-public dates when known;
- one or more canonical resource IDs.

The frontend never receives a chart-only score. Frontier points are derived
from canonical observations and retain their observation ID and source
lineage.

Do not merge results with materially different benchmark versions, task sets,
scorers, prompts, harnesses, or tool settings. If a difference matters and
cannot be reconciled, use `SKIPPED_WITH_REASON` or `EXTRACTION_FAILED` and
explain why.

## 4. Extraction order

Use this order when inspecting an official source:

1. semantic HTML and accessible text;
2. HTML tables;
3. embedded JSON or script data;
4. SVG DOM labels/data;
5. browser network responses or page JavaScript state;
6. screenshot/image visual reading as a fallback.

Record the method used in the update audit. Visual extraction must preserve a
source screenshot or direct source location where practical and should not be
used to guess values hidden by unreadable graphics.

## 5. Required update report

Every model-release update should leave a short audit record, for example:

```text
Model: Example Model
Source: https://example.com/release

Benchmark                         Found  Tracked  Result
GPQA Diamond                     yes    yes      UPDATED
OSWorld 2.0                     yes    yes      ALREADY CURRENT
Example New Benchmark            yes    no       NOT TRACKED
Chart-only evaluation           yes    yes      EXTRACTION_FAILED
```

The report must also list:

- all source evaluations not tracked by the project;
- scores that could not be extracted reliably;
- extraction method for non-text results;
- protocol/version caveats;
- observations added or confirmed;
- any provenance gaps.

## 6. Update directions

Two independent discovery directions are supported by the resource model:

```text
benchmark resources → discover new model results
model resources     → discover new benchmark results
```

This protocol does not authorize an automated crawler, scheduler, backend, or
database. Updates remain manually curated and reproducible from checked-in
source data.

## 7. Completion rule

An update is complete only after:

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_provenance.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

and the source inventory/reconciliation report has no unexplained unmatched
items.
