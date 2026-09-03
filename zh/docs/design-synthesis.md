# Benchmark Observatory：初始设计综合

状态：草案，2026-09-03

## A. 研究与产品综合

### 产品主张

Benchmark Observatory 是一个以 benchmark 为中心、持续记录、带版本管理的观测系统。用户首先浏览的是 benchmark；模型评测结果只是带时间戳的证据，用来重建 benchmark 随时间变化的测量轨迹。

产品应展示多个可以解释的维度，而不是压缩成一个不透明的健康分数：

- 在 floor 和 ceiling 有可靠定义时，展示 normalized progress 和 remaining headroom；
- 展示达到 T50、T80、T90 所需的时间；
- 展示近期 frontier velocity；
- 展示近期模型的分数分布和 discrimination；
- 把 reporting activity / adoption 作为独立维度；
- 展示带有解释依据的 lifecycle state。

首页是紧凑的 benchmark leaderboard table：每个 benchmark 占一行，方便快速比较生命周期字段。点击后进入 detail page；detail 才承载完整 frontier curve、provenance、coverage breakdown、caveats 和次级 metrics。

### 以 model-representative 为目标的 coverage

本系统有意不追求 model-complete，而是维护一个规模较小、带版本和时间范围的 `ReferenceModelPanel`，把模型当作 capability frontier 的 measurement probes。只有当一个模型能补充时间、组织、能力、开放性或领域 coverage 时，才考虑加入 panel。

对 benchmark `B`，预期 panel 为 `P_B(t) = P_core(t) ∪ P_domain(B)(t)`。panel 随时间变化，因此 2024 年的 health snapshot 应使用 2024 年有效的 panel，不能事后用更晚发布的模型回填判断。

系统必须分开两个轴：**Benchmark Health** 描述 headroom、threshold、frontier velocity、discrimination、saturation 和 stagnation；**Evaluation Coverage** 描述当前是否真的有足够新、足够强的 probe 测过这个 benchmark。coverage 是 health 结论的证据强度，不是 health 本身的一部分。coverage 低或过期时，状态应为 `UNDER_EVALUATED` / `UNKNOWN`，不能直接标为 `HEALTHY` 或 `STAGNATING`。

至少分别展示 historical coverage 和 current frontier coverage。最简单的形式是 `C_B(t; Δ) = 最近窗口内已评测的 panel 成员权重 / 有资格的 panel 成员权重`。初版可以使用 equal weights，但必须保留 role 和 organization，以便以后区分 frontier probe、domain specialist、open-weight probe、historical anchor 以及同一 family 的相关成员。

### 参考项目带来的设计经验

`scientific-eval-environments` 提供了几条适合复用的原则：每个主要对象使用轻量事实卡片；源文件是事实来源，交互式 explorer 是生成的展示层；不同问题使用不同导航轴；首次公开日期必须有来源；`N/A` 和 `?` 要严格区分；索引和交叉链接应自动检查；事实卡片与综合分析分开；自动更新必须保留人工审核。

本项目会采用这些原则，但不会照搬目录。不可变的结构化 observation 和 benchmark/version registry 才是本项目的 source of truth；benchmark card 是它们的查询或生成视图。保留“先看 card，再看 index”的使用方式，同时给每个 derived view 加上 snapshot ID。除非仓库以后明确要求，否则不建立中文镜像以外的额外语言层。

### 中英文同步原则

英文文档是 canonical version，中文文档在 `zh/` 下保持对应目录。中文不是逐词翻译，而是保持技术含义、数字、公式、链接、限定条件和 provenance 不变的自然中文。benchmark 名称、模型名、论文标题、项目名、专有名词、代码标识符和稳定 metric label 默认保留英文。

每完成一批英文内容，就立即同步对应中文页面；同步后要单独以中文读者视角检查自然度和歧义。中文镜像不是第二个事实来源，修改应先发生在英文页面。

### 解释原则

面对用户解释复杂问题时，采用 DongbeiGPT 的克制原则：先讲实际问题，再说清楚谁对什么做了哪一步变化，必要时用一个小例子把数据或状态走一遍，最后说明边界和不能推出的结论。表达可以自然、亲切、好懂，但不做方言表演，不堆口头禅，不用玩笑替代定义，也不能为了顺口改变科学含义。

代码、schema、测试、配置、Git message 和正式方法学定义不自动使用这种口吻；它们保持专业、稳定、可机器处理的表达。

## B. Canonical schema proposal

