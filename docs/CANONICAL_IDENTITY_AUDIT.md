# Canonical Identity Audit

Snapshot: `2026-09-05` · schema version `2`

A source row is preserved as evidence. Exact duplicate measurements may share one canonical observation; model/display setting, protocol, task set, score series, and score must all match.

- Source evidence records: **4231**
- Canonical measurements: **4090**
- Measurements with multiple evidence records: **119**
- Duplicate evidence rows reconciled: **141**
- Canonical models: **1192**
- Canonical resources: **892**

## Reconciliation by benchmark

| Benchmark | Evidence | Measurements | Merged rows |
|---|---:|---:|---:|
| ARC-AGI-2 | 221 | 210 | 11 |
| BIG-Bench Hard | 92 | 79 | 13 |
| BoolQ | 206 | 186 | 20 |
| GSM8K | 235 | 215 | 20 |
| HellaSwag | 135 | 129 | 6 |
| MMLU | 249 | 237 | 12 |
| OpenBookQA | 71 | 69 | 2 |
| PIQA | 140 | 116 | 24 |
| SciCode | 162 | 159 | 3 |
| Terminal-Bench 2.0 | 204 | 183 | 21 |
| TriviaQA | 115 | 106 | 9 |
