# Curation Queue：候选队列

这些候选可能值得加入，但需要进一步的 source、protocol 或重复性审计。它们暂不属于 Tier A，不能阻塞核心实现。

| Candidate | 可能纳入理由 | Concern / overlap | Recommendation |
|---|---|---|---|
| HumanEval | 经典 coding benchmark，execution-based scoring 清晰 | 当前 source export 缺少可比较历史序列，可能已饱和 | 找到干净历史序列后再加入 |
| Humanity's Last Exam | 重要的 current expert-knowledge benchmark | 历史较短，item quality 与 ceiling 仍需谨慎 | 后续 current-frontier candidate |
| ARC-AGI-1 / ARC-AGI-2 | 独特的 abstract reasoning task | task-set version 与 model coverage 需要分开审计 | 审计后只选一个版本 |
| MMMU | 重要 multimodal knowledge benchmark | item format 导致 floor 和 protocol 更复杂 | 只有提供明显不同的纵向对象时加入 |
| MathVista | multimodal math | 与 MATH/GSM8K 有部分能力重叠，历史可能较薄 | 作为 MMMU 的替代候选 |
| SimpleQA Verified | 重要 factuality 目标 | grader、abstention 和历史长度问题 | 等 grader metadata 稳定后复查 |
| FrontierMath | 有价值的 hard-math frontier probe | private test 与 ceiling 不适合当前 normalized thresholds | 先保留为 non-normalized candidate |
| SWE-bench original vs Verified | 两者都有历史价值 | 相关版本不应自动做成两个 homepage objects | Verified 保持 core，original 放入 version lineage |

Tier C 不维护完整 rejected list：obscure、来源弱、minor variant、历史几乎为空或只增加噪声的 benchmark 暂不纳入。
