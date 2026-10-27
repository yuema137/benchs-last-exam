#!/usr/bin/env python3
"""Build the self-contained static bundle published under /ble/."""

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_VERSION_TOKEN = 'const DATA_VERSION = "dev";'
STYLE_TOKEN = 'styles.css?v=dev'
APP_TOKEN = 'app.js?v=dev'


def content_hash(paths, root):
    """Short SHA-256 over file names and bytes, independent of build time."""
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(root).as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()[:12]


def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"expected exactly one {old!r} in {path}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def stamp_cache_versions(output):
    """Derive cache-busting query strings from the published bytes.

    Data requests use one hash of every published data file; the stylesheet and
    script URLs use the hash of their final contents, so any data, style, or code
    change produces new URLs while unchanged builds keep stable ones.
    """
    data_dir = output / "data"
    versions = {"data": content_hash([path for path in data_dir.rglob("*.json") if path.is_file()], output)}
    replace_once(output / "app.js", DATA_VERSION_TOKEN, 'const DATA_VERSION = "%s";' % versions["data"])
    versions["styles"] = content_hash([output / "styles.css"], output)
    versions["app"] = content_hash([output / "app.js"], output)
    replace_once(output / "index.html", STYLE_TOKEN, f"styles.css?v={versions['styles']}")
    replace_once(output / "index.html", APP_TOKEN, f"app.js?v={versions['app']}")
    return versions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()

    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing snapshot: {output}")

    subprocess.run(["python3", str(ROOT / "scripts" / "build_snapshot.py")], cwd=ROOT, check=True)
    generated = ROOT / "site"
    output.mkdir(parents=True)
    for name in ("index.html", "app.js", "styles.css"):
        shutil.copy2(generated / name, output / name)
    public_data = output / "data"
    public_data.mkdir()
    shutil.copy2(generated / "data" / "index.json", public_data / "index.json")
    shutil.copy2(generated / "data" / "resources.json", public_data / "resources.json")
    shutil.copytree(generated / "data" / "benchmarks", public_data / "benchmarks")
    # The destination repository currently validates this historical filename.
    # Keep it as a small index alias; the 25 MB monolithic detail payload is not
    # published and the frontend never fetches this compatibility file.
    shutil.copy2(generated / "data" / "index.json", public_data / "benchmarks.json")
    assets = generated / "assets"
    if assets.exists():
        shutil.copytree(assets, output / "assets")

    asset_versions = stamp_cache_versions(output)

    benchmarks = json.loads((output / "data" / "index.json").read_text())
    manifest = {
        "project": "BLE",
        "source_repository": "https://github.com/yuema137/benchs-last-exam",
        "source_sha": args.source_sha,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_date": benchmarks["snapshot_id"],
        "benchmark_count": len(benchmarks["benchmarks"]),
        "schema_version": benchmarks["schema_version"],
        "asset_versions": asset_versions,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built BLE snapshot at {output} ({manifest['benchmark_count']} benchmarks)")


if __name__ == "__main__":
    main()
