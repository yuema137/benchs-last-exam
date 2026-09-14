# Provenance 与 Resource 模型

静态 snapshot 只有一个 canonical `Resource` registry。一个 resource 是一条可复用、以 URL 为依据的证据记录，对应某个 benchmark、model 或共享的 evaluation 来源。observation 只存 `source_ids`，不重复保存 resource 的标题或 URL。

## Canonical artifacts

- `data/resources.json` 是生成的 resource registry。
- `data/models.json` 是生成的 reference-model 证据 registry。
- `data/observations.jsonl` 每行一条 canonical score observation。
- `data/evidence.jsonl` 包含每一条被接受的 source row，位于 exact-measurement 合并之前。
- `site/data/benchmarks.json` 是 canonical 的完整构建 validation snapshot。
- `site/data/index.json` 是前端首次加载用的轻量索引。
- `site/data/benchmarks/<id>.json` 是完整的、按需加载的 benchmark dossier，
  其中的 derived frontier points 保留 `observation_id` 和 `source_ids`。
- `site/data/resources.json` 是按需加载的公开 resource registry，供 detail
  页的 provenance 链接使用。

Snapshot schema version 2 把不可变的 source evidence 记录与去重后的 canonical measurements 分开，并为 resources、models 和 observations 使用语义化 ID。

运行：

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_provenance.py
```

## 日期语义

observation 会把 benchmark release date、model release date、evaluation date、result-public date、source-publication date 和 ingestion date 作为独立字段分别保留。对同一条 canonical measurement，`observation_date` 取最早可得的 evaluation/run date、model release date 或 score-publication date。只有当某个 source version 确实包含该 score 时，它的 publication date 才有资格参与。即使只有最早的日期驱动时间线，多个 source 仍然全部挂在该 observation 上。

lifecycle 图使用 `max(benchmark_release_date, observation_date)`。因此一条 pre-release observation 会显示为 `At release`，elapsed time 为零；它在 provenance 中的原始日期保持不变。禁止出现负的 T50/T80/T90 时长。

raw source rows 仍保留在 `data/evidence.jsonl`。canonical observations 只合并完全一致的 measurement identity，并保留 `evidence_ids`、`evidence_count` 和每一个 score source。observation、model 和 resource 的 ID 由语义 identity 生成，而非行号位置。这样既能安全地重排 source，又能让全部原始证据保持可审计。

## 由 model 预备的更新通道

在未来的手动 refresh 中，可以检查 benchmark-scoped 的 resource 是否有新的 model 结果，同时检查挂在 reference model 上的 resource 是否有新的 benchmark 结果。`watch` 和 `last_checked_at` 就是为此准备的。所需的清点与对账流程记录在 [`MODEL_RELEASE_UPDATE_PROTOCOL.md`](MODEL_RELEASE_UPDATE_PROTOCOL.md)。本层不包含任何 scheduler、crawler 或自动更新 job。

## 已知缺口

当前的导出为许多 observation 提供了 evaluation log 或 aggregator 链接，但并不是每个 score 都有 model 专属的官方 release resource 或 first-public result date。这些缺口由 `scripts/validate_provenance.py` 记录，而不是用猜测的 metadata 填补。
