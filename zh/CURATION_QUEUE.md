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

## 2026 年 10 月候选

以下为初步发现记录；新增卡片前需对照论文重新核对所有数字。

- **Doc2Harness**（[arXiv 2610.20344](https://arxiv.org/abs/2610.20344)，2026-10-14）—— 328 个测试用例，三次构建取平均，覆盖 5/7 参考组织。未说明 reasoning effort，也没有模型发布日期；纳入前需先固定 builder 配置。
- **SCI-AGENT-EXAM**（[arXiv 2610.32441](https://arxiv.org/abs/2610.32441)，2026-10-23）—— 120 个任务，覆盖 5/7。最终分数部分依赖 LLM 评审，且所有模型都在 Claude Code 中运行；需先审查评审模型和 harness 的中立性。
- **E2E-SWE**（[arXiv 2609.38335](https://arxiv.org/abs/2609.38335)，2026-09-29）—— 186 个任务，四次运行的 Pass@1，覆盖 4/7；各行 effort 不同。纳入前需先确定 canonical effort 规则。

## 现有卡片后续事项 —— 2026-10-27

- **BrowseComp 厂商自报序列** —— 这张卡的主序列目前仍只有 OpenAI 原始论文的结果。已有 90% 及以上的厂商自报成绩（例如 [GPT-6 Astra 页面](https://openai.com/index/gpt-6-astra/)的文字表格：GPT-6 Astra 91.5%、GPT-5.6 Sol 90.4%、Claude Opus 5 90.8%），按这些成绩算，90% 门槛会在 2026 年 7 月被跨过。在从各厂商原始发布页加入一条经过审核、逐行标明 harness 和 fallback 设置的厂商自报序列之前，Kimi K3.1 Pro 的 92.1% 保持为辅助序列。
