# Curation Audit：策展审计

状态：初始 curated core 提案，2026-09-03

## 策展原则

Benchmark Observatory 是 curated，而不是 comprehensive。core set 只收录重要、可解释、具有历史意义、当前仍相关，并且有助于重建纵向 frontier 的 benchmark。不追求收集所有 benchmark、model 或 score。

## Tier A：核心 benchmark

| Benchmark | 纳入理由 | Metric 与 bounds | 当前纵向证据 | Lifecycle 作用 | 信心 |
|---|---|---|---|---|---|
| MMLU original fixed version | canonical 的 broad knowledge reference，可观察长期 saturation 与 version pressure | accuracy；四选一 random floor 0.25；ceiling 1.0 | Epoch 选定导出中有 215 条可用 dated rows | 历史重要、可能已饱和 | High |
| GSM8K original fixed version | canonical 的多步小学数学 benchmark，exact-answer scoring 清晰 | exact-match accuracy；floor 0.0；ceiling 1.0 | 选定导出中有 162 条可用 dated rows | 快速解决、数学历史轨迹 | High |
| MATH Level 5 | competition math 难题集，可和 GSM8K 形成有意义对照 | accuracy；floor 0.0；ceiling 1.0 | Epoch internal export 提供较集中的 dated trajectory | 数学 benchmark 的快速解决或饱和 | High |
| GPQA Diamond | 重要的 expert-level science reasoning benchmark，困难起点和后续结果都适合生命周期分析 | accuracy；四选一 floor 0.25；ceiling 1.0，带 data-quality caveats | 选定导出中有 311 条 dated internal-run rows | 当前困难、frontier 变化快 | High |
| SWE-bench Verified | 重要的 coding-agent benchmark，有独特 evaluation burden 和 human-validated fixed subset | issue-resolution rate；floor 0.0；ceiling 1.0；必须保留 protocol/scaffold | 选定导出中有 35 条，明显比 QA benchmark 稀疏 | coding/agent 轨迹 | Medium-high |

来源包括各 benchmark 的 original paper、official project，以及 Epoch AI export。Epoch 在第一版中作为 trusted aggregator，不取代 primary metadata。

五个对象已经覆盖 broad knowledge、两种 math regime、expert science reasoning 和 repository-level coding agents。HumanEval 暂不进入首批 core，因为当前选定 source export 没有可比较的历史文件。

## Reference Model Panel

第一版 panel 保持小规模、带时间范围，并把 model 当作 probe 而不是 model catalog。只有当模型能补充时间、vendor、开放性或领域 coverage 时才加入。

| 代表 family/generation | Organization | Role | 相关领域 | 纳入理由 |
|---|---|---|---|---|
| GPT-4 → GPT-4o → o1-era representative | OpenAI | historical anchor + contemporary frontier | general、math、science、coding/agents | 代表主要 capability generations |
| Claude 3.5/3.7 Sonnet → current Sonnet/Opus representative | Anthropic | historical anchor + contemporary frontier | general、math、science、coding/agents | 独立 frontier probe，coding relevance 强 |
| Gemini 1.5/2.x representative | Google | historical anchor + contemporary frontier | general、math、science、multimodal | 独立 vendor coverage |
| Llama 3.x representative | Meta | historical anchor + open-weight frontier | general、math、coding | 重要 open-weight family |
| DeepSeek-V3 / reasoning-era representative | DeepSeek | open-weight frontier | math、science、coding | 增加组织和 open-weight diversity |
| Qwen 2.5 representative | Alibaba | open-weight frontier | math、coding、multilingual/general | 增加 open-weight 与组织多样性 |
| 一个有 documented protocol 的 coding-agent specialist | varies | domain specialist | coding/agents | 只有明显增加信息时才加入 |

具体 model version 和日期仍需从 official model card/technical report 核验，不能从产品名或 leaderboard 猜测。

## 解释规则

高 frontier score 不代表 current coverage 足够。相反，如果多个独立的 contemporary family 都得分较低，才更有底气说 benchmark 仍然困难。Coverage 是 evidence strength，不是 benchmark health。