中文页面与英文页面共享同一组 schema、公式、字段名和版本语义。详细 schema、metric specification、pilot benchmark proposal 与 implementation plan 以英文 canonical page 为准；本镜像必须在每次英文页面更新后同步。

核心对象关系如下：

```text
Benchmark
  └── BenchmarkVersion
        ├── MetricDefinition
        ├── evaluation protocol
        └── ScoreObservation[]
              ├── Model
              └── SourceProvenance
```

主要字段包括：

- `Benchmark`：canonical name、aliases、domains、modality、description、versions；
- `BenchmarkVersion`：version label、release date、dataset、scoring protocol、metric definition、validity status；
- `MetricDefinition`：name、direction、unit、bounded、floor、ceiling、normalization policy version；
- `Model`：canonical name、family、release date、provider、model card；
- `Model`：canonical name、family、release date、provider、model card、organization、roles、domains、panel start/end、inclusion reason、predecessor；
- `ReferenceModelPanel`：panel ID、label、valid from/until、core 或 domain scope、domain、member IDs、methodology version；
- `PanelMembership`：panel/model、role、organization、weight、valid from/until 和 inclusion reason；
- `SourceProvenance`：source type、URL、title、publisher、publication date、retrieved time、source revision；
- `ScoreObservation`：benchmark version、model、score、evaluation/report/public availability dates、protocol、setting、uncertainty、provenance、validity status、parser version；
- `FrontierPoint`：as-of date、frontier score、来源 observation IDs、metric direction、derivation version；
- `DerivedBenchmarkMetrics`：current frontier、normalized progress/headroom、T50/T80/T90、30/90/180/365-day velocity、discrimination、last frontier change、activity、unavailable reasons；
- `DerivedBenchmarkMetrics` 还必须包含 historical/current frontier evaluation coverage、eligible panel IDs 和 freshness/counts；
- `LifecycleEvidence`：snapshot、state、rule version，以及每条 metric evidence 和解释；
- `DataSnapshot`：as-of time、raw input revisions、transformation/metric/lifecycle versions 和 artifact URI。

原始 observation 不可变。frontier、metrics 和 lifecycle evidence 都是带 lineage 的 derived artifacts。不同 benchmark version 或不兼容 protocol 不能静默合并。

## C. Metric specification

设 `F` 为 floor，`C` 为有依据的 ceiling，`s(t)` 为历史 frontier 的 step function，`r` 为 benchmark release 或首次公开日期。

| Metric | 定义 | 适用条件与边界 | 输出与测试 |
|---|---|---|---|
| Current frontier | higher-is-better 取 `max(score)`；lower-is-better 取 `min(score)` | 只使用有效且可比较的 observations；不同版本不合并 | 原始 metric 单位；测试方向、tie、无序和 invalid rows |
| Normalized progress | higher-is-better：`(s-F)/(C-F)`；lower-is-better：`(C-s)/(C-F)` | 必须有固定且有意义的 `F`、`C`，且 `C != F`；越界值要 flag | `[0,1]`；测试 zero/random floor、缺失 bounds、lower-is-better |
| Normalized headroom | `1 - progress` | 与 progress 相同 | `[0,1]`；测试刚好到达 floor/ceiling |
| T50/T80/T90 | 第一个满足 `t >= r` 且 normalized progress `>= q` 的日期 | 没有可靠 fixed bounds 时为 `N/A`；没达到的 benchmark 是 censored | 从 release 到 crossing 的时长和日期；测试 exact hit、never reached、同日 reports |
| Frontier velocity | `(s(now)-s(now-window))/window` | sparse data 必须返回 `N/A` 或带 flag 的 estimate；native 与 normalized 版本分开 | score/day 或 progress/month；测试 boundary 缺失和无历史数据 |
| Recent frontier discrimination | 在配置的 recent qualified cohort 上输出 `n`、median、IQR、standard deviation、top-minus-k spread 和原始 observations | cohort、family deduplication、protocol class、uncertainty 必须可见；不只保留一个数字 | 原始 metric 单位；测试样本不足、重复 family 和 uncertainty |
| Days since last SOTA | `as_of - last frontier change date` | 同时展示 raw delta；没有 threshold/uncertainty 时不声称“meaningful” | 天数和日期；测试 ties、retractions |
| Recent activity | 30/90/180 天内的 observations、distinct model families、reports 数量 | 与 measurement health 分开；明确 deduplication policy | 数量/速率；测试重复 reports 和同模型多条 observation |
| Evaluation coverage | 在指定窗口内已评测的、与时间匹配的 panel 成员占 eligible panel 成员的权重或比例；按 role、organization、domain 分组 | 需要 versioned panel 和 capability/time window；coverage 低或过期时不能下强 lifecycle 结论 | `[0,1]` 加 counts 与 freshness；测试历史 panel 选择、panel end date、缺少 evaluation 和 domain specialist |

