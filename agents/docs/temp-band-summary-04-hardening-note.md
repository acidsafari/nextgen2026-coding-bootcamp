# 04 Hardening Note

## Session Reference

- Task: Temperature-Band Summary (`feat/temp-band-summary`)
- Review and decision reference: `agents/docs/temp-band-summary-03-review-and-decision.md`

## Durable Instructions to Move Into `AGENTS.md`

- **Verify column names between stages**: Remind the agent to check for column renaming (e.g., `temp` to `temp_c`) when crossing stage boundaries like `prepare` -> `analyze`.
- **Observed Categories in Groupby**: When using `pd.cut` with categorical labels, set `observed=True` in `groupby` to avoid empty rows for labels without observations.

## Checks to Automate

- **Automated Regression Artifact Diff**: Add a test or utility that automatically compares key CSV outputs against a "baseline" run to detect unintended shifts in existing analysis logic.

## Reusable Prompt or Template Patterns

- **Visual Context Map**: The Mermaid diagram approach in `SESSION_CONTEXT.md` worked well for tracking risk and stage boundaries. This pattern should be reused for future tasks.

## One Concrete Improvement Action

- Update `AGENTS.md` with a rule about verifying schema changes between stages to prevent `KeyError` regressions.

## Approval

- Reviewer: User
- Status: Approved
