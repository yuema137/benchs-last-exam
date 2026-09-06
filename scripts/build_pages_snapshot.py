#!/usr/bin/env python3
"""Build the self-contained static bundle published under /ble/."""

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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

    benchmarks = json.loads((output / "data" / "index.json").read_text())
    manifest = {
        "project": "BLE",
        "source_repository": "https://github.com/yuema137/benchs-last-exam",
        "source_sha": args.source_sha,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_date": benchmarks["snapshot_id"],
        "benchmark_count": len(benchmarks["benchmarks"]),
        "schema_version": benchmarks["schema_version"],
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built BLE snapshot at {output} ({manifest['benchmark_count']} benchmarks)")


if __name__ == "__main__":
    main()
