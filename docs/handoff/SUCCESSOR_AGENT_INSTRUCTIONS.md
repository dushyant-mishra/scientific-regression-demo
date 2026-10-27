# Paste-ready takeover instruction for a new coding/review agent

You are taking custody of the **scientific-regression-demo** tutorial lane (https://github.com/dushyant-mishra/scientific-regression-demo), not the JEPA target-discovery research lane.

1. Start from **current** `main`, capture its exact SHA and current GitHub Actions result. Audit handoff starting commit was `a5dd0292d2fec1d3bc50878c566fc486f0f100bc`; do not assume that is today's head.
2. Read `docs/audit/README.md`, `docs/audit/HISTORICAL_AUDIT_20261027.md`, `docs/audit/DEFECT_REGISTER.csv`, `docs/audit/BASELINE_20261027.json`, and `docs/handoff/TAKEOVER_20261027.md`. Treat PRs #1–#7 and their exact-head success evidence as already audited. Do not redo them absent a **new** exact-head defect.
3. Inspect README, Medium draft, science_rules, intentionally buggy module, data generator, reader, tests, output receipts, scripts, four PNG/SVG pairs, CITATION.cff and workflow. Use exact current Git paths; do not rebuild equivalent copies.
4. Run `python try_examples.py`, `python -m pytest -q`, `python scripts/validate_lane_audit.py`, `python run_demo.py`, `python make_figures.py`; reconcile output counts and source/report hashes. RED is intentionally failing; GREEN must pass. Check any CI discrepancy.
5. Preserve every closed outcome. The original fixed-figure bug was **pre-repo** and repaired by #1, not a current vulnerability. The gene/cell names, 6 vs 2 donor distinction, four figures, prose revisions and accessible code walkthrough were settled in #2–#6.
6. Restrict claims to educational software behavior; no real biological or JEPA validation, independent donor statistical proof, published Medium URL, or registered DOI is established.
7. Check `docs/handoff/PENDING_WORK.md`. Current meaningful open work is external Medium publication/usability verification, optional future citation archival and prospective fixes for *new* defects. Do not use an open task as license to rewrite the science or run unrelated historical audits.
8. For new changes, first state the scientific/software contract and acceptance conditions; write negative tests before repair when appropriate. Use isolated PRs, exact-head CI, report source/data/figure changes, compare old vs new output, and request independent review for consequential changes.
9. Keep the README natural and beginner-friendly; no repetitive artificial-data disclaimers or LLM editing anecdotes. Make article code match real source. Inspect images visually.
10. Return a custody update with: exact repo+SHA, tests and GitHub run IDs, changed paths, any new defects, whether publication actually occurred, and open/closed action register.

If access to GitHub or external publishing is blocked, state the precise blocker and give only verified outputs. **No background promises.**
