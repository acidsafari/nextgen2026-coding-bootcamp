# Research Workflow Guide

This guide is a research-workflow path rather than a feature catalog. Each chapter introduces one reproducibility capability, explains its methodological purpose, and leaves a runnable checkpoint that makes progress observable.

The sequence is intentionally cumulative: structural boundaries, explicit configuration, stable invocation, durable evidence, traceable runs, orchestration, and tests are introduced in dependency order. Following that order helps build workflows that are easier to interpret, compare, review, and defend.

## 1. Core Path

Use the core path to establish the minimum contract for auditable runs. These chapters are the required baseline before adding scale or platform tooling.

1. [Project Structure](./01-project-structure.md): isolate reusable analysis logic from execution wrappers.
2. [Configuration](./02-config.md): make analysis behavior explicit through hierarchical config.
3. [Command-Line Interface](./03-cli.md): standardize stage invocation and override surface.
4. [Logging and Observability](./04-observability.md): capture durable process evidence.
5. [Traceable Runs](./05-traceability.md): create one run record per execution.
6. [Workflow Orchestration](./06-orchestration.md): run all stages through one canonical command.
7. [Testing the Workflow](./07-testing.md): protect behavior and provenance with automated tests.

## 2. Appendices

Appendices extend the core contract for scale, collaboration, and orchestration ergonomics. They should be treated as optional accelerators, not substitutes for core controls.

8. [Experiment Tracking](./08-appendix-experiment-tracking.md): index runs in an experiment tracker.
9. [Workflow Engines](./09-appendix-workflow-engines.md): add scheduler/engine control without changing method logic.
10. [Multiruns](./10-appendix-multiruns.md): run and compare parameter sweeps.
11. [Hydra](./11-appendix-hydra.md): migrate config UX and multiruns to Hydra.
12. [Automated Testing on Git Push](./12-appendix-git-push-testing.md): enforce a deterministic push gate.

## 3. Reading Conventions

These conventions keep pedagogical intent explicit and reduce confusion between “teaching snapshot” and “final repository state.”

- Examples are chapter snapshots intended for learning progression.
- Commands are intentionally minimal and executable from repo root.
- Rationale is research-first: each change should reduce method ambiguity or provenance risk.
