# Adversarial Score-Semantics Audit

Snapshot: `2026-09-04`  
Benchmarks: 89

## Gate result

- Ratio observations outside `[0, 1]`: **0**
- Ratio observations below `1%`: **114**
- Observations below a normalization/reference floor: **21**
- Unbounded numeric observations above `100`: **79**

`progress_baseline` is treated as a chance/reference baseline for normalized progress, not as a hard observation bound. Accordingly, a model may score below the floor without the canonical observation being invalid.

Values above 100 are accepted only for `score_format: number`; examples include minutes, Elo, and simulated business outcomes. They are never formatted or normalized as percentages unless explicit finite bounds exist.

## Low ratio observations (<1%)

- gsm8k / babbage (1.3B) / 0.007
- gsm8k / ada (350M) / 0.006
- gsm8k / text-curie-001 / 0.006
- gsm8k / Cohere small v20220720 (410M) / 0.004
- gsm8k / text-ada-001 / 0.004
- gsm8k / text-babbage-001 / 0
- gsm8k / T0pp (11B) / 0
- gsm8k / YaLM (100B) / 0
- browsecomp / GPT-4o (no browsing) / 0.006
- browsecomp / GPT-4.5 / 0.009
- frontiermath-tiers-1-3-v2 / gpt-3.5-turbo-0125 / 0
- frontiermath-tiers-1-3-v2 / gpt-4o-mini-2024-07-18 / 0.00701754
- frontiermath-tiers-1-3-v2 / gpt-4-turbo-2024-04-09 / 0.00701754
- frontiermath-tiers-1-3-v2 / gpt-4o-2024-08-06 / 0.00350877
- arc-agi-2 / Claude 3.7 (8K) / 0.009
- arc-agi-2 / GPT-5 Nano (Medium) / 0.0088
- arc-agi-2 / Claude Sonnet 4 (Thinking 1K) / 0.0085
- arc-agi-2 / Gemini 3.5 Flash-Lite (Minimal) / 0.00833333
- arc-agi-2 / DeepSeek V4 Pro 0813 (None) / 0.00833333
- arc-agi-2 / o1-mini / 0.0083
- arc-agi-2 / GPT-5.2 / 0.0083
- arc-agi-2 / GPT-5 Mini (Low) / 0.0083
- arc-agi-2 / GPT-4.5 / 0.008
- arc-agi-2 / Gemini 1.5 Pro / 0.008
- arc-agi-2 / Claude 3.7 (16K) / 0.007
- arc-agi-2 / GPT-4.1 / 0.0042
- arc-agi-2 / Grok 3 Mini (Low) / 0.0042
- arc-agi-2 / GPT-5.1 (Thinking, None) / 0.0042
- arc-agi-2 / Claude 3.7 (1K) / 0.004
- arc-agi-2 / Claude 3.7 / 0
- arc-agi-2 / GPT-4o-mini / 0
- arc-agi-2 / GPT-4.1-Nano / 0
- arc-agi-2 / Llama 4 Scout / 0
- arc-agi-2 / Llama 4 Maverick / 0
- arc-agi-2 / o3-mini (Low) / 0
- arc-agi-2 / GPT-4.1-Mini / 0
- arc-agi-2 / Grok 3 / 0
- arc-agi-2 / Claude Opus 4 (Thinking 1K) / 0
- arc-agi-2 / Magistral Small / 0
- arc-agi-2 / Magistral Medium / 0
- arc-agi-2 / Gemini 2.5 Pro (Thinking 1K) / 0
- arc-agi-2 / GPT-5 (Minimal) / 0
- arc-agi-2 / GPT-5 Nano (Low) / 0
- arc-agi-2 / GPT-4o / 0
- arc-agi-2 / GPT-5 Nano (Minimal) / 0
- arc-agi-2 / Magistral Medium (Thinking) / 0
- arc-agi-2 / Inkling Small (None) / 0
- critpt / Trinity Large Thinking / 0.00857143
- critpt / Qwen3.6 27B (Non-reasoning) / 0.00857143
- critpt / Qwen3.5 122B A10B (Non-reasoning) / 0.00857143
- critpt / Mercury 2 / 0.0084898
- critpt / o4-mini (high) / 0.006
- critpt / MiniMax-M2.7 / 0.00571429
- critpt / Qwen3.5 35B A3B (Non-reasoning) / 0.00571429
- critpt / Claude Opus 4 / 0.003
- critpt / Qwen3.5 9B (Reasoning) / 0.00285714
- critpt / Qwen3.6 35B A3B (Reasoning) / 0.00285714
- critpt / Claude 4 Sonnet (Reasoning) / 0.00285714
- critpt / Qwen3 32B (Reasoning) / 0.00285714
- critpt / Magistral Medium 1.2 / 0.00285714
- …and 54 more canonical low-score observations.

## Large unbounded numeric observations (>100)

- vending-bench-2 / Claude Opus 5 / 11181.9
- vending-bench-2 / Claude Opus 4.7 / 10936.8
- vending-bench-2 / GPT-5.6 Sol / 9619.37
- vending-bench-2 / Grok 4.6 / 9047.03
- vending-bench-2 / GLM-5.2 / 8313.78
- vending-bench-2 / GLM-5.3 / 8163.61
- vending-bench-2 / Claude Opus 4.6 / 8017.59
- vending-bench-2 / GPT-5.5 / 7523.84
- vending-bench-2 / GPT-5.6 Terra / 7343.21
- vending-bench-2 / Claude Sonnet 4.6 / 7204.14
- vending-bench-2 / Muse Spark 1.1 / 6520.47
- vending-bench-2 / Claude Sonnet 5 / 6377.7
- vending-bench-2 / Kimi K2.6 / 6204.57
- vending-bench-2 / GPT-5.4 / 6144.18
- vending-bench-2 / GPT-5.3-Codex / 5940.12
- vending-bench-2 / Claude Opus 4.8 - High / 5787.43
- vending-bench-2 / Claude Fable 5 - High / 5680.26
- vending-bench-2 / GLM-5.1 / 5634.41
- vending-bench-2 / Gemini 3 Pro / 5478.16
- vending-bench-2 / Gemini 3.5 Flash / 5396.42
- vending-bench-2 / Kimi K3 (Moonshot) / 5165.04
- vending-bench-2 / Qwen 3.6 Plus / 5114.87
- vending-bench-2 / Kimi K2.7 Code / 5082.94
- vending-bench-2 / Claude Fable 5 - Low / 5018.52
- vending-bench-2 / Claude Opus 4.5 / 4967.06
- vending-bench-2 / Claude Fable 5 - Max / 4966.64
- vending-bench-2 / Grok 4.20 / 4662.85
- vending-bench-2 / Claude Fable 5 - None / 4529.94
- vending-bench-2 / GLM-5 / 4432.12
- vending-bench-2 / Claude Fable 5 - Medium / 4339.81
- …and 49 more numeric observations.

## Interpretation

The low ratios are retained because their source metrics genuinely permit zero or near-zero performance. The large numeric values are retained because their metrics are not percentages. Every observation now preserves its raw input score and explicit input unit, and the validator checks the raw-to-canonical conversion.
