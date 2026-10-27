# Medium publication readiness — 27 October 2026

This is a prospective editorial verification of the **public tutorial repository**, not the separate JEPA research lane and not an assertion of independent biological validation.

## Version and evidence

- Verified baseline: `main` at `540143af6b49c1177d2de99aba0d0e9768a10ce2`.
- Hosted [GitHub Actions run 40537406640](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40537406640) completed successfully on that exact commit on 27 October 2026.
- The workflow ran the beginner examples, deterministic CSV generator, RNA reader, full pytest suite, historical audit validator, deliberate RED/GREEN wrapper, and figure producer.
- The log explicitly reports **24 passed** for the complete suite; **RED 4 passed / 6 failed / 0 errors** (intentional), **GREEN 10 passed / 0 failed / 0 errors**; **4 PNG + 4 SVG** figures generated.
- The included example has 6 donors, 12 cells, 36 gene-by-cell rows; study_b/gene_3 has 6 unassayed records, not measured zeros.
- The canonical medium draft is [MEDIUM_ARTICLE.md](../../MEDIUM_ARTICLE.md), not an old exported teaching kit. The README and manuscript full-suite references were reconciled with the current hosted count in this publication branch. The historical audit's 22-test starting count remains unchanged as historical evidence.

## Scientific and code-review disposition

- The three explicit teaching contracts in `science_rules.py` match the narrative and tests: assay support differs from count zero; repeated observations do not create additional donor identifiers; missing required status cannot become PASS under the chosen illustrative decision policy.
- The separate **2-donor/1,000-row** example does not describe the **6-donor RNA CSV**. Merely counting distinct donor IDs is not a statistical test of biological independence.
- The RED/GREEN counts are parsed from JUnit testcase reports, not hand-entered into the result chart. These checks establish behavior under specified tests, not correctness of an untested biological analysis.
- The four referenced PNG paths and the manuscript's Figure 1–4 sequence are consistent with the code paths reviewed. The repo has asset-integrity tests, but programmatic validation cannot certify legibility in Medium's live desktop/mobile presentation.

## Editorial pre-publication checklist

- [ ] Import or paste the **current** `MEDIUM_ARTICLE.md` into Medium; confirm headings, emphasis, Unicode arrows, code indentation/fences, and tables survive conversion. Recreate tables manually if Medium does not preserve Markdown tables.
- [ ] Insert the four final PNGs at their intended locations, in this article order (which differs from source filename order): Figure 1 `figure_1_rna_measurements_v2.png`; Figure 2 `figure_4_donor_units_v2.png`; Figure 3 `figure_2_test_results_v2.png`; Figure 4 `figure_3_regression_workflow_v2.png`.
- [ ] Check that all four captions and alt descriptions match their images; inspect gene/cell labels on narrow/mobile and desktop widths. Use PNGs for Medium; SVGs are source-quality alternatives.
- [ ] Check code samples are readable and copyable, including `None`, `True`, `False`, and `NOT_ESTIMABLE`. Confirm that external GitHub links and cited workflow links open.
- [ ] Add a Medium publication date and final canonical URL **only after the article is actually published**. A GitHub Markdown file is not a Medium publication.
- [ ] If promoting on LinkedIn, link the **verified Medium URL** and the repository, not an unverified placeholder. Retain the scientific caveat that the dataset is illustrative.
- [ ] For citation, identify the exact source revision used. `CITATION.cff` provides software citation metadata; no DOI is currently established.

## Remaining qualification limits

- A successful hosted CI workflow proves the configured steps executed on the checked Git revision, not that an independent newcomer completed setup. A separate novice usability trial remains open.
- Local independent `git clone` in this takeover environment was blocked by DNS resolution of github.com; do **not** claim a fresh local end-to-end test. The exact-head hosted CI run above supplies execution evidence.
- Medium editor preview, live published desktop/mobile visuals, external posting, and a published article URL are **not verified** here.
- This review makes **no changes** to teaching implementations, datasets, tests, outputs, or figures. Historical audits and closed defects remain untouched.

## Post-takeover publication source reconciliation

On 27 October 2026, [PR #10](https://github.com/dushyant-mishra/scientific-regression-demo/pull/10) merged a prospective, separately falsified CSV reader consistency test. The new [main CI run 40553329081](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40553329081) succeeded on commit `75ecd86cec470843b5352f80ef1a67d92f89eba3`: **25 total tests passed**, while the unchanged ten-test teaching demonstration remains RED 4 passed/6 failed and GREEN 10 passed. The original 24-test result above is retained as a dated baseline; it was not fabricated or erased.

The canonical article and README now cite the 25-test run. The manuscript was also corrected to say the two-donor example **repeats identifiers** and does not actually perform resampling. This correction does not alter the stored RNA CSV, test figures, or scientific claim limits.

**Remaining external acceptance checks:** independently observed novice setup on another environment; actual Medium editor formatting and live desktop/mobile image readability; user-authorized Medium publication and final URL. Do not mark these complete from hosted CI alone.

## Prospective beginner-readability corrections — 27 October 2026

A fresh reviewer-read of the current tutorial identified two **presentation** shortcomings, distinct from previously closed software bugs: a biologist new to terminals or GitHub lacked an executable start-to-finish exercise, and the old figure_4 v2 labeled constructed identifiers as resamples/independent donors. These did not invalidate the existing toy rule logic, but they limited beginner reproducibility and over-described the donor plot.

The article now introduces Python/terminal and ZIP setup before first use, then supplies a complete standalone `tests/test_my_first_rule.py` example with a one-line intentional error and exact **1 passed → 1 failed → 1 passed** exercise, followed by browser-only fork/branch/Actions steps that explicitly prevent sending a deliberately broken PR to the original upstream repository. A local isolated run of this single-test exercise observed that sequence. This is not a substitute for an independent human first-time reader test.

Figure 2 in the manuscript now uses `figures/figure_4_donor_units_v3.png`, generated by the canonical `make_figures.py` and accompanied by an SVG with selectable text. It correctly compares **1,000 repeated row labels** with **two distinct donor IDs**, not completed resampling or statistically proven donor independence. Historical v2 PNG/SVG remain tracked because `scripts/validate_lane_audit.py` requires them as frozen historical artifacts; they are not current publication images. A new figure-integrity test guards the v3 labels.

[Branch CI run 40559192830](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40559192830) passed on `d7fe0aa5591789abb06b69eca6de973b03749c65`: **26 repository tests passed**, the audit validator passed, RED 4 passed/6 failed, GREEN 10 passed, and all four PNG/SVG figure pairs regenerated. The article's earlier citation of 25 tests refers to a dated previous main commit and remains a true historical result.

**External limitations unchanged:** No real first-time human completed this workflow during takeover; there is no verified Medium editor preview, publication, URL, or DOI.
