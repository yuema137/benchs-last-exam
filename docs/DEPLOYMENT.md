# BLE deployment

BLE is the source of truth. The deployed copy under `yuema137.github.io/ble/`
is a generated static snapshot, not a second editable source tree.

On every relevant merge to BLE `main`, the source workflow:

1. runs provenance validation, unit tests, and JavaScript syntax checks;
2. builds `index.html`, `app.js`, `styles.css`, a lightweight benchmark index,
   one lazy detail JSON per benchmark, the resource registry, and `manifest.json`;
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

The deployed runtime does not include the 25 MB monolithic validation snapshot.
Its initial request loads `data/index.json`; a benchmark click loads only
`data/benchmarks/<id>.json` plus the shared resource registry on first use. A
small `data/benchmarks.json` compatibility alias currently mirrors the index so
the destination repository's existing deterministic boundary check remains
backward compatible.

Each public detail file omits fields of the canonical validation snapshot that
duplicate a published field or that the frontend never reads (`frontier`,
`frontier_events`, `historical_frontier`, `retrospective_observations`; see
`src/benchmark_observatory/public_bundle.py`). The canonical snapshot keeps them.

Cache busting is derived from content, never maintained by hand. Source files
carry `?v=dev` tokens; `scripts/build_pages_snapshot.py` replaces them with short
SHA-256 hashes of the published data files (all data requests), `styles.css`,
and the final `app.js`, and records them as `asset_versions` in `manifest.json`.
Any data, style, or code change therefore produces new URLs, while an unchanged
rebuild keeps the same ones.

`index.html` declares a self-only Content-Security-Policy (scripts, styles, and
fetches from the same origin; no inline script or style attributes) and a
canonical URL of `https://yuema137.github.io/ble/`. Data-derived text is
HTML-escaped in `app.js`, and only `http`/`https` URLs become link targets.
