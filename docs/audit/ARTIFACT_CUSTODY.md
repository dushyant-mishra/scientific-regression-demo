# Artifact/source custody — no re-creation needed

Use exact Git blob identities in [BASELINE_20261027.json](BASELINE_20261027.json) to retrieve historical bytes from baseline commit `1c5c52fd9ca61c6314ce35143db1a02431f40d27`. Full history and old versions are accessible via merged PRs #1–#6; **do not duplicate code/data/figures as additional canonical copies**.

| Authoritative current path | Role |
|---|---|
| `data/fictional_rna_observations.csv`, `generate_fictional_data.py` | Deterministic sample producer/data. |
| `analyze_fictional_rna.py`, `outputs/analysis_summary.json`, `outputs/fictional_summary.csv` | Assay classification and data summaries. |
| `try_examples.py`, `science_rules.py`, `science_rules_buggy.py` | Beginner walkthrough, current rule logic, intentional RED comparator. |
| `tests/test_science_rules.py`, `tests/test_beginner_walkthrough.py`, `tests/test_data_integration.py` | 10 behavior tests + first-run and CSV integration checks. |
| `tests/test_reporting_integrity.py`, `tests/test_figure_integrity.py` | Report and figure corruption/identity guards. |
| `run_demo.py`, `junit_results.py`, `make_figures.py` | Exact RED/GREEN execution and figure generation. |
| `outputs/red_pytest.xml`, `outputs/green_pytest.xml`, `outputs/red_run.txt`, `outputs/green_run.txt`, `outputs/results.json` | **Saved local** test evidence. Parse actual cases and check source/report digests. |
| `figures/figure_1_rna_measurements_v2.*` through `figure_4_donor_units_v2.*` | Current four PNG/SVG publication image pairs. |
| `MEDIUM_ARTICLE.md`, `README.md`, `CITATION.cff`, `LICENSE` | Canonical manuscript, instructions, software citation and MIT license. |
| `.github/workflows/scientific-regressions.yml` | Hosted CI. The PR #6 run ID is 40397918856 and completed successfully at its **exact head**. |

Old pre-repo local files were identified in the originating conversation; only the salient original defect has been recorded in this audit. They are intentionally not re-added as executable code to GitHub. User-provided large JEPA checkpoints/foundation/expression archives are unrelated and must not enter this public tutorial repository.

**Semantic separation:** 6-donor RNA CSV is not the 2-donor/1,000-row pseudoreplication check. `NOT_ESTIMABLE` is a chosen status label, not a measured biological outcome.
