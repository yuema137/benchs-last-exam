# Vertical Slice Plan

状态：进行中，2026-09-03

## Baseline

Git baseline：`00bc31e Establish methodology and typed schema baseline`。

## Pilot selection

第一个 slice 使用来自 Epoch AI 公开数据导出的四条 benchmark 记录：

| Benchmark | 在 slice 中的角色 | Metadata | Raw observations | 初始 metrics |
|---|---|---|---:|---|
| MMLU | 老的、覆盖面广的 benchmark | 固定 accuracy 量表；random-choice floor | 249 | frontier、progress、headroom、thresholds、velocity、coverage |
| GSM8K | math 轨迹 | exact-match accuracy；固定 bounds | 235 | frontier、progress、headroom、thresholds、velocity、coverage |
| GPQA Diamond | 高难度科学 reasoning | accuracy；four-choice floor | 311 | frontier、progress、headroom、thresholds、velocity、coverage |
| SWE-bench Verified | 更高负担的 coding/agent benchmark | issue-resolution rate；variant-specific | 35 | frontier、progress、headroom、thresholds、velocity、coverage |

上面的计数是对下载导出的一次 ingestion audit，而不是对 benchmark 质量的产品性论断。该导出于 2026-09-03 从 [Epoch AI 的数据页](https://epoch.ai/benchmarks/use-this-data) 获取。其附带的 README 说明了数据 license 与引用要求。

## Data-source audit

- 主要 benchmark metadata 仍然链接到每个 benchmark 的 original paper 或官方项目。
- 在这第一个 slice 中，Epoch AI 被视为可信 aggregator，`SourceProvenance.source_type = trusted_aggregator`。
- internal 与 external 的 run 仍然可以区分。
- 缺少 model date、缺少 source 链接或 setting 不兼容的 observation 不会被静默丢弃；normalization 会给出一个 validation 理由。
- 导出中的 “Best score (across scorers)” 字段不能自动与每一个 external score 互换。protocol class 和 source 字段必须保留。

## 第一个本地产品的范围

先实现一个静态 snapshot 和一个原生浏览器 read layer。它必须支持：

- 带紧凑 SOTA frontier curve 的 benchmark card；
- calendar-age 和 since-release 两种 x 轴模式；
- 在有 bounds 时提供 raw 和 normalized 两种 y 轴模式；
- 按 age、frontier、headroom、T50、T90、velocity 和 current coverage 排序；
- 带 frontier provenance 的 benchmark detail view；
- 区分 reached、right-censored、not-applicable 和 unknown 四种 threshold 状态；
- 分开的 health 与 evaluation coverage 字段。

discrimination、cost、adoption 和复杂的 lifecycle 规则在其 raw input 可用之前，保持显式的 `N/A` 或 `insufficient_data`。
