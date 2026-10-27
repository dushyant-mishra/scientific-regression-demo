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
