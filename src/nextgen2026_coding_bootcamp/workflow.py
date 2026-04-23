from collections.abc import Callable

from nextgen2026_coding_bootcamp.steps.fetch import run_fetch
from nextgen2026_coding_bootcamp.steps.prepare import run_prepare
from nextgen2026_coding_bootcamp.steps.analyze import run_analyze
from nextgen2026_coding_bootcamp.steps.report import run_report

StageCallback = Callable[[str, dict], None]


def run_workflow(cfg, ctx, on_stage_finish: StageCallback | None = None):
    stage_plan = [
        ("fetch", run_fetch),
        ("prepare", run_prepare),
        ("analyze", run_analyze),
        ("report", run_report),
    ]

    for stage_name, stage_fn in stage_plan:
        artifact = stage_fn(cfg=cfg, ctx=ctx)
        ctx.artifacts[stage_name] = artifact
        if on_stage_finish is not None:
            on_stage_finish(stage_name, artifact)
    return ctx
