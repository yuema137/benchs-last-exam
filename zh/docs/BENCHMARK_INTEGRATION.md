# Benchmark 接入契约

新增一个 benchmark 是一次端到端的仓库事务，而不是简单地改一个数据文件。

canonical 的活跃 benchmark registry 是下面这一组带类型的记录：

```text
data/benchmarks/<benchmark-id>.json
```

每个活跃的 benchmark/version 恰好对应一条源记录。文件名必须与 benchmark ID 一致。`src/benchmark_observatory/registry.py` 会在任何 snapshot 计算开始之前校验每一条记录；`scripts/build_snapshot.py` 只做计算，不得包含 benchmark/card 的声明。不存在另外一份手写的 leaderboard 或 lifecycle-tab 收录清单。

`registry_order` 是一个唯一且连续的整数，用来保证确定性的 ingestion 和 tie-breaking。新记录使用下一个整数。它不控制 story-tab 的归属，也不控制 leaderboard 的排序。

一次完整的新增需要提供：

1. canonical 身份、version、release date、Evaluation Type、互斥的 Domain，以及经审核的 capability labels；
2. 简洁的中英文 summary、task format、scoring 说明和 evaluation target；
3. benchmark 资源和带源链接的 canonical observations；
4. 可解析的模型、日期、协议，以及 capability-frontier 的谱系；
5. 派生的 lifecycle metrics、coverage 和 cost（证据不足时用 `Unknown`、`N/A` 或 `—`）；
6. 生成的 leaderboard/detail 数据，以及自动的 lifecycle-tab 资格。

Lifecycle 同步是一条 build invariant。每次 build 都会从同一份 canonical benchmark metrics 重新生成全部四个 story view（`test-of-time`、`still-frontier`、`fastest-solved` 和 `recently-saturated`）的成员 ID。前端消费这些生成的 ID；它不得保留另一份可能过期的手动清单或选择器。新增或更新一个 benchmark，只有在四个生成的 view 及其空/非空状态一起校验通过后，才算完成。

选择器语义和可见卡片语义也必须一致。`Still Frontier` 表示 T50 被右删失（right-censored），normalized progress 低于 50%，且证据充分。因此它的卡片以 normalized progress 为主。当 benchmark 有非零的 chance/reference baseline 时，一个高于 50% 的 raw score 仍可能对应低于 50% 的 normalized progress；raw score 可以作为单独标注的辅助数值展示，但绝不能当作支撑“低于 50%”这一结论的那个数值。

## Canonical 与 auxiliary 分数契约

每个活跃的 benchmark/version 恰好有一条 `canonical_score` 记录。它固定了 metric、task set、evaluation protocol、direction、score 格式/单位，以及 progress 的 baseline/target。canonical observations 带有匹配的 `score_series_id` 和 `score_role: canonical`。所有跨 benchmark 的 metrics 和 view 只消费这一条 series。

任何额外的分数都归入 `auxiliary_score_series`，即使它与该 benchmark 家族同名。典型的例子有：不同的 task subset、pass@k 设置、voting/scaffolding 协议、替代的 judge、次级 metric，或未经核实的 leaderboard task set。auxiliary observations 仍然是 canonical 的溯源记录，但每条 series 必须：

- 声明 `role: auxiliary` 和 `lifecycle_eligible: false`；
- 标明自己的 metric、协议和 task set；
- 用中英文说明它与 canonical score 的差异原因；
- 保留 observation ID 和源谱系；
- 仅在 detail page 上以独立的图例/配色渲染；
- 排除在 canonical frontier、leaderboard 排序、T50/T80/T90、headroom、velocity 以及所有 lifecycle 选择器之外。

生成的 snapshot、接入 validator、前端防御性选择器和回归测试都会强制这条边界。即使某个 benchmark 没有 auxiliary 数据，也要输出一个空的 `auxiliary_score_series` 列表，让契约保持显式。

## 证据与 canonical 测量身份

一条导入的源数据行是一条不可变的证据记录，并不自动成为一次新的科学测量。Evidence ID 在存在源行 ID 时基于该 ID，否则基于规范化后的行内容；CSV 中的位置永远不是身份。

只有当下面这些全部完全匹配时，多条证据行才能合并为一条 canonical observation：

