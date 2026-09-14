# Benchmark Observatory 仓库章程

## 目的

Benchmark Observatory 追踪 benchmark 的生命周期及其测量价值。它不是一个模型排行榜，也绝不能把模型排名当作产品的首要抽象。

## 范围说明

这是一个轻量的个人 benchmark 知识库，也是一个 **Leaderboard of Benchmarks**，而不是评测平台或产品基础设施项目。

首选架构：

```text
curated source data → small Python scripts → generated JSON → static frontend → GitHub Pages
```

以简洁、可读、可维护、静态部署和便于人工整理为优化目标。不要引入后端服务器、数据库、公开 API、用户账户、云服务、遥测系统或复杂的接入框架，除非后续有明确决定要求这样做。只要本地脚本加生成的 JSON 能解决问题，它们就是默认选择。

仓库应始终保持为一个可信、可检验的研究基础设施项目。科学正确性、provenance、可复现性和显式的不确定性优先于覆盖面或视觉打磨。

## 模型覆盖原则

本系统的目标不是 model-complete，而是 model-representative。模型是被选中的 measurement probes，因为它们能补充时间、组织、能力、开放性或领域上的 coverage。

Benchmark health 和 evaluation coverage 是相互独立的维度。低覆盖或过期覆盖必须产出 `under_evaluated` 或 `unknown`，而不是 `healthy` 或 `stagnating`。当当前的 frontier probes 尚未被评测时，分数没有变动并不能作为 stagnation 的证据。

每个 reference model panel 都是带版本、依赖时间的。时刻 `t` 的历史 health 使用在 `t` 时刻生效的 panel，而不是把今天的 panel 追溯回去。

## 事实来源

- 英文文档是 canonical。
- 原始 benchmark observation 不可变。
- Benchmark 版本、metric 定义、协议和 provenance 都是一等记录。
- Reference model panel 及 panel 成员关系都是一等、带版本的记录。
- 派生出的 frontier、metric、lifecycle label 和 UI 数据是带版本的输出；它们必须能从原始输入中复现出来。
- 没有可追溯 provenance 的公开数字不可发布。

## 卡片与分析视图

- 每个 benchmark 版本对应一张以 benchmark 为中心的卡片或详情视图。
- 卡片记录该 benchmark 及其当前的纵向证据。
- 跨 benchmark 的问题属于对比视图和研究视图，而不属于单条事实字段。
- `domain` 是一个互斥的主要主题/任务领域。`labels` 是一组非空、多对多的受控能力需求，取自 `data/capability_labels.json`；自由格式的 `tags` 仍然是描述性的搜索元数据。Label 必须在 canonical benchmark 记录中显式给出，作为核心任务需求接受审查，绝不能在运行时从领域名称或文字描述中推断。参见 `docs/CAPABILITY_LABELS.md`。
- Reasoning label 必须指明一个具体机制。不要使用笼统的 reasoning label，也不要仅凭任务难度、多步骤行为、planning，或文字里出现“reasoning”一词就推断存在形式化演绎。
- 活跃度/采用度、provenance 质量、有效性和测量 health 必须保持为相互独立的维度。
- 当一项 metric 在科学上不适用时使用 `N/A`；当所需证据尚未知晓时使用 `?` 或一个显式的验证状态。

## 证据规则

- 优先采用原始论文、官方 benchmark 仓库、官方 leaderboard 或官方项目页面。
- 对照来源核实标题、日期、URL、metric、设置和数值主张。
- 绝不臆造分数、发布日期、上限、baseline 或不确定性。
- 保留相互冲突的 observation，而不是无声地覆盖它们。
- 把更正、撤稿、contamination 发现和协议变更记录为 validity/provenance 事件。
- 如果某个值尚无法核实，使用 `TODO(reference)` 或一个显式的不可用理由。

## 双语文档

英文树始终是 canonical。中文在 `zh/` 下镜像相同的结构。

镜像要求覆盖的是活跃的、手工撰写的文档。它**不**覆盖由脚本生成的文件（审计报告 `docs/CANONICAL_IDENTITY_AUDIT.md`、`docs/OBSERVATION_DATE_AUDIT.md`、`docs/SCORE_ADVERSARIAL_AUDIT.md`、`MATH_LEVEL5_TIME_AUDIT.md` 和 `docs/PROVENANCE_GAPS.md`），也不覆盖那些记录某个带日期的发现、而非一条长期规则的一次性审计快照（`MATH_LEVEL5_HISTORICAL_RECONSTRUCTION.md`、`docs/DOMAIN_CURATION_AUDIT.md`、`docs/FRONTIER_MODEL_CARD_AUDIT.md` 和 `docs/GPT6_PUBLIC_BENCHMARK_AUDIT.md`）。这些文件只保留英文。