Lifecycle 一开始只使用 `insufficient_data` 或 `under_evaluated`，等 pilot 数据分布和 panel coverage 检查完再制定阈值。当 current frontier coverage 低于证据阈值时，`under_evaluated` 优先于其他 health label。只有在 coverage 足够、headroom 仍然较大、并且 frontier 长期低速移动时，才能叫 `stagnating`。规则必须输出证据，例如“current frontier coverage 82%、normalized progress 92%、recent IQR 1.2 pp、180 天 frontier gain 0.4 pp”。MVP 不需要 composite health score。

## D. Pilot benchmark proposal

首批建议候选：MMLU、GSM8K、MATH/MATH-500、HumanEval、GPQA Diamond、SWE-bench、MMMU、MathVista、SimpleQA、Humanity's Last Exam、ARC-AGI-1、ARC-AGI-2 和 FrontierMath。

它们覆盖 general knowledge、math、coding、science/reasoning、multimodal 和 agents。每个 benchmark 只有在 metadata、protocol comparability 和 provenance 检查通过后，才进入公开 snapshot。

候选原始资料包括各 benchmark 的 original paper、official repository、official leaderboard，以及 Epoch AI 的结构化数据。具体 release date、floor、ceiling 和 scores 必须在 ingestion 时从原始来源提取，不能凭记忆补齐。

特别注意：SWE-bench 的原始 benchmark、Verified 等 variant 必须分开；GPQA、HLE 等 benchmark 的数据质量和审计结果应保留为 validity caveats；FrontierMath 等 private-test benchmark 在 floor/ceiling 无法确认前，T50/T80/T90 应显示 `N/A`。

## E. Implementation plan

### Milestone 1：repository and contracts

建立 `README.md`、`src/schema/` 和 `pyproject.toml`。schema tests 必须拒绝缺失 provenance、非法 direction 和不一致 bounds。

### Milestone 2：curated registry and raw fixtures

建立 `data/benchmark_registry/`、`data/fixtures/`、`src/validation/` 和 `src/provenance/`。先验证 3–5 个 benchmark version；原始 observation 不可变，每条公开记录都有 provenance，并覆盖 duplicate/conflict tests。

### Milestone 3：frontier and metric engine

建立 `src/frontier/`、`src/metrics/` 和对应 tests。实现 deterministic frontier、normalization、threshold、velocity、discrimination、activity、last-SOTA，并覆盖本页 C 节的 edge cases。

### Milestone 4：snapshot CLI

建立 `src/snapshots/`、`scripts/build_snapshot.py` 和 `data/snapshots/`。同一输入重复运行应产生稳定 artifact，并记录 raw references、derived records、unavailable reasons 和所有版本号。

### Milestone 5：pilot expansion and manual audit

扩展到 10–20 个 benchmark，逐条人工检查 frontier curves，并发布 limitations report。不能为了填满表格而加入证据不足的 benchmark。

### Milestone 6：benchmark cards and comparison table

建立 `apps/web/` 和 read-model/API。card 展示 current frontier、headroom、thresholds、velocity、discrimination distribution、activity、lifecycle evidence 和可点击 provenance；metric logic 不进入 frontend。

### Milestone 7：global lifetime analysis

增加 release date vs T90 图，明确区分已 crossing 和 right-censored benchmark，并支持 domain 和 metric applicability 筛选。

### Milestone 8：source adapters and refresh

实现 `fetch → parse → normalize → validate → conflict report → snapshot`。至少让一个 structured source 的完整流程可复现，并保证 adapter-specific quirks 不泄漏到 metric code。

## 当前决定与待决定事项

现在确定：benchmark/version identity、immutable raw observations、source tiers、显式 `N/A`、activity 与 health 分离，以及 English canonical / Chinese mirror 规则。

等 pilot 数据检查后再决定：lifecycle thresholds、family deduplication、frontier cohort 最小样本数、meaningful SOTA delta、interpolation policy，以及是否使用 “half-life” 这个术语。
