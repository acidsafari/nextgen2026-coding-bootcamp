# 🧬 Advanced Research Workflow Template

This repository is a standardized template for reproducible research and data analytics projects at scale. It extends the core **"Engine vs. Wrapper"** architecture with specialized tools for experiment tracking, orchestration, and complex configuration management.

---

## 🚀 Advanced Features

### 1. Experiment Tracking (MLflow)
Integrated dashboard for comparing parameters, metrics, and artifacts across runs.
- View UI: `uv run mlflow ui`

### 2. Workflow Orchestration (Prefect)
Support for managed runs, retries, and asynchronous execution visibility.
- Demo: `uv run python scripts/prefect_engine_runs.py`

### 3. Advanced Configuration (Hydra)
Standardized override ergonomics and native support for multirun parameter sweeps.
- Sweep: `uv run python scripts/hydra_workflow.py --multirun analysis.threshold=0.85,0.90`

---

## 🚀 Quick Start Onboarding

### 1. Prerequisites
- **Python 3.11+**
- **uv** (Recommended for environment management):
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 2. Environment Setup
Initialize the virtual environment and install dependencies:
```bash
# Create .venv and install dependencies from pyproject.toml
uv sync
```

### 3. Run the Canonical Pipeline
To verify the environment, run the orchestrated workflow:
```bash
uv run python scripts/run_workflow.py --profile base --run-name initial-test
```

---

## 🏗️ Architectural Patterns

### 1. The "Engine vs. Wrapper" Pattern
- **The Engine (`src/`)**: Reusable scientific logic.
- **The Ignition (`scripts/`)**: Thin entry points for CLI and Engine execution.

### 2. Composed Configuration
Small, focused YAML files (`run.yaml`, `paths.yaml`, `stages/*.yaml`) merged at runtime.

---

## 🧪 Experiment Management: The Branching Method
Follow the **"Branching Out"** method: create a branch for each hypothesis, commit your config overrides, and save your results directly to that branch for side-by-side comparison.

---

## 🤖 Working with AI Coding Agents
This project is optimized for AI-assisted development. Please refer to **[AGENTS.md](./AGENTS.md)** for session synchronization and architectural safety rules.

---

## 🔗 Other Templates
- **[Basic Research Template](https://github.com/acidsafari/research-template-basic)**
- **Advanced Research Template** (Current)
