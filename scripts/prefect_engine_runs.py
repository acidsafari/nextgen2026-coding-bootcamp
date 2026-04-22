import argparse
from pathlib import Path
import mlflow
from omegaconf import OmegaConf
from prefect import flow, task
from nextgen2026_coding_bootcamp.engine_runner import run_once


@task(retries=2, retry_delay_seconds=5)
def orchestrated_run_task(
    profile: str, run_name: str, overrides: list[str] | None = None
):
    """Prefect task that wraps a single workflow execution."""

    # Optional: Integrate MLflow tracking within the task
    mlflow.set_experiment("bike-sharing-prefect")

    # Create a tracking callback for MLflow
    def tracking_callback(stage_name, artifact):
        if stage_name == "prepare" and "rows_out" in artifact:
            mlflow.log_metric("prepare.rows_out", artifact["rows_out"])
        if stage_name == "analyze" and "threshold" in artifact:
            mlflow.log_metric("analyze.threshold", artifact["threshold"])

    with mlflow.start_run(run_name=f"prefect-{run_name}"):
        run_dir = run_once(
            profile=profile,
            run_name=run_name,
            overrides=overrides,
            on_stage_finish=tracking_callback,
        )
        mlflow.set_tag("local_run_dir", str(run_dir))
        return str(run_dir)


@flow(name="Bike Sharing Sensitivity Sweep")
def sensitivity_sweep_flow(quantiles: list[float]):
    """Prefect flow that runs multiple orchestrated runs in parallel (or sequence)."""
    results = []
    for q in quantiles:
        run_name = f"q-{int(q * 100)}"
        overrides = [f"analysis.high_demand_quantile={q}"]
        res = orchestrated_run_task(
            profile="base", run_name=run_name, overrides=overrides
        )
        results.append(res)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quantiles", type=float, nargs="+", default=[0.9, 0.95, 0.99])
    args = parser.parse_args()

    sensitivity_sweep_flow(quantiles=args.quantiles)