工作循环：

1. 完成并审查一批英文内容。
2. 立即同步对应的中文页面。
3. 检查 claim、公式、label、链接、数字、caveat 和 N/A 理由是否一致。
4. 独立地阅读中文页面，检查其自然度和歧义。
5. 验证每个英文页面都恰好有一个预期的中文对应页面。

翻译是语义层面的，而非逐词翻译。Benchmark 名称、模型名、论文标题、项目名、专有名词、代码标识符、公式和稳定的 metric label 保持不变，除非确有必要使用一个有据可查的中文 label。中文行文可以重组英文句子，但不得强化、弱化、省略或添加任何 claim。

中文镜像不是第二个事实来源。先修改英文，再同步中文。

## 解释风格

采用 `EXPLANATION_STYLE.md` 中的原则。DongbeiGPT 式的节奏是克制而平易的：它可以让面向用户的解释更温和、更易懂，但绝不能变成方言表演、玩笑、口头禅，或改变科学含义。

该风格适用于对话式解释和明确选定的解释性行文。它不会自动适用于代码、代码注释、schema、测试、配置、Git message、API 字段或正式的研究 claim。

## 工程边界

- 保持 source data、schema、validation、normalization、frontier computation、metric、生成的 JSON 和 UI 之间的模块化。
- 优先采用小型的 scripts/data/frontend 结构，而非服务边界。API 层和数据库层被推迟，不属于当前架构。
- 把科学规则挡在 frontend 组件之外。
- 每实现一项 metric 都要配上测试。
- 不要在 MVP 中加入 composite health score。
- 在检查经验分布之前，不要指定 lifecycle 阈值。
- 保留 right-censored 的 benchmark，以备后续做 survival analysis。
- 每次新增 benchmark 都必须是 `data/benchmarks/<benchmark-id>.json` 下一条完整的类型化记录，满足 `docs/BENCHMARK_INTEGRATION.md` 中的 Benchmark Integration Contract，并在被视为完成之前通过 `python3 scripts/validate_benchmark_integration.py`。逐 benchmark 的 registry 是唯一的活跃卡片 registry；绝不要把 benchmark 定义或卡片文案直接加进构建脚本或 frontend。这同样适用于带有真实 `Unknown`、`N/A` 或 `—` 值的 partial-core benchmark，以及完全测量过的 benchmark。
- 每次 benchmark 或 observation 更新都必须一并重新生成并验证全部四个 lifecycle 故事视图：`Test of Time`、`Still Frontier`、`Fastest Solved` 和 `Recently Saturated`。它们的成员关系由 canonical lifecycle metric 在一次构建中生成；绝不要单独维护或更新某一个 tab。
- 公开数据是一个生成的两阶段 bundle：`site/data/index.json` 只包含 leaderboard/story 字段，而 `site/data/benchmarks/<id>.json` 包含完整的卡片/详情记录并按需加载。每条活跃 registry 记录都必须在两层中各恰好存在一次。绝不要让 frontend 为其首次渲染去拉取那份庞大的 canonical validation snapshot，也绝不要手工编辑任一生成的层。

## 卡片更新同步不变式

对某个 benchmark/卡片的任何改动，除非另有证明，否则都同时是一次影响 lifecycle 的改动。这包括对 observation、分数、模型发布日期、benchmark 发布/版本元数据、协议资格、frontier 事件、coverage 或成本的改动。

Lifecycle 日期使用一条统一的 observation-time 规则。对同一条 canonical measurement，收集所有可得的评测/运行日期、模型发布日期和分数发布日期，然后取最早的候选作为 `observation_date`。当多份发布资源包含同一分数时，使用实际包含该分数的最早来源版本，而不仅仅是论文或页面的第一个版本。Lifecycle 的 `plot_date` 是 `max(benchmark_release_date, observation_date)`，而 T50/T80/T90 在零处被截断并显示为 `At release`；原始的发布前日期在 provenance 中保持不变。绝不能输出负的 lifecycle 时长。

