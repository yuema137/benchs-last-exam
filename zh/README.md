# Benchmark Observatory

Benchmark Observatory 是一个轻量的 **Leaderboard of Benchmarks**。

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
python3 scripts/validate_benchmark_integration.py
python3 scripts/audit_observation_dates.py
python3 scripts/audit_canonical_identity.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## 文档

- [Design synthesis](docs/design-synthesis.md)
- [Vertical slice plan](docs/vertical-slice-plan.md)
- [Repository constitution](AGENT.md)
- [Benchmark integration contract](docs/BENCHMARK_INTEGRATION.md)
- [Explanation style](EXPLANATION_STYLE.md)
- [Chinese design mirror](zh/docs/design-synthesis.md)
