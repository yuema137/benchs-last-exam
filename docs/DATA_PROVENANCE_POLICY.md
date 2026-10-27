# Data Provenance and Licensing Policy

This policy says where BLE numbers may come from, how third-party material is
reused, and which license covers which part of the repository. It complements
the resource and lineage model in [`PROVENANCE.md`](PROVENANCE.md).

This document records the terms BLE found in primary sources and how BLE reads
them. It is not legal advice.

## 1. Licenses in this repository

| Material | License |
| --- | --- |
| Code: site (`site/*.html`, `site/*.js`, `site/*.css`), scripts, pipeline (`scripts/`, `src/`), tests | MIT, see [`LICENSE`](../LICENSE) |
| BLE's own data and writing: scores, rankings, frontiers, lifecycle metrics and classifications that BLE computes; benchmark cards in `data/benchmarks/`; documentation | CC BY-SA 4.0, see [`LICENSE-DATA`](../LICENSE-DATA) |
| Third-party results and materials: source rows in `data/raw/`, `raw_fields` in `data/evidence.jsonl`, linked papers, leaderboards, logs and vendor releases | Their original terms; see [`NOTICE`](../NOTICE) and section 5 |

Copyright for the MIT and CC BY-SA 4.0 parts: 2026 Yue Ma.

A third-party number does not become CC BY-SA 4.0 because BLE republishes or
transforms it. The CC BY-SA 4.0 license applies to BLE's own contribution:
selection, normalization, derived metrics, classifications and prose.

## 2. Every observation cites its original source

- Each canonical observation must have at least one `source_ids` entry that
  resolves to the original source of the number: the benchmark paper, the
  official benchmark leaderboard, the vendor's model card, system card or
  release post, or the evaluator's own run record (for example an Epoch AI
  evaluation log for a run Epoch AI performed).
- The number is read from that original source. Values are never copied from a
  discovery tool or a secondary compilation without re-reading the original.
- An aggregator may be cited in addition to the original source when it adds
  something (a log, a run date), never instead of it for a new observation.
- The existing evidence rules in [`AGENT.md`](../AGENT.md) still apply:
  verify titles, dates, URLs, metrics and settings; never invent values; keep
  conflicting observations.

## 3. benchmark-radar is a discovery source only

