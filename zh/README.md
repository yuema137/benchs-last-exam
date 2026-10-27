# Benchmark Observatory

Benchmark Observatory 是一个轻量的 **Leaderboard of Benchmarks**。

**BLE 评估的是 benchmark 本身，而不是它们的结果在哪里被报告。**
它沿着区分力、剩余空间与饱和速度、覆盖度与新鲜度、协议可比性、成本以及抗 contamination 能力等维度来考察每个 benchmark。BLE 是刻意有所取舍的：它只收录经典、被广泛关注的 benchmark，目标是用相对少的信息展示 frontier 的进展，而不是全面覆盖。参见[收录标准](CONTRIBUTING.md#收录标准初始政策)。

### 致谢

BLE 感谢 Koutian Wu 开发的 [benchmark-radar](https://github.com/ktwu01/benchmark-radar)，它追踪 AI benchmark 与评测结果在哪里被报告。我们只把它作为发现来源的参考：BLE 中的每一个数字都从原始论文、leaderboard 或厂商发布中重新读取，并在那里引用；没有任何 benchmark-radar 内容被复制或再分发。

两个项目回答的是不同的问题。benchmark-radar 在一个非常大的集合中，帮你找到 benchmark 以及它们的结果出现的地方。BLE 则刻意有所取舍：它只跟踪一小组经典、被广泛关注的 benchmark，并评估 benchmark 本身，维度包括区分力、剩余空间与饱和速度、覆盖度与新鲜度、协议可比性、成本以及抗 contamination 能力，让你能判断一个 benchmark 对 frontier 模型还能告诉你什么。

## 访问网站

**[打开在线的 Benchmark Observatory →](https://yuema137.github.io/ble/)**

网站是面向公众的 frontend。本仓库包含它所用的、经整理的 benchmark 数据、provenance、metric 逻辑和静态站点源码。

传统的 benchmark leaderboard 用 benchmark 来给模型排名。本项目反转了这个视角：一个小而有代表性的 reference model panel 提供历史 observation，用来描述和比较 benchmark 本身。

当前的范围刻意保持很小：

```text
curated source data → Python metric scripts → generated JSON → static frontend
```

同一份静态输出被发布到 GitHub Pages，地址为 [yuema137.github.io/ble](https://yuema137.github.io/ble/)。

本项目目前不打算提供后端、数据库、公开 API、账户、云端接入或穷尽式的模型覆盖。

## 本地开发

本地 frontend 位于 `site/` 下，由生成的 JSON 驱动。Metric 逻辑属于 Python 脚本，而不属于 frontend 组件。

运行时为 leaderboard 和 story 视图加载一个很小的 `site/data/index.json`。完整的 benchmark 档案被拆分到 `site/data/benchmarks/<benchmark-id>.json` 下，只有在打开时才被拉取。

首页筛选把一个互斥的 `domain` 与受控的、多对多的能力 `labels` 区分开来。Label 定义是双语且 canonical 的；选择多个 label 时，要求所有被选中的能力都匹配。

每个活跃的 benchmark/版本都在 `data/benchmarks/<benchmark-id>.json` 中独立维护；其源 observation 存放在所引用的 `data/raw/*.csv` 文件里。类型化的 registry 加载器会自动发现这些记录，构建过程则由它们派生出 leaderboard、详情卡片、frontier、metric 和所有 lifecycle tab。

在改动任何 benchmark 或 observation 之后，运行完整的 integration gate：

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_score_semantics.py
python3 scripts/validate_provenance.py
python3 scripts/validate_benchmark_integration.py
python3 scripts/audit_observation_dates.py
python3 scripts/audit_canonical_identity.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## 许可

- **代码**（站点、脚本、流水线、测试）：[MIT](../LICENSE)。
- **BLE 自己的数据和文字**（BLE 计算出的分数、排名、frontier、lifecycle metric 与分类；benchmark 卡片；文档）：[CC BY-SA 4.0](../LICENSE-DATA)。
- **第三方结果和材料**（`data/raw/` 中的源数据行，以及所链接的论文、leaderboard、评测日志和厂商发布）保留其原有条款。Epoch AI 数据及其他批量来源的署名见 [`NOTICE`](../NOTICE)。

版权 2026 Yue Ma。BLE 找到的第三方条款以及未决的许可事项，见 [数据 Provenance 与许可政策](docs/DATA_PROVENANCE_POLICY.md)。引用 BLE 时请使用 [`CITATION.cff`](../CITATION.cff)。

## 文档

- [Design synthesis](docs/design-synthesis.md)
- [Vertical slice plan](docs/vertical-slice-plan.md)
- [Repository constitution](AGENT.md)
- [Benchmark integration contract](docs/BENCHMARK_INTEGRATION.md)
- [数据 Provenance 与许可政策](docs/DATA_PROVENANCE_POLICY.md)
- [贡献指南与收录标准](CONTRIBUTING.md)
- [Explanation style](EXPLANATION_STYLE.md)
- [Chinese design mirror](zh/docs/design-synthesis.md)
