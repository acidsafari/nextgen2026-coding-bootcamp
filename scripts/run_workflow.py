import argparse
from pathlib import Path

import mlflow
from omegaconf import OmegaConf

from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.manifests import write_manifest
from nextgen2026_coding_bootcamp.runtime import create_run_context, configure_logging
from nextgen2026_coding_bootcamp.workflow import run_workflow

DEFAULT_PARTS = [
    "run.yaml",
    "paths.yaml",
    "stages/fetch.yaml",
    "stages/prepare.yaml",
    "stages/analyze.yaml",
    "stages/report.yaml",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full workflow.")
    parser.add_argument("--profile", type=str, default="base")
    parser.add_argument("--part", action="append", default=[])
    parser.add_argument("--set", nargs="*", default=[], metavar="KEY=VALUE")
    parser.add_argument("--log-level", type=str, default="INFO")
    parser.add_argument("--run-name", type=str, default=None)
    parser.add_argument("--experiment", type=str, default="bike-sharing-baseline")
    args = parser.parse_args()

    parts = [*DEFAULT_PARTS, f"profiles/{args.profile}.yaml", *args.part]
    cfg = compose_config(Path("configs"), parts=parts, overrides=args.set)

    ctx = create_run_context(Path(cfg.run.output_root), run_name=args.run_name)
    configure_logging(ctx.run_dir / "run.log", level=args.log_level)
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    # Tracking integration
    mlflow.set_experiment(args.experiment)
    with mlflow.start_run(run_name=ctx.run_id):
        # Log all config as parameters (flattened)
        mlflow.log_params(OmegaConf.to_container(cfg, resolve=True))
        mlflow.set_tag("local_run_dir", str(ctx.run_dir))

        def on_stage_finish(stage_name: str, artifact: dict):
            # Log specific numeric metrics if present in artifact
            if stage_name == "prepare" and "rows_out" in artifact:
                mlflow.log_metric("prepare.rows_out", artifact["rows_out"])
            if stage_name == "analyze" and "threshold" in artifact:
                mlflow.log_metric("analyze.threshold", artifact["threshold"])
            if stage_name == "analyze" and "rows_in" in artifact:
                mlflow.log_metric("analyze.rows_in", artifact["rows_in"])

        run_workflow(cfg=cfg, ctx=ctx, on_stage_finish=on_stage_finish)
        write_manifest(ctx=ctx)

        # Log the manifest and config as artifacts in MLflow too
        mlflow.log_artifact(str(ctx.run_dir / "config.yaml"))
        mlflow.log_artifact(str(ctx.run_dir / "manifest.json"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