[benchmark-radar](https://github.com/ktwu01/benchmark-radar) by Koutian Wu
(<https://benchmark-radar.org/>) tracks where AI benchmark and evaluation
results are reported. BLE may use it to *find* candidate sources. It may not
be cited as the source of any number, and no benchmark-radar content (values,
descriptions, caveats, curated lists, identity links or briefings) is copied
into BLE or redistributed.

- The only place benchmark-radar may be named in BLE data is an explicit
  discovery-source field named `discovered_via` (a raw CSV column
  `discovered_via` or `Discovered via`, or a `discovered_via` key in a JSON
  record). That field is attribution only. It never feeds lineage,
  eligibility, dates or scores.
- `scripts/validate_provenance.py` enforces this. It fails when:
  1. an observation's only cited sources are benchmark-radar resources (any URL
     on `benchmark-radar.org`, `github.com/ktwu01/benchmark-radar`,
     `ktwu01.github.io/benchmark-radar` or
     `huggingface.co/datasets/ktwu01/benchmark-radar`); or
  2. benchmark-radar is named or linked anywhere other than a
     `discovered_via` field, whether in the generated snapshot, in
     `data/raw/*.csv` or in `data/benchmarks/*.json`. This includes a
     benchmark-radar resource cited alongside an original source.
- The test is `tests/test_provenance_policy.py`.

Its acknowledgement is in the README, on the site and in `NOTICE`.

## 4. No bulk import against a source's terms

- Do not bulk-import or repackage any curated third-party dataset whose terms
  forbid redistribution, dataset packaging, commercial use or derivative works,
  or whose terms are unknown. benchmark-radar's content falls in this group.
- A bulk source may be used only when its terms allow redistribution with
  attribution (for example CC BY 4.0). Record the source and its terms in
  section 5 and in `NOTICE` before the import.
- Facts read one at a time from an original paper, leaderboard or vendor
  release, and cited there, are the normal path for new observations.

## 5. Third-party terms register

Retrieved 2026-10-27. Quotes are verbatim from the linked pages.

### Epoch AI Benchmarking Hub (largest bulk source)

Sources: <https://epoch.ai/benchmarks/use-this-data> (section "Licensing"),
<https://epoch.ai/benchmarks/about> ("How is the data licensed?"),
<https://epoch.ai/data/ai-benchmarking-dashboard>.

> "Epoch AI's data is free to use, distribute, and reproduce provided the
> source and authors are credited under the Creative Commons Attribution
> license. [...] Benchmark questions and answers are the property of their
> respective creators. This hub also includes data sourced from external
> projects, which retains its original licensing. Users are responsible for
> complying with the license terms of the specific data they use, and should
> credit the original sources as indicated."

The "Creative Commons Attribution license" link on both pages points to
<https://creativecommons.org/licenses/by/4.0/>. Suggested citation on the same
page: "Epoch AI, 'Capabilities & benchmarking'. Published online at epoch.ai.
Retrieved from 'https://epoch.ai/benchmarks/use-this-data' [online resource]."

What it allows: use, redistribution and adaptation, including commercial use,
with attribution (CC BY 4.0). No share-alike requirement and no
non-commercial restriction.

BLE use: 623 of 933 resources are Epoch AI evaluation logs, and 690 of 4,813
canonical observations cite an Epoch AI resource. Many `data/raw/*.csv` files
use the hub's export layout (internal runs and external runs).

Compatibility with CC BY-SA 4.0: compatible for Epoch AI's own data. CC BY 4.0
Section 3(a)(4) requires only that "the Adapter's License You apply must not
prevent recipients of the Adapted Material from complying with this Public
License" (<https://creativecommons.org/licenses/by/4.0/legalcode>), and
CC BY-SA 4.0 does not prevent that. Conditions BLE must keep: credit Epoch AI,
link the license, indicate that BLE modified the data, and keep the verbatim
Epoch rows under CC BY 4.0 rather than relabeling them. The hub's
external-runs rows are different: Epoch says they keep their original
licensing (see section 6).

### Official leaderboards and benchmark repositories used in bulk

License fields as reported by the GitHub API for each repository on
2026-10-27:

| Source | BLE use | Stated terms |
| --- | --- | --- |
| Stanford HELM / CRFM leaderboards (<https://crfm.stanford.edu/helm/>) | 248 evidence rows cite "Stanford HELM" or "Stanford CRFM Leaderboard" | Framework repository <https://github.com/stanford-crfm/helm> is Apache-2.0. BLE found no separate license statement for the published leaderboard results. |
| Aider leaderboards (<https://aider.chat/docs/leaderboards/>) | 61 evidence rows | Leaderboard data is kept in <https://github.com/Aider-AI/aider> (Apache-2.0). |
| Terminal-Bench leaderboard (<https://www.tbench.ai/>) | 105 evidence rows | <https://github.com/harbor-framework/terminal-bench> is Apache-2.0. |
| ScienceQA leaderboard | 81 evidence rows | <https://github.com/lupantech/ScienceQA> is MIT. |
| Video-MME leaderboard | 49 evidence rows | No license detected for <https://github.com/MME-Benchmarks/Video-MME>. |
| Artificial Analysis (<https://artificialanalysis.ai/>) | SciCode (198 evidence rows, 195 observations) and GDPval-AA v2 (35 observations) cite Artificial Analysis pages | Website Terms of Use v1.0, last revised April 28 2024 (<https://artificialanalysis.ai/docs/legal/Terms-of-Use.pdf>): a license "solely for your own personal, noncommercial use"; "you shall not license, sell, rent, lease, transfer, assign, distribute, host, or otherwise commercially exploit the Site, whether in whole or in part, or any content displayed on the Site"; "no part of the Site may be copied, reproduced, distributed, republished, downloaded, displayed, posted or transmitted in any form or by any means". |

### benchmark-radar

Sources: <https://github.com/ktwu01/benchmark-radar> (`LICENSE`: MIT) and
`LICENSE-CONTENT.md` in the same repository:

> "Software: MIT License. Technical report and original editorial content:
> CC BY-NC-SA 4.0. Commercial republication, resale, paid newsletters, dataset
> packaging, or commercial product integration requires prior written
> permission from Koutian Wu. Adaptations must be shared under the same terms.
> Third-party source material remains under its original terms."

BLE use: discovery only (section 3). Because nothing is copied, no
benchmark-radar terms attach to BLE's data. CC BY-NC-SA content could not be
included under CC BY-SA 4.0, which allows commercial use. This is another
reason for the no-copy rule.

## 6. Open licensing items

These are unresolved. They are recorded here, not papered over.

1. **Artificial Analysis rows conflict with CC BY-SA 4.0.** The Artificial
   Analysis Terms of Use allow only personal, noncommercial use and forbid
   copying, redistribution and republication. BLE redistributes 198 SciCode
   and 8 GDPval-AA v2 raw rows that reference Artificial Analysis pages, plus
   derived values for 230 observations. CC BY-SA 4.0 allows commercial use.
   Whether individual scores are protectable is a separate question from the
   contractual terms of use. BLE does not resolve it here. Until the
   maintainer decides (re-source from original papers or vendor releases,
   remove, or obtain permission), these rows are marked as third-party under
   their original terms in `NOTICE` and are not covered by `LICENSE-DATA`.
2. **Epoch AI external-runs rows keep their original terms.** Epoch states
   that external data "retains its original licensing". BLE has not audited
   the terms of every paper, leaderboard and vendor page behind those rows.
   BLE also does not yet record, per row, whether it came from an Epoch export
   or from a direct read. A per-row `source_dataset` field would make the
   applicable terms checkable.
3. **HELM and Video-MME results have no explicit data license.** The HELM
   framework is Apache-2.0, but BLE found no statement covering the published
   leaderboard results. No license was detected for the Video-MME repository.
   Their terms are unknown, not permissive.
4. **Mixed-license data bundle.** `site/data/*.json` combines BLE-derived
   values (CC BY-SA 4.0) with third-party facts and source titles (original
   terms). The split in section 1 is the rule. The files themselves do not yet
   carry per-field license markers.
