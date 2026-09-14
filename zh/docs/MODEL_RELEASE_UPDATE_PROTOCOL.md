# 模型发布更新协议

本项目是一个经过策展的 **Leaderboard of Benchmarks**，而不是一个穷尽式的
模型或文献数据库。当用一个新的模型发布页、model card 或 system card 来更新
benchmark observations 时，更新必须从一次源级别的清点开始。

要求的顺序是：

```text
inventory the source
→ reconcile with the benchmark registry
→ update canonical observations
→ rebuild derived data
→ validate completeness and provenance
```

## 1. 改数据之前先清点

枚举源中展示的每一个对外报告的 benchmark 或 evaluation，包括通过以下方式暴露的结果：

- 可访问的 HTML 文本和表格；
- 发布页显式引用的 tab、carousel，以及链接的 model/system card；
- 内嵌的 JSON 或 script 数据；
- SVG 或其他图表的 DOM 数据；
- 浏览器网络响应，或在可用时的 JavaScript 状态；
- 图像或 canvas 图表，仅在退而求其次时才使用视觉提取。

临时的清单应记录：

```text
benchmark/evaluation
score, if extractable
metric
source location
extraction method
```

结构化提取优先于视觉转录。某个图表没有出现在初始页面文本中，并不能证明它的数据不存在。

## 2. 与策展后的 registry 对账

把完整的源清单与被追踪的 benchmark registry 对账。每一个匹配到的条目必须恰好落在其中一个状态：

```text
UPDATED
ALREADY CURRENT
SKIPPED_WITH_REASON
EXTRACTION_FAILED
NOT TRACKED
```

对账必须保持平衡：

```text
tracked source results
= UPDATED + ALREADY CURRENT + SKIPPED_WITH_REASON + EXTRACTION_FAILED
```

`NOT TRACKED` 单独报告，因为它标识的是一个可能的未来策展候选，而不是对某个已有 benchmark 的更新。

任何匹配到的结果都不得在清点和报告之间悄无声息地消失。

## 3. Canonical observation 要求

每一个被接受的 score 都是策展后源数据中的一条 canonical observation。它必须包含或能解析出：

- benchmark 和 benchmark version；
- model/system 和 model family；
- score 和 metric；
- 协议或 evaluation 设置；
- evaluation/run 日期、模型 release date，以及推导最早 observation date 所需的每一个已知 score 发表日期；
- 已知时的 evaluation 日期和结果公开日期；
- 一个或多个 canonical resource ID。

当 arXiv、Hugging Face、OpenReview 或另一个源发表了同一测量时，保留每一份资源，并使用确实包含该 score 的、日期最早的版本。不要把一个 score 回溯到一个并不包含它的更早的源修订。绘图和 lifecycle 阈值会把被选中的 observation date 裁剪到 benchmark release 处，而 provenance 保留未裁剪的日期。

前端从不接收仅用于图表的 score。Frontier points 从 canonical observations 派生，并保留它们的 observation ID 和源谱系。

不要合并 benchmark version、task set、scorer、prompt、harness 或 tool 设置有实质差异的结果。如果某个差异重要且无法调和，就使用 `SKIPPED_WITH_REASON` 或 `EXTRACTION_FAILED` 并说明原因。

## 4. 提取顺序

检查一个官方源时使用以下顺序：

1. 语义化 HTML 和可访问文本；
2. HTML 表格；
3. 内嵌的 JSON 或 script 数据；
4. SVG DOM 的标签/数据；
5. 浏览器网络响应或页面 JavaScript 状态；
6. 截图/图像的视觉读取作为退而求其次的手段。

在更新审计中记录所使用的方法。视觉提取应在可行时保留一张源截图或直接的源位置，且不应被用来猜测被难以辨认的图形所隐藏的数值。

## 5. 必需的更新报告

每次模型发布更新都应留下一条简短的审计记录，例如：

```text
Model: Example Model
Source: https://example.com/release

Benchmark                         Found  Tracked  Result
GPQA Diamond                     yes    yes      UPDATED
OSWorld 2.0                     yes    yes      ALREADY CURRENT
Example New Benchmark            yes    no       NOT TRACKED
Chart-only evaluation           yes    yes      EXTRACTION_FAILED
```

报告还必须列出：

- 所有本项目未追踪的源 evaluation；
- 无法可靠提取的 score；
- 非文本结果的提取方法；
- 协议/version 方面的注意事项；
- 新增或确认的 observation；
- 任何 provenance 缺口。

## 6. 更新方向

资源模型支持两个相互独立的发现方向：

```text
benchmark resources → discover new model results
model resources     → discover new benchmark results
```

本协议不授权任何自动 crawler、scheduler、backend 或 database。更新仍然是人工策展的，并且可以从签入的源数据复现。

## 7. 完成规则

一次更新只有在下列命令之后才算完成：

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_provenance.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

并且源的清点/对账报告没有任何无法解释的未匹配条目。
