from __future__ import annotations

import csv
import json
from pathlib import Path

from nextgen2026_coding_bootcamp.engine_runner import run_once

QUANTILES = [0.80, 0.85, 0.90, 0.95]


def _read_manifest(run_dir: Path) -> dict:
    return json.loads((run_dir / "manifest.json").read_text())


def main() -> int:
    rows: list[dict] = []

    print(f"Starting sweep across {len(QUANTILES)} quantiles...")

    for q in QUANTILES:
        # Use run_once adapter for consistent execution contract
        run_dir = run_once(
            profile="base",
            overrides=[f"analysis.high_demand_quantile={q}"],
            run_name=f"sweep-q{int(q * 100)}",
        )

        manifest = _read_manifest(run_dir)
        prepare = manifest.get("artifacts", {}).get("prepare", {})
        analyze = manifest.get("artifacts", {}).get("analyze", {})

        rows.append(
            {
                "run_id": manifest.get("run_id", run_dir.name),
                "quantile": q,
                "threshold": analyze.get("threshold"),
                "rows_processed": prepare.get("rows_out"),
                "run_dir": str(run_dir),
            }
        )
        print(f"  Completed q={q} -> threshold={analyze.get('threshold'):.2f}")

    # Generate the local summary index
    summary_dir = Path("runs") / "summaries"
    summary_dir.mkdir(parents=True, exist_ok=True)
    summary_path = summary_dir / "quantile_sweep.csv"

    with summary_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["run_id", "quantile", "threshold", "rows_processed", "run_dir"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSweep complete. Summary index written to: {summary_path}")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
