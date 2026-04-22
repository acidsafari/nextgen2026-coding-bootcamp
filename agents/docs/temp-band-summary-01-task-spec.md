# 01 Task Spec

## Task Summary

- Request: Add a temperature-band demand summary in `analyze` and surface it in `report`.
- Intended repo change: Modify `src/nextgen2026_coding_bootcamp/steps/analyze.py` to bin temperature data and calculate mean rentals per band. Modify `src/nextgen2026_coding_bootcamp/steps/report.py` to include this summary in the Markdown report and potentially a plot.
- Why this task is appropriate for delegation: It is a bounded analytical extension that crosses a stage boundary (analyze -> report) without changing core data transformations in `prepare`. It produces a measurable new output.

## Risk and Review Burden

- Technical debt risk: Low. It uses standard pandas operations.
- Interpretive risk: Medium. Need to decide on appropriate temperature bins (e.g., Cold, Mild, Warm, Hot).
- Verifiability: High. The new artifact can be checked for correctness against the input CSV.
- Blast radius: Low. It only adds new artifacts and report sections; it doesn't modify existing ones.
- Review burden: Low. The reviewer can check the generated CSV and the updated Markdown report.

## Likely Files and Surfaces

- Code or docs likely involved: 
    - `src/nextgen2026_coding_bootcamp/steps/analyze.py`
    - `src/nextgen2026_coding_bootcamp/steps/report.py`
- Tests or commands to inspect:
    - `uv run python scripts/run_workflow.py --profile base --run-name temp-band-check`
    - `tests/test_analyze.py` (if it exists or needs update)
- Existing artifacts or outputs to check:
    - `runs/<run_id>/analyze/temp_band_summary.csv` (new)
    - `runs/<run_id>/report/analysis_summary.md` (updated)

## Constraints and Non-Goals

- Constraints: Must use normalized `temp` column if following existing patterns, or denormalize if requested.
- Non-goals: Do not change the `prepare` stage or the `hourly_bike_data.csv` schema.
- What must not change: Existing hourly profiles and high-demand logic.

## Verification Plan

| Layer | Planned check | Repo surface or command | What it proves | What still needs your review |
| --- | --- | --- | --- | --- |
| Unit | Test binning logic in `analyze` | `pytest tests/test_analyze_report.py` | Bins are assigned correctly to expected labels | N/A |
| Regression | Compare baseline artifacts | `diff runs/baseline/analyze/hourly_profile.csv runs/temp-band/analyze/hourly_profile.csv` | Existing analysis is unchanged | N/A |
| Integration | Run stage handoff | `pytest tests/test_integration_stage_handoff.py` | `analyze` correctly consumes `prepare` output | N/A |
| End-to-end or smoke | Run full workflow smoke test | `pytest tests/test_workflow_smoke.py` | Artifact is produced and flows to report stage | N/A |
| Artifact or contract | Inspect `temp_band_summary.csv` | `head runs/latest/analyze/temp_band_summary.csv` | Correct columns (`temp_band`, `mean_rentals`) and reasonable values | Scientific plausibility |
| Your review | Inspect Markdown report | `cat runs/latest/report/analysis_summary.md` | Temperature bands are surfaced in the final summary | Visual formatting |

## Decision Threshold

- Accept when: 
    - `temp_band_summary.csv` is produced with bins [Cold, Cool, Mild, Warm, Hot].
    - `analysis_summary.md` contains a new section for Temperature Band analysis.
    - All existing tests pass and new coverage for temp bands is added to `test_analyze_report.py`.
- Revise when: 
    - Bins are inconsistent or mislabeled.
    - Report formatting is messy or hard to read.
- Reject when: 
    - Existing analysis (hourly profile, high demand) is altered or broken.
    - Stage boundaries are violated (e.g., binning logic put in `report` instead of `analyze`).

## Approval

- Reviewer: User
- Status: Approved
