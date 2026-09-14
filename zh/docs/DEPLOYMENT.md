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