原始 source row 和 canonical measurement 是相互独立的两层。每条被接受的 source row 都必须有一个稳定的、与行顺序无关的 evidence ID。只有当 benchmark 版本、模型配置、归一化模型 label、canonical/auxiliary score series、协议、任务集和精确归一化后的分数全都一致时，才能把多行合并成一条 canonical observation。Canonical observation ID 由那些语义字段派生，绝不来自 CSV 行号。合并时必须保留每个 evidence ID 和分数资源；设置不同的行仍保持为各自独立的 observation。`data/evidence.jsonl` 与 canonical observation 的谱系必须精确对账。

在任何此类改动之后，agent 必须：

1. 重建 canonical snapshot；
2. 重新计算该 benchmark 的 capability frontier 和 lifecycle metric；
3. 针对**每一个** lifecycle selector 检查该 benchmark，既检查成员关系也检查非成员关系：
   - `Test of Time`
   - `Still Frontier`
   - `Fastest Solved`
   - `Recently Saturated`
4. 确认任何新符合或被取消资格的卡片都自动反映在生成的成员列表中；
5. 核实 Leaderboard 行、详情页、筛选器、卡片 metric、sparkline 和 provenance 都解析到更新后的 canonical 数据；
6. 在报告完成之前，运行 `python3 scripts/validate_benchmark_integration.py`、provenance 验证和测试套件。

Integration validator 会独立地重新计算全部四个 lifecycle 成员关系，并将其与生成的 snapshot 比较。一个过期或只更新了一部分的 tab 属于硬性失败，即便 benchmark 卡片本身渲染正确也是如此。

Lifecycle 卡片的 hero metric 必须使用与其 selector 相同的分数语义。特别地，`Still Frontier` 是按 normalized progress 低于 50% 来选择的，因此它的 hero 值和解释性文案必须展示 normalized progress——而不是原始的 benchmark 分数。如果两者都有用，原始 frontier 只能作为一个明确标注的辅助 metric 出现。

分数更新还必须额外运行 `python3 scripts/validate_score_semantics.py`。Ratio metric 必须保持在 `[0, 1]` 内；诸如分钟、Elo 或业务结果这类无界数值 metric 绝不能被自动转换为百分比。归一化的 `floor` 可能是一个 chance/reference baseline，而非一个硬性下界，因此一条真实的低于 floor 的 observation 应被保留并调查，而不是无声地钳制或删除。

极端值需要显式的对抗性审查。任何引入了低于 `1%` 的 ratio observation 或高于 `100` 的无界数值 observation 的 benchmark 组，都必须对照其主要测量来源核查，并记录在 `scripts/validate_score_semantics.py` 的 `REVIEWED_LOW_RATIO_BENCHMARKS` 或 `REVIEWED_LARGE_NUMERIC_BENCHMARKS` 中。一个未经审查的极端分数组属于硬性验证失败；绝不能通过无声地钳制、重新缩放或删除 observation 来“修复”它。

不要只更新可见的 benchmark 卡片就假定 story tab 仍然正确。不要为了弥补过期的派生数据而手动修补某个 tab。如果某个 lifecycle 结果发生了变化，生成的 snapshot 及其源数据必须包含在同一次改动中。

## Canonical score 不变式

每个 benchmark/版本都必须声明恰好一个 canonical score series。只有 canonical-series 的 observation 才可以决定：

- capability frontier 和 current frontier；
- normalized progress、headroom、T50/T80/T90 和 velocity；
- leaderboard 的值和排序；
- 每个 lifecycle 故事 tab 中的成员关系和排序。

其他 metric、任务集变体、协议变体或辅助评测必须作为显式标注的 `auxiliary_score_series` 保留。Auxiliary series 只能出现在 benchmark 详情页上，配以视觉上有区分度的线型/点型、对该 metric/协议差异的解释，以及 canonical 的 observation/来源谱系。它们必须带有 `lifecycle_eligible: false`，并且绝不能影响 leaderboard 排序、lifecycle 阈值、story-tab 成员关系或 canonical frontier。

更改 canonical score 是一次 benchmark 版本的方法学变更，而非表面的编辑。它需要来源审查、显式的理由、snapshot 重新生成、重新计算所有 lifecycle selector，以及完整的 integration/score-semantics 测试套件。绝不要仅仅因为某个可得分数最高、最新或最容易提取就选它作为 canonical score。
