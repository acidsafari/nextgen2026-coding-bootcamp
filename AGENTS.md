# Repository Instructions for Coding Agents

## Purpose
This repository provides a standardized, reproducible research workflow template with support for experiment tracking (MLflow), orchestration (Prefect), and complex configurations (Hydra).

## Canonical Commands
- Full test suite: `uv run pytest -q`
- Full workflow: `uv run python scripts/run_workflow.py --profile base --run-name local-run`
- Hydra workflow: `uv run python scripts/hydra_workflow.py`
- Prefect Demo: `uv run python scripts/prefect_engine_runs.py`

## Repository Map
- `src/<PROJECT_PACKAGE>/steps/`: stage logic
- `scripts/`: CLI wrappers and workflow runner
- `configs/`: run/path/stage/profile configuration
- `tests/`: regression and workflow checks
- `runs/`: run-scoped artifacts and manifests
- `docs/`: methodology guides and architectural patterns

---

## 1. Environment & Dependency Management
- **Tool**: Always use `uv` for environment management, package installation, and execution.
- **Lockfile**: Always keep `uv.lock` in sync with `pyproject.toml`.
- **Execution**: Use `uv run <command>` or `uv run python <script>` to ensure the project environment is used.

## 2. Code Organization (The "Thin Interface" Rule)
- **Source (`src/`)**: All durable, reusable logic must live in `src/<PROJECT_PACKAGE>/`.
- **Scripts (`scripts/`)**: Scripts should be "thin." They should handle CLI arguments and call functions from `src/`. Do not put core business/research logic in scripts.
- **Notebooks (`notebooks/`)**: Notebooks are for exploration and visualization. They must import project code from `src/` rather than redefining logic.

## 3. Data & Results Handling
- **Raw Data (`data/raw/`)**: Treat raw data as read-only. Never modify files in this directory.
- **Results (`results/`)**: All generated outputs must go into `results/`.
- **Traceability**: For all formal analysis runs, use the `run_id` pattern. Outputs must be stored in unique, timestamped directories under `runs/` to preserve provenance.

## 4. Version Control & Session Management
- **Experiment Management**: Use the **"Branching Out"** method for experiments. Create dedicated branches for hypothesis testing or parameter variants and commit both config snapshots and results to those branches.
- **Commits**: Make small, logical commits using Conventional Commits where possible.

## 5. Safety, Destructive Commands & Explainability
- **Destructive Commands**: Before running any destructive commands (e.g., `git clean -fd`), the agent **must**:
    1. Explain the reason for the command.
    2. Explain the meaning and impact.
    3. Request explicit permission.

---

## 6. Delegation & Review
- **Delegation Strategy**: Use one agent per bounded contract. Request a plan before implementation.
- **Review Requirements**: Every delegated change must include contract alignment, diff review, and test evidence.

