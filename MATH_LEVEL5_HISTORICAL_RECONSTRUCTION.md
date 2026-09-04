# MATH Level 5 Historical Reconstruction

Status: **not reconstructed**. The current 108 standardized Epoch
observations remain retrospective data and are excluded from the historical
frontier and lifecycle metrics.

## Decision

There is not yet enough evidence to construct a defensible single historical
frontier for MATH Level 5. The candidate results below establish that the
subset was evaluated publicly over time, but they do not establish one
comparable protocol and one first-public date for each result. The snapshot
therefore keeps:

```text
Historical frontier: unavailable
T50: Unknown
T80: Unknown
T90: Unknown
```

This is preferable to treating a later standardized re-run as if it had been
known when the model was released.

## Candidate historical results

| Candidate | Public evidence date | Subset evidence | Protocol notes | Decision |
|---|---|---|---|---|
| GPT-2 1.5B, approximately 4% on Level 5 | 2021-03-05 paper preprint | The original MATH paper reports results by difficulty level, including Level 5 | Original MATH evaluation; exact prompt/decoding details must be checked against later results | Candidate only; no later comparable point yet |
| Minerva 540B, 33.6% on Level 5 | 2022-06-29 paper preprint | Minerva reports the MATH difficulty breakdown | Four-shot prompting and sampled majority voting; not directly comparable to a single-sample baseline | Rejected from one frontier |
| GPT-4, 23.1% | Publicly listed later in Epoch's 2025 analysis | Epoch table labels the column MATH Level 5 | The table uses model release dates and says its data combine Epoch Hub data with release announcements and leaderboards; the first public result date and exact protocol are not supplied | Rejected from historical frontier |
| GPT-4 Turbo, 40.0% | Publicly listed later in Epoch's 2025 analysis | Epoch table labels the column MATH Level 5 | Exact original report/protocol and first-public date are not established in the available export | Rejected from historical frontier |
| GPT-4o, 51.0% (May 2024) | Publicly listed later in Epoch's 2025 analysis | Epoch table labels the column MATH Level 5 | Later standardized/aggregated evidence; public-result date and scorer provenance are not established here | Rejected from historical frontier |
| Llemma | 2023-10-16 paper preprint | The paper reports MATH results, but the available abstract does not establish a Level 5 score | MATH aggregate and Level 5 are not interchangeable | Rejected: subset not explicitly established |

The original MATH paper defines a 12,500-problem competition-mathematics
dataset and the relevant difficulty breakdown. The Minerva paper explicitly
describes a fixed four-shot prompt and majority selection over sampled
solutions. These are materially different evaluation procedures, even when
both report a Level 5 result.

Sources: [MATH paper](https://arxiv.org/abs/2103.03874), [Minerva paper](https://arxiv.org/abs/2206.14858), [Llemma paper](https://arxiv.org/abs/2310.10631), [Epoch GPT-series analysis](https://epoch.ai/data-insights/gpt-capabilities-progress), and [Epoch MATH Level 5 methodology](https://epoch.ai/benchmarks/math-level-5).

## Accepted frontier-eligible results

**None in this iteration.**

The original-paper GPT-2 point is a valid historical candidate, but one point
cannot reconstruct a frontier trajectory. Minerva's result is not accepted
into the same frontier because its four-shot, multi-sample majority-vote setup
changes the measurement procedure. The later Epoch-listed results lack the
row-level first-public date and protocol evidence needed to bridge the gap.

## Why the prior T50/T90 values were invalid

The previous snapshot used the Epoch evaluation-run date for the 108
retrospective rows. Many runs shared the same run date, so a large score jump
was represented as one late frontier event. Both T50 and T90 consequently
became 46.8 months. That number described the collapsed evaluation timeline,
not the time from benchmark release to publicly observed historical events.

The corrected snapshot still exposes the standardized scores and the
retrospective marker layer. It does not allow them to rewrite the historical
frontier.

## Other four pilot benchmarks

The same concern affects the current lifecycle metrics, although this audit
does not silently rewrite their metric outputs:

| Benchmark | Current source pattern | Current date used by snapshot | Historical lifecycle status |
|---|---|---|---|
| MMLU | Mostly Stanford HELM/aggregator links | Model `Release date`; no evaluation/public-result date in export | Not demonstrated to be first-public historical timeline |
| GSM8K | Mostly Stanford HELM/aggregator links | Model `Release date`; no evaluation/public-result date in export | Not demonstrated to be first-public historical timeline |
| GPQA Diamond | Epoch evaluation logs | `Started at` where present | Retrospective/operational timeline; not demonstrated historical |
| SWE-bench Verified | Epoch evaluation logs | `Started at` where present | Retrospective/operational timeline; not demonstrated historical |

This means their current T50/T90 values should be treated as provisional
operational-order statistics, not publication-timeline lifetimes. A later
follow-up should either recover defensible public-result dates and protocol
groups for each benchmark or mark those lifecycle metrics `Unknown`, just as
MATH Level 5 now is.

## Is MATH Level 5 still a good fit?

Yes, as a curated benchmark record and as a paired view of:

1. retrospective standardized capability by model generation; and
2. a future historical public-result frontier, if protocol-grouped evidence
   can be recovered.

It is not currently a good source of a single precise lifetime number. The
benchmark should remain in the core set because the distinction between its
original public evaluations and later standardized re-runs is itself a useful
benchmark-lifecycle finding.

## Next evidence needed

- original paper/report links for each proposed historical score;
- first-public dates for the actual reported results;
- exact subset/version confirmation;
- prompt, sampling, answer extraction, and scorer details;
- explicit protocol grouping before any frontier merge.
