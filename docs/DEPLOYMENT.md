# BLE deployment

BLE is the source of truth. The deployed copy under `yuema137.github.io/ble/`
is a generated static snapshot, not a second editable source tree.

On every relevant merge to BLE `main`, the source workflow:

1. runs provenance validation, unit tests, and JavaScript syntax checks;
2. builds `index.html`, `app.js`, `styles.css`, generated `data/`, and `manifest.json`;
3. validates that the bundle has no symlinks or development Markdown files;
4. updates only `auto/ble-sync` in the personal-site repository.

The personal-site repository independently validates that this branch changes
only `ble/**`, then creates and merges a generated snapshot PR. Its Pages
workflow stages `ble/` as an optional allowlisted section. A failed build or
validation therefore leaves the previous live snapshot and the rest of the
personal site unchanged.

`manifest.json` records the BLE source SHA and build time. To roll back, revert
the generated BLE snapshot commit in the personal-site repository, or rebuild
from the recorded source SHA.

The source workflow expects the personal-site repository to have a dedicated
`BLE_PERSONAL_SITE_DEPLOY_KEY` secret with write access to that repository.
No key or credential belongs in this repository.