```text
benchmark version
model configuration
normalized model/display setting
score series and role
protocol
task set
normalized score
```

这样做是有意让不同的 prompting 标签、harness、task subset 和 metric 保持分开。合并后的 observation 会保留每一个 evidence ID 和 score 资源。生成的 `data/evidence.jsonl` 必须与 canonical observations 引用的 evidence ID 一一对应：不允许有孤立的 evidence，也不允许一条 evidence 关联到多个测量。

Leaderboard 行和 lifecycle 卡片都是生成的 view。任何 benchmark 都不得被手动指派到某个 story tab，也不允许存在仅用于图表的分数。活跃的 benchmark ID 必须由生成的 leaderboard 和 detail 数据来表示。

每次新增 benchmark 或更新 observation 后，运行验收检查：

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_score_semantics.py
python3 scripts/validate_benchmark_integration.py
python3 scripts/audit_observation_dates.py
python3 scripts/audit_canonical_identity.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

接入 validator 会检查每个生成的 story-view 列表都存在、ID 唯一，并且能解析到活跃的 benchmark。一个 benchmark 合理地不出现在某个 view 中是允许的；但它不能是无法解析的，也不能因为只刷新了另一个 tab 而被漏掉。

选择证据（例如 citation counts）属于 curation 文档，需附带其来源和检查日期。它不是一个 leaderboard metric。缺少纵向数据本身不构成推迟一个重要 benchmark 的理由；身份、version、metric 不清，或测量对象不兼容，才是。

## 新增或编辑单个 benchmark

1. 只创建或编辑它的 `data/benchmarks/<id>.json` 声明，用于身份、taxonomy、双语文案、canonical score、协议、normalization 和源文件绑定。
2. 新增或更新对应的 `data/raw/<file>.csv` 证据行。
3. 不要手动编辑生成的 `site/data/index.json`、`site/data/benchmarks/<id>.json`、leaderboard 行、detail-page 对象或 lifecycle 成员。`site/data/benchmarks.json` 仍是一个 canonical 的全量 build 校验产物，不会被抓取或发布为运行时的 detail payload。
4. 运行上面的验收序列。build 会发现每一个 registry 文件，生成它的 leaderboard/detail 表示，并从 canonical metrics 派生出所有 story view。

带类型的 loader 会拒绝：缺失的 EN/ZH 文案、不支持的类型/单位、未知字段、重复的 ID 或测量身份、缺失的 raw 文件、非 HTTP 的源，以及不连续的 registry order。接入 validator 要求生成的 benchmark ID 与 registry ID 在相同的确定性顺序下一致。

每个 benchmark 还有一个或多个显式的 `labels`，取自 `data/capability_labels.json`。Domain 是互斥的；labels 是多对多的，用来描述任务在核心上所要求的能力。自由形式的 `tags` 可以描述协议、格式、人群或主题，但不得替代受控的 labels。新增或修改一张卡片时，遵循 [CAPABILITY_LABELS.md](CAPABILITY_LABELS.md)。

## 生成的运行时边界

浏览器首先加载 `site/data/index.json`，它只包含筛选、排序、leaderboard 行、lifecycle 成员和 story 卡片所需的字段。打开一张卡片会恰好加载一个 `site/data/benchmarks/<id>.json` 档案。共享的 `site/data/resources.json` registry 在首次进入 detail view 时惰性加载，随后被缓存。

这些拆分后的运行时文件是生成的，并被 gitignore。CI 和发布工作流会从被追踪的、按 benchmark 组织的源 registry 和 canonical observations 重新构建它们；它们从不作为源文件被审阅或编辑。

接入 validator 要求：

```text
active registry IDs
= canonical full snapshot IDs
= lightweight index IDs
= per-benchmark detail filenames and embedded IDs
```

它还会拒绝：沉重的 observations/frontiers/prose 泄漏进 index、过期的 lifecycle 列表、不完整的资源谱系、多余的 detail 文件，以及与 canonical build 不一致的 detail 记录。公开 bundle 会临时保留一个小的 `data/benchmarks.json` 作为 index 的别名，用于兼容目标工作流；它从不包含或替代完整的 detail 记录。
