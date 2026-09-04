# Frontier Model Release-Resource Audit

This audit records the seven current frontier reference-panel anchors. It is intentionally a release-resource audit, not an exhaustive model catalog. A model can have a release resource without having a score on every benchmark.

| Model | Organization | Release date | Canonical release/model resource |
|---|---|---:|---|
| Claude Fable 5.1 | Anthropic | 2026-09-01 | [Official release page](https://www.anthropic.com/claude/fable) |
| GPT-6 Astra | OpenAI | 2026-09-03 | [Official model page](https://developers.openai.com/api/docs/models/gpt-6-astra) |
| Gemini 3.8 Flash | Google DeepMind | 2026-09-02 | [Official model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/) |
| DeepSeek-V4-Pro-0813 | DeepSeek | 2026-08-13 | [Official release announcement](https://api-docs.deepseek.com/news/news260813/) |
| Qwen3.8-Max | Alibaba | 2026-08-03 | [Official model documentation](https://docs.modelstudio.console.alibabacloud.com/en/model-studio/qwen3-8-max) |
| Llama 4 Maverick | Meta | 2025-04-05 | [Official model resources](https://ai.meta.com/llama/get-started/) |
| Grok 4.6 | xAI | 2026-08-12 | [Official release announcement](https://x.ai/news/grok-4-6) |

The generated snapshot is checked to ensure every listed model exists and points to its canonical release resource. Benchmark-specific systems such as GLM-5.3 + Claude Code remain represented by their score evidence; they are not silently promoted into this seven-organization reference panel.

The same audit also checks that every benchmark detail record contains bilingual summary/task/scoring metadata. This prevents newly added benchmark rows from appearing in the leaderboard without a usable detail page.
