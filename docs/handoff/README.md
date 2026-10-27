# Agent takeover: scientific-regression-demo

This is the durable entrypoint for a successor agent. **Do not restart the completed six-PR audit.** The separate historical record has been frozen and tested.

Read in this order:

1. [Takeover memorandum](TAKEOVER_20261027.md) — source, purposes, trusted evidence, completed work, restrictions and state.
2. [Execution playbook](EXECUTION_PLAYBOOK.md) — executable commands, expected outputs, what failures mean, source/result graph.
3. [Pending work](PENDING_WORK.md) — what genuinely remains open versus what was closed.
4. [Publishing/citation checklist](PUBLICATION_CHECKLIST.md) — next reader-facing step, no invented DOI.
5. [Agent assignment](SUCCESSOR_AGENT_INSTRUCTIONS.md) — reusable instructions for another coding or audit agent.
6. [Machine-readable custody](ACTIVE_STATE.json) — unambiguous SHA, CI and artifact referents.

Historical records: [audit index](../audit/README.md), [exact baseline](../audit/BASELINE_20261027.json), [PR audit chronology](../audit/HISTORICAL_AUDIT_20261027.md), [defect register](../audit/DEFECT_REGISTER.csv).

This handoff is documentation/custody. The runnable project stays in root paths; no shadow copy of scripts, data, results or figures was created.

**Immediate workflow:** inspect current main SHA and current CI, read historical audit, run `python try_examples.py`, `python -m pytest -q`, `python run_demo.py`, `python make_figures.py`, review actual outputs, then perform only an authorized new task on a dedicated branch.

The tutorial has no asserted real biological discovery or completed Medium publication. 
