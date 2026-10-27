# Historical audit — 27 October 2026

## Scope and evidence
Repository: https://github.com/dushyant-mishra/scientific-regression-demo. Initial audit head: `1c5c52fd9ca61c6314ce35143db1a02431f40d27`. All six PRs #1–#6 were merged before this record. Each exact PR head has a **completed successful** GitHub Actions run; hashes and run IDs are in [BASELINE_20261027.json](BASELINE_20261027.json). Current source/data/results are already in Git; do **not** duplicate them in a new directory.

## Before the repository — independently detected error
The original local teaching kit ran pytest but placed **fixed** numbers in `run_demo.py`'s summary (3 passed/3 failed for buggy, 6/0 for repaired); `make_figures.py` also plotted literal arrays `passes=[3,6]`, `failures=[3,0]`. Those happened to match the first observed run but could conceal changes. In an adversarial mutation the **actual** buggy result was **4 failed, 2 passed** while the saved report continued to say **3 failed, 3 passed**. This is a preserved **historical negative**, not a defect of current `main`. See [PRE_REPO_NEGATIVE.md](PRE_REPO_NEGATIVE.md).

## PR ledger (exact-head CI success)
| PR | Exact reviewed head | Hosted run | Outcome and historical role |
|---|---|---|---|
| [#1](https://github.com/dushyant-mishra/scientific-regression-demo/pull/1) | `41312f9502cc79693da697345d64c943980fa3c9` | [40390858772](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40390858772) | Publish executable demo, artificial data, JUnit-derived RED/GREEN, article, citation, CI; report bug already repaired before initial PR. 17 local tests. |
| [#2](https://github.com/dushyant-mishra/scientific-regression-demo/pull/2) | `da746a14281a9a17d286ee34b48fcb2cc09e382f` | [40392934048](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40392934048) | Replace FIC-prefixed IDs with `gene_1`, `cell_01`, etc; simplify README; add consistency test. 18 local tests. |
| [#3](https://github.com/dushyant-mishra/scientific-regression-demo/pull/3) | `7cc66097ea199488c2bb8ad14db2f8e81dbe1eb4` | [40393565230](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40393565230) | Remove repetitive sample-data disclaimers and make prose natural. |
| [#4](https://github.com/dushyant-mishra/scientific-regression-demo/pull/4) | `df95c041a3e9f4de6309255dee50e558e54c4f17` | [40395501857](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40395501857) | Regenerate four PNG/SVG pairs, new filenames to avoid stale cached images; validate gene/cell labels and links. 21 local tests. |
| [#5](https://github.com/dushyant-mishra/scientific-regression-demo/pull/5) | `26354d7c6560e2cac616290623e3e7bda6f8b982` | [40396331791](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40396331791) | Remove irrelevant self-referential LLM editing story from reader article. |
| [#6](https://github.com/dushyant-mishra/scientific-regression-demo/pull/6) | `51315c7365e4c80b9008cf86f5504711a75202f4` | [40397918856](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40397918856) | Add `try_examples.py`, accessible code walkthrough and distinguish six-donor RNA CSV from **separate** two-donor, 1,000-row pseudoreplication illustration. 22 local tests. |

## What was established
- Current CSV has 2 studies × 3 donors × 2 cells × 3 genes = **36 gene-by-cell records**, 6 donors and 12 cells. Study B never assays `gene_3`: exactly six structurally unmeasured records, not zeros.
- Measured zero and unassayed count are distinct, rows cannot substitute for independent donors, and the example's predeclared `PASS/FAIL/NOT_ESTIMABLE` policy does not promote incomplete sources to PASS.
- Ten behavior tests are executed unchanged against deliberately broken `science_rules_buggy.py` and corrected `science_rules.py`: 4 pass/6 fail (RED); 10 pass/0 fail (GREEN). Hosted PR #6 checked the expanded **22-test** suite.
- The chart numbers are derived from executed JUnit testcase nodes via `junit_results.py`, not literal plotted expectations. Integrity tests cover misleading JUnit headers and modified plotted counts.
- Figures and links use refreshed v2 names; outdated figure URLs were removed. Current full tests include visual-asset structural checks.

## Limits and unresolved facts
- Neither the data nor the tests support differential-expression, disease, gene-regulation, donor-inference or real JEPA biological claims.
- `evidence_verdict` combines **assigned status labels**; it does not calculate statistical support.
- A green CI check shows the defined tests ran on a specified revision; it does not prove test completeness, biology, independently accepted scientific results, active branch protection, or a Medium publication.
- Reader testing and external usability review have **not** been performed. No DOI or Zenodo release has been claimed.
- Pre-repository ZIPs were generated before #1. They are **superseded** and are not needed to execute the current repo; Git PR history is canonical for changes after #1.

**Audit disposition:** Preserve history, do not reopen closed work without fresh reproducible evidence. The agent may propose new improvements on a separate branch.
