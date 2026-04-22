# 02 Agent Brief

## Approved Objective

- Task spec reference: `agents/docs/temp-band-summary-01-task-spec.md`
- Objective: Implement temperature-band demand summary in the `analyze` stage and surface it in the `report` stage.

## Bounded Scope

- In scope:
    - Binning `temp` column into [Cold, Cool, Mild, Warm, Hot] in `analyze.py`.
    - Calculating `mean_rentals` for each temperature band.
    - Exporting `temp_band_summary.csv` in `analyze` stage.
    - Including the temperature band summary in `analysis_summary.md` in `report` stage.
    - Updating `tests/test_analyze_report.py` to cover new outputs.
- Out of scope:
    - Modifying `prepare` stage.
    - Changing `hour.csv` schema.
    - Implementing new plots (unless requested later).
    - Changing existing analysis logic.

## Durable Instructions

- Repo rules to keep front-of-mind:
    - Use `uv run` for all commands.
    - Reusable logic in `src/`, thin interfaces in `scripts/`.
    - Outputs must go into `runs/` (traceability).
    - Do not use hardcoded absolute paths.
    - Use type hints and docstrings.

## Minimal Context Bundle

- `src/nextgen2026_coding_bootcamp/steps/analyze.py`: Implementation of analysis logic.
- `src/nextgen2026_coding_bootcamp/steps/report.py`: Implementation of reporting logic.
- `tests/test_analyze_report.py`: Baseline tests for verification.
- `configs/stages/analyze.yaml`: Analysis configuration.

## First Handoff Message

Please implement the temperature-band demand summary as specified in the Task Spec (`agents/docs/temp-band-summary-01-task-spec.md`).

Instructions:
1. Inspect `src/nextgen2026_coding_bootcamp/steps/analyze.py` and `src/nextgen2026_coding_bootcamp/steps/report.py`.
2. Propose a short plan that bins normalized temperature into [Cold, Cool, Mild, Warm, Hot] bands (0.2 increments) in `analyze.py`, exports a new CSV artifact, and surfaces it in the `report.py` Markdown output.
3. Update `tests/test_analyze_report.py` to verify the new outputs.
4. Do not implement any code until the plan is reviewed.

## Required Return Format

- Restated task:
- Files inspected:
- Files likely to change:
- Short plan:
- Verification commands:
- Changed files:
- Checks run:
- Assumptions or open questions:
- Hold for approval confirmation:

## Stop and Escalate Conditions

- Stage boundary is unclear: If binning logic seems to belong better in `prepare`, escalate.
- Wider file scope is needed: If files outside `src/` or `tests/` need changes, escalate.
- Workflow entrypoints or CLI behavior would change: Escalate.
- Scientific meaning may change beyond the approved task spec: If the normalized `temp` binning thresholds are questionable, escalate.

## Approval

- Reviewer: User
- Status: Approved
