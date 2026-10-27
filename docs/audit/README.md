# Audit register: scientific-regression-demo

Read this before repeating old reviews. These documents freeze the **software/tutorial lane**; this repository is not the separate JEPA research and training project.

Start with [historical audit](HISTORICAL_AUDIT_20261027.md), [defect register](DEFECT_REGISTER.csv), [artifact custody](ARTIFACT_CUSTODY.md), [pre-repository negative](PRE_REPO_NEGATIVE.md), and [guardrails](GUARDRAILS.md). The machine-readable [baseline](BASELINE_20261027.json) records original exact Git blobs, PR heads, and successful CI run IDs. It is a dated snapshot, not a claim that future main is unchanged.

**Audit entrypoint at 2026-10-27:** `1c5c52fd9ca61c6314ce35143db1a02431f40d27`, PRs #1–#6 merged, local full suite 22 passed, deliberate RED 6 failed/4 passed, GREEN 10 passed. Distinguish RED working as designed from a genuine CI failure.

After these records, go to [takeover handoff](../handoff/README.md) once that branch is published. Do not inspect unrelated JEPA dataset/checkpoint archives to work on this public educational repo.
