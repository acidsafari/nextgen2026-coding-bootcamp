from __future__ import annotations

from pathlib import Path
import subprocess

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


def _git_commit() -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], check=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    commit = result.stdout.strip()
    return commit or None


def run_once(
    *,
    profile: str = "base",
    overrides: list[str] | None = None,
    extra_parts: list[str] | None = None,
    run_name: str | None = None,
    log_level: str = "INFO",
    config_root: Path = Path("configs"),
    on_stage_finish=None,
) -> Path:
    """Reusable entry point for executing a single full workflow run."""
    parts = [*DEFAULT_PARTS, f"profiles/{profile}.yaml", *(extra_parts or [])]
    cfg = compose_config(config_root=config_root, parts=parts, overrides=overrides)

    ctx = create_run_context(Path(cfg.run.output_root), run_name=run_name)
    configure_logging(ctx.run_dir / "run.log", level=log_level)
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    run_workflow(cfg=cfg, ctx=ctx, on_stage_finish=on_stage_finish)
    write_manifest(ctx=ctx, git_commit=_git_commit())
    return ctx.run_dir
