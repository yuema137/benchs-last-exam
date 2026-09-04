# GPT-6 Astra Public Benchmark Audit

Source checked: [GPT-6 Astra release page](https://openai.com/index/gpt-6-astra/), 2026-09-03.

The page reports public results for benchmark objects that are already in the curated set, plus two clearly versioned public additions in this update:

| Benchmark | Result added | Protocol note |
|---|---:|---|
| Agents' Last Exam | 59.3% | Computer-use evaluation |
| AutomationBench | 41.4% | Public task pass rate |
| ARC-AGI-3 | 99.9% | Responses API harness; interactive agent benchmark |
| FrontierMath Tier 4 (v2) | 97.6% | Separate v2 Tier 4 object; verified accuracy |
| GPQA Diamond | 96.0% | Accuracy |
| Humanity's Last Exam | 57.2% | With tools |
| ScreenSpot-Pro | 92.7% | No tools; direct grounding |
| Terminal-Bench-Science 0.1 | 64.6% | Fixed 0.1 snapshot |
| Terminal-Bench 4.0 | 57.9% | Version 4.0 |

The page also reports OSWorld 2.0 as a **partial score** (72.6%), not the binary accuracy metric used by the current OSWorld card. It is therefore not silently merged into that card's headline series. FrontierCode 1.1 Extended is also distinct from the current Main score series and requires a separate protocol/version record before import.

The following public benchmark names appear on the page but are not yet added as cards because this repository does not currently have a sufficiently curated benchmark-version/resource record for them: BenchCAD, BrowseComp, OpenScore String Quartets, DeepSWE, GeneBench Pro, LifeSciBench, HealthBench Professional, ExploitBench, ExploitGym, SRE-Bench, and SEC-Bench Pro. They are not internal benchmarks, but adding a score without the benchmark's own canonical version, release date, and scoring semantics would create false lifecycle data. They remain a focused curation queue rather than being silently represented by an OpenAI-only result.

Internal Design Tasks, Data Science Tasks, Database Migration Tasks, MedChemBench, internal cybersecurity evaluations, internal alignment evaluations, and other explicitly marked internal evaluations are excluded.

All imported GPT-6 Astra observations use the official release page as their score resource and the model release date (`2026-09-03`) for the capability timeline. The result-publication date remains provenance metadata.
