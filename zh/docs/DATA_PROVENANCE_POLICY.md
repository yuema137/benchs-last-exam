# 数据 Provenance 与许可政策

本政策规定 BLE 的数字可以来自哪里、第三方材料如何复用，以及仓库的哪一部分适用哪一种许可。它是对 [`PROVENANCE.md`](PROVENANCE.md) 中 resource 与 lineage 模型的补充。

本文件记录 BLE 在一手来源中找到的条款，以及 BLE 对这些条款的理解。它不构成法律意见。

## 1. 本仓库的许可

| 材料 | 许可 |
| --- | --- |
| 代码：站点（`site/*.html`、`site/*.js`、`site/*.css`）、脚本、流水线（`scripts/`、`src/`）、测试 | MIT，见 [`LICENSE`](../../LICENSE) |
| BLE 自己的数据和文字：BLE 计算出的分数、排名、frontier、lifecycle metric 与分类；`data/benchmarks/` 中的 benchmark 卡片；文档 | CC BY-SA 4.0，见 [`LICENSE-DATA`](../../LICENSE-DATA) |
| 第三方结果和材料：`data/raw/` 中的源数据行、`data/evidence.jsonl` 中的 `raw_fields`，以及所链接的论文、leaderboard、日志和厂商发布 | 各自原有条款；见 [`NOTICE`](../../NOTICE) 和第 5 节 |

MIT 与 CC BY-SA 4.0 部分的版权：2026 Yue Ma。

第三方数字不会因为 BLE 重新发布或转换了它，就变成 CC BY-SA 4.0。CC BY-SA 4.0 只适用于 BLE 自己的贡献：选择、归一化、派生 metric、分类和文字。

## 2. 每条 observation 都引用其原始来源

- 每条 canonical observation 的 `source_ids` 中，至少要有一项指向该数字的原始来源：benchmark 论文、官方 benchmark leaderboard、厂商的 model card、system card 或发布文章，或者评测方自己的运行记录（例如 Epoch AI 亲自运行的评测所对应的 Epoch AI 评测日志）。
- 数字从该原始来源读取。绝不在没有重新阅读原始来源的情况下，从发现工具或二手汇编中复制数值。
- 汇编方在能补充信息时（例如日志、运行日期），可以作为原始来源之外的附加引用；对新的 observation，它永远不能代替原始来源。
- [`AGENT.md`](../AGENT.md) 中已有的证据规则仍然适用：核实标题、日期、URL、metric 和设置；绝不臆造数值；保留相互冲突的 observation。

## 3. benchmark-radar 只作为发现来源

