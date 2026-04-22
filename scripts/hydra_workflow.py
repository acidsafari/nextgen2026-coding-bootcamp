from __future__ import annotations

from pathlib import Path

import hydra
import mlflow
from omegaconf import DictConfig, OmegaConf

from nextgen2026_coding_bootcamp.manifests import write_manifest
from nextgen2026_coding_bootcamp.runtime import create_run_context, configure_logging
from nextgen2026_coding_bootcamp.workflow import run_workflow


@hydra.main(version_base=None, config_path="../configs", config_name="hydra_workflow")
def main(cfg: DictConfig) -> None:
    # 1. Setup local run context and logging
    ctx = create_run_context(Path(cfg.run.output_root), run_name=str(cfg.run_name))
    configure_logging(ctx.run_dir / "run.log", level=str(cfg.log_level))
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    # 2. Tracking integration (MLflow)
    mlflow.set_experiment(str(cfg.get("experiment", "bike-sharing-hydra")))

    with mlflow.start_run(run_name=ctx.run_id):
        # Log all config as parameters
        mlflow.log_params(OmegaConf.to_container(cfg, resolve=True))
        mlflow.set_tag("local_run_dir", str(ctx.run_dir))
        mlflow.set_tag("engine", "hydra")

        def tracking_callback(stage_name: str, artifact: dict):
            if stage_name == "prepare" and "rows_out" in artifact:
                mlflow.log_metric("prepare.rows_out", artifact["rows_out"])
            if stage_name == "analyze" and "threshold" in artifact:
                mlflow.log_metric("analyze.threshold", artifact["threshold"])

        # 3. Execute workflow
        run_workflow(cfg=cfg, ctx=ctx, on_stage_finish=tracking_callback)
        write_manifest(ctx=ctx)

        # 4. Finalize tracking artifacts
        mlflow.log_artifact(str(ctx.run_dir / "config.yaml"))
        mlflow.log_artifact(str(ctx.run_dir / "manifest.json"))


if __name__ == "__main__":
    main()
