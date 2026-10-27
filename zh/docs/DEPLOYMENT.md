# BLE deployment

BLE 是 source of truth。`yuema137.github.io/ble/` 下部署的副本是一份生成的静态 snapshot，不是第二棵可编辑的 source tree。

每当有相关变更 merge 到 BLE `main`，source workflow 会：

1. 运行 provenance validation、单元测试和 JavaScript 语法检查；
2. 构建 `index.html`、`app.js`、`styles.css`、一个轻量 benchmark index、
   每个 benchmark 一份的按需 detail JSON、resource registry 和 `manifest.json`；
3. 验证 bundle 中没有 symlink 或开发用的 Markdown 文件；
4. 只更新 personal-site 仓库中的 `auto/ble-sync`。

personal-site 仓库独立验证该分支只改动了 `ble/**`，然后创建并 merge 一个生成的 snapshot PR。它的 Pages workflow 把 `ble/` 作为一个可选的、在 allowlist 中的 section 暂存。因此一次失败的构建或 validation 会让此前的线上 snapshot 以及 personal site 的其余部分保持不变。

`manifest.json` 记录 BLE 的 source SHA 和构建时间。要回滚，可在 personal-site 仓库中 revert 生成的 BLE snapshot commit，或从记录的 source SHA 重新构建。

source workflow 期望 personal-site 仓库有一个专用的 `BLE_PERSONAL_SITE_DEPLOY_KEY` secret，对该仓库具备写权限。任何 key 或凭据都不应放在本仓库中。

部署的 runtime 不包含那份 25 MB 的单体 validation snapshot。它的首次请求加载 `data/index.json`；点击某个 benchmark 时，才在首次使用时加载 `data/benchmarks/<id>.json` 以及共享的 resource registry。目前有一个小的 `data/benchmarks.json` 兼容 alias 镜像该 index，以便目标仓库既有的确定性 boundary check 保持向后兼容。

每个公开 detail 文件都会省略 canonical validation snapshot 中那些与已发布字段重复、或前端从不读取的字段（`frontier`、`frontier_events`、`historical_frontier`、`retrospective_observations`；见 `src/benchmark_observatory/public_bundle.py`）。canonical snapshot 仍保留这些字段。

Cache busting 由内容派生，从不手工维护。源文件使用 `?v=dev` 占位；`scripts/build_pages_snapshot.py` 会把它们替换为短 SHA-256 哈希：所有数据请求使用已发布数据文件的哈希，`styles.css` 和最终的 `app.js` 各用自身内容的哈希，并把这些值以 `asset_versions` 记录在 `manifest.json` 中。因此任何数据、样式或代码变化都会产生新的 URL，而内容不变的重建会保持相同 URL。

`index.html` 声明了仅允许同源的 Content-Security-Policy（脚本、样式和请求都只来自同源；不使用内联脚本或 style 属性），以及 canonical URL `https://yuema137.github.io/ble/`。`app.js` 会对来自数据的文本做 HTML 转义，并且只把 `http`/`https` URL 用作链接目标。