由 Koutian Wu 开发的 [benchmark-radar](https://github.com/ktwu01/benchmark-radar)（<https://benchmark-radar.org/>）追踪 AI benchmark 与评测结果在哪里被报告。BLE 可以用它来*寻找*候选来源。它不得被引用为任何数字的来源，也不得把任何 benchmark-radar 内容（数值、描述、注意事项、整理过的列表、身份链接或简报）复制进 BLE 或再分发。

- BLE 数据中唯一可以出现 benchmark-radar 名称的位置，是一个显式的发现来源字段 `discovered_via`（raw CSV 中名为 `discovered_via` 或 `Discovered via` 的列，或 JSON 记录中的 `discovered_via` 键）。该字段只用于致谢，永远不参与 lineage、资格判断、日期或分数。
- `scripts/validate_provenance.py` 强制执行这一规则。以下情况会导致校验失败：
  1. 某条 observation 引用的来源全部是 benchmark-radar resource（任何位于 `benchmark-radar.org`、`github.com/ktwu01/benchmark-radar`、`ktwu01.github.io/benchmark-radar` 或 `huggingface.co/datasets/ktwu01/benchmark-radar` 的 URL）；或
  2. benchmark-radar 在 `discovered_via` 字段以外的任何地方被提及或链接，无论是在生成的 snapshot、`data/raw/*.csv` 还是 `data/benchmarks/*.json` 中。与原始来源一起被引用的 benchmark-radar resource 也算在内。
- 对应测试为 `tests/test_provenance_policy.py`。

对它的致谢见 README、站点和 `NOTICE`。

## 4. 不违反来源条款进行批量导入

- 不要批量导入或重新打包任何条款禁止再分发、数据集打包、商业使用或衍生作品的第三方整理数据集，也不要导入条款未知的此类数据集。benchmark-radar 的内容属于这一类。
- 只有当某个批量来源的条款允许署名后再分发（例如 CC BY 4.0）时才可以使用。导入之前，先在第 5 节和 `NOTICE` 中记录该来源及其条款。
- 新 observation 的常规途径，是从原始论文、leaderboard 或厂商发布中逐条读取事实，并在那里引用。

## 5. 第三方条款登记

检索日期 2026-10-27。引文逐字摘自所链接页面（保留英文原文）。

### Epoch AI Benchmarking Hub（最大的批量来源）

来源：<https://epoch.ai/benchmarks/use-this-data>（"Licensing" 一节）、<https://epoch.ai/benchmarks/about>（"How is the data licensed?"）、<https://epoch.ai/data/ai-benchmarking-dashboard>。

> "Epoch AI's data is free to use, distribute, and reproduce provided the
> source and authors are credited under the Creative Commons Attribution
> license. [...] Benchmark questions and answers are the property of their
> respective creators. This hub also includes data sourced from external
> projects, which retains its original licensing. Users are responsible for
> complying with the license terms of the specific data they use, and should
> credit the original sources as indicated."

两个页面上的 "Creative Commons Attribution license" 链接都指向 <https://creativecommons.org/licenses/by/4.0/>。同一页面给出的建议引用格式："Epoch AI, 'Capabilities & benchmarking'. Published online at epoch.ai. Retrieved from 'https://epoch.ai/benchmarks/use-this-data' [online resource]."

允许的范围：在署名的前提下使用、再分发和改编，包括商业使用（CC BY 4.0）。没有相同方式共享要求，也没有非商业限制。

BLE 的使用情况：933 个 resource 中有 623 个是 Epoch AI 评测日志，4,813 条 canonical observation 中有 690 条引用了 Epoch AI resource。许多 `data/raw/*.csv` 文件采用该 hub 的导出格式（internal runs 与 external runs）。

与 CC BY-SA 4.0 的兼容性：对 Epoch AI 自己的数据而言是兼容的。CC BY 4.0 第 3(a)(4) 条只要求 "the Adapter's License You apply must not prevent recipients of the Adapted Material from complying with this Public License"（<https://creativecommons.org/licenses/by/4.0/legalcode>），而 CC BY-SA 4.0 并不妨碍这一点。BLE 必须遵守的条件：为 Epoch AI 署名、链接许可、注明 BLE 修改了数据，并让逐字保留的 Epoch 数据行继续适用 CC BY 4.0，而不是重新贴上别的许可。hub 中 external runs 的数据行则不同：Epoch 说明它们保留原有许可（见第 6 节）。

### 被批量使用的官方 leaderboard 与 benchmark 仓库

各仓库的许可字段取自 2026-10-27 的 GitHub API 返回结果：

| 来源 | BLE 的使用 | 所述条款 |
| --- | --- | --- |
| Stanford HELM / CRFM leaderboard（<https://crfm.stanford.edu/helm/>） | 248 条 evidence 行引用 "Stanford HELM" 或 "Stanford CRFM Leaderboard" | 框架仓库 <https://github.com/stanford-crfm/helm> 为 Apache-2.0。BLE 没有找到针对已发布 leaderboard 结果的单独许可声明。 |
| Aider leaderboard（<https://aider.chat/docs/leaderboards/>） | 61 条 evidence 行 | Leaderboard 数据存放在 <https://github.com/Aider-AI/aider>（Apache-2.0）中。 |
| Terminal-Bench leaderboard（<https://www.tbench.ai/>） | 105 条 evidence 行 | <https://github.com/harbor-framework/terminal-bench> 为 Apache-2.0。 |
| ScienceQA leaderboard | 81 条 evidence 行 | <https://github.com/lupantech/ScienceQA> 为 MIT。 |
| Video-MME leaderboard | 49 条 evidence 行 | 未检测到 <https://github.com/MME-Benchmarks/Video-MME> 的许可。 |
| Artificial Analysis（<https://artificialanalysis.ai/>） | SciCode（198 条 evidence 行，195 条 observation）与 GDPval-AA v2（35 条 observation）引用 Artificial Analysis 页面 | 网站 Terms of Use v1.0，最后修订于 2024 年 4 月 28 日（<https://artificialanalysis.ai/docs/legal/Terms-of-Use.pdf>）：许可 "solely for your own personal, noncommercial use"；"you shall not license, sell, rent, lease, transfer, assign, distribute, host, or otherwise commercially exploit the Site, whether in whole or in part, or any content displayed on the Site"；"no part of the Site may be copied, reproduced, distributed, republished, downloaded, displayed, posted or transmitted in any form or by any means"。 |

### benchmark-radar

来源：<https://github.com/ktwu01/benchmark-radar>（`LICENSE`：MIT），以及同一仓库中的 `LICENSE-CONTENT.md`：

> "Software: MIT License. Technical report and original editorial content:
> CC BY-NC-SA 4.0. Commercial republication, resale, paid newsletters, dataset
> packaging, or commercial product integration requires prior written
> permission from Koutian Wu. Adaptations must be shared under the same terms.
> Third-party source material remains under its original terms."

BLE 的使用情况：仅用于发现（第 3 节）。由于没有复制任何内容，benchmark-radar 的条款不附着于 BLE 的数据。CC BY-NC-SA 内容无法纳入允许商业使用的 CC BY-SA 4.0 之下，这也是不复制规则的另一个理由。

## 6. 未决的许可事项

以下事项尚未解决。它们记录在这里，而不是被掩盖。

1. **Artificial Analysis 数据行与 CC BY-SA 4.0 冲突。** Artificial Analysis 的 Terms of Use 只允许个人、非商业使用，并禁止复制、再分发和重新发布。BLE 再分发了 198 条 SciCode 和 8 条 GDPval-AA v2 raw 行，这些行引用 Artificial Analysis 页面；另有 230 条 observation 的派生值。CC BY-SA 4.0 允许商业使用。单个分数是否受保护，与使用条款的合同约束是两个不同的问题。BLE 在此不作结论。在维护者作出决定（改从原始论文或厂商发布取得来源、删除，或取得许可）之前，这些数据行在 `NOTICE` 中被标为适用其原有条款的第三方材料，不在 `LICENSE-DATA` 覆盖范围内。
2. **Epoch AI external runs 数据行保留其原有条款。** Epoch 说明外部数据 "retains its original licensing"。BLE 尚未审查这些数据行背后每一篇论文、每一个 leaderboard 和厂商页面的条款。BLE 目前也没有逐行记录某一行来自 Epoch 导出还是直接读取。增加逐行的 `source_dataset` 字段，可以让适用的条款变得可核查。
3. **HELM 与 Video-MME 的结果没有明确的数据许可。** HELM 框架为 Apache-2.0，但 BLE 没有找到覆盖已发布 leaderboard 结果的声明。Video-MME 仓库未检测到许可。它们的条款是未知，而不是宽松。
4. **混合许可的数据包。** `site/data/*.json` 把 BLE 派生的值（CC BY-SA 4.0）与第三方事实和来源标题（原有条款）合在一起。第 1 节的划分是规则。这些文件本身尚未带有逐字段的许可标记。
