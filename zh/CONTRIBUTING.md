# 为 BLE 做贡献

BLE 是刻意有所取舍的。它只跟踪一小组经典、被广泛关注的 benchmark，目标是用相对少的信息展示 frontier 的进展，而不是追求全面覆盖。一个新的、小众的或评测稀少的 benchmark 也许有价值，但在具备下面的证据之前，它应进入 curation queue。

贡献之前，请阅读 [`AGENT.md`](AGENT.md)、[Benchmark Integration Contract](docs/BENCHMARK_INTEGRATION.md) 和 [数据 Provenance 与许可政策](docs/DATA_PROVENANCE_POLICY.md)。

## 收录标准（初始政策）

以下阈值是初始政策，在应用到现有 registry 之后会再作修订。一个 benchmark/版本只有在**全部**满足以下条件时，才能上站：

1. **固定的任务集和明确的分数。** 该 benchmark 有一个固定、带版本的任务集，以及一个有充分理由的 canonical score，并声明了方向和单位。滚动更新或可变的任务集需要先有一个显式的带版本快照。
2. **被广泛关注。** 至少满足以下一项：
   - 在提议之前的 18 个月内，该 benchmark 的结果出现在来自 `data/organizations.json` 所列**至少两家**不同 reference organization（目前为 OpenAI、Anthropic、Google、DeepSeek、Qwen、Meta 和 xAI）的模型官方发布材料中（model card、system card、技术报告或发布文章）；或
   - 该 benchmark 被一个跨实验室运行或汇编结果的主要独立 leaderboard 追踪（例如 Epoch AI Benchmarking Hub 或 Stanford HELM）。
3. **有当前 frontier 结果。** 对于提议之前 12 个月内发布的模型，至少有**三条**带来源链接的 canonical observation，且来自至少**两家**不同的 reference organization。
4. **可追溯的 provenance。** 按照 provenance 政策的要求，每条 observation 都引用其原始论文、leaderboard、评测日志或厂商发布。benchmark-radar 这类发现工具永远不是来源。

缺少这些证据的 benchmark 进入 [`CURATION_QUEUE.md`](CURATION_QUEUE.md)，而不是上站。请记录缺少的是哪一条标准，以便日后重新核查。

这些标准适用于新增内容。已在 registry 中的 benchmark 会另行对照这些标准审查。本政策本身不会移除任何现有卡片。

## 如何贡献

- **为现有 benchmark 新增 observation：** 在该 benchmark 的 `data/raw/*.csv` 文件中加一行，数值从原始来源读取，并附上来源链接和日期。如果你是通过发现工具找到该结果的，可以在 `discovered_via` 列中注明；该列只用于致谢。
- **新增 benchmark：** 在 `data/benchmarks/<benchmark-id>.json` 下添加一条满足 Benchmark Integration Contract 的完整类型化记录，并附上其 raw observation 文件。
- **更正：** 保留相互冲突的 observation，并把更正记录为 validity/provenance 事件；绝不无声地覆盖。
- **文档：** 英文为 canonical。在同一次改动中更新 `zh/` 下的中文镜像。

提交之前，运行 [README](README.md) 中列出的完整 integration gate。

## 贡献内容的许可

贡献即表示你同意：你贡献的代码采用 MIT License（[`LICENSE`](../LICENSE)），你贡献的数据和文字采用 CC BY-SA 4.0（[`LICENSE-DATA`](../LICENSE-DATA)）。你添加的第三方结果保留其原有条款；请引用它们，并且不要批量导入条款禁止批量导入的数据集。
