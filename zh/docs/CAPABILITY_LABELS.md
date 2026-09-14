# Capability labels

BLE 把三类元数据分开：

- `evaluation_type` 描述被评测系统的行为方式：`Model` 或 `Agent`。
- `domain` 是一个互斥的主要任务或主题领域。
- `labels` 是一个多对多的列表，列出任务在核心上所要求的能力。

自由形式的 `tags` 仍可用于协议、格式、人群、实现和搜索等元数据。一个 tag 并不自动成为一个 capability label。

受控的双语词表存放在 `data/capability_labels.json`。每条记录包含一个简短名称、一条 taxonomy 定义，以及一句 `coverage_statement`，说明该能力如何在任务中体现。每个活跃的 benchmark 必须引用至少一个有效的 label ID。带类型的 registry loader 和接入 validator 会拒绝缺失、重复或未知的 label。

Detail 页面会在每个已指派的 label 下渲染其 coverage statement。前端从受控的 registry 解析这段文案；它不得在 HTML 或 JavaScript 中另行维护 label 的解释。让这句陈述保持具体、简短，并聚焦于被评测系统实际必须做的事。

## Curation 规则

只有当在 canonical benchmark 上取得成功确实需要某项能力时，才指派对应的 label。不要仅因为下面这些原因就添加 label：

- 领域名称里含有一个相似的词；
- evaluator 在幕后使用了代码或测试；
- 某个任务声明某个工具不可用；
- 该能力只是某个小子集中的附带要求；
- 某个自由形式的 tag 看起来像一个 label。

Labels 描述任务要求；它们并不主张某个 benchmark 从因果上隔离了模型的某个内部机制。一个宽泛的 benchmark 可以有多个 label。一个狭窄的 benchmark 完全可以只有一个 label。

Reasoning 类 label 是有意做到机制专一的。难度、多步骤工作、规划，或 benchmark 文案里出现“reasoning”这个词，本身都不足以支撑一个 reasoning label：

- `formal-deductive-reasoning` 需要显式的前提、规则、约束或一套形式系统；
- `rule-induction-abstraction` 需要从样例中发现潜在的规则或表示；
- `commonsense-inference` 需要用到未言明的日常或物理世界知识来判断可能的结果；
- `mechanistic-reasoning` 需要一个关于系统如何运作的因果、科学或操作性模型。

举例来说，一个会浏览、调用工具并做规划的 agent 并不自动就是 deductive 的。一个物理 benchmark 可以同时带有 `mechanistic-reasoning` 和 `quantitative-reasoning`，因为这两个 label 描述的是不同的要求。

`scripts/suggest_capability_labels.py` 是一个审计辅助工具。它的输出是一个起点建议，绝不是运行时的事实。被采纳的 label 会显式写入按 benchmark 组织的源记录，并在 diff 中接受审阅。

## 筛选语义

首页的 label 控件是多选的。多个被选中的 label 采用 AND 语义。例如：

```text
Planning + Tool use
```

会返回同时带有这两个 label 的 benchmark。Domain、evaluation type、年份、coverage、搜索和 labels 作为附加筛选条件组合在一起。应用筛选会恢复到 Capability frontier 升序排列，除非用户随后选择了另一个可排序的列。
