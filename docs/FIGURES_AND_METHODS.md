# Figures: scientific meaning and reproducible generation

The figures in this repository illustrate **RNA measurement semantics, software-test outcomes, donor-ID accounting, and the regression-testing workflow**. They use fictional input data; they are not microscopy images, statistical estimates of biological effects, or findings from a real RNA study.

## Figures and their source data

| Figure | Data source | Scientific interpretation |
| --- | --- | --- |
| [RNA measurement matrix](../figures/figure_1_rna_measurements_v2.png) | [Fictional RNA observations](../data/fictional_rna_observations.csv) | A plus sign means RNA detected, `0` means an assay returned zero detected molecules, and a dash means the gene was **not assayed**. Study B never assayed `gene_3`. |
| [RED/GREEN regression checks](../figures/figure_2_test_results_v2.png) | [Recorded test results](../outputs/results.json) | The deliberately incorrect source fails six of the ten unchanged behavior tests; the repaired source passes all ten. These are software outcomes, not biological effect estimates. |
| [Scientific regression workflow](../figures/figure_3_regression_workflow_v2.png) | Explanatory steps | A researcher defines the software rule, writes a test capable of detecting a violation, repairs the code, and runs the tests automatically after future changes. |
| [Distinct donor identifiers](../figures/figure_4_donor_units_v3.png) | Separate constructed donor-label demonstration | There are 1,000 repeated labels and two unique donor IDs. This **does not** establish independence or represent the six-donor RNA table. |

The four charts are accompanied by SVG versions in [`figures/`](../figures/), suitable for inspecting their vector labels.

## Rebuild from the input and test receipts

From the repository root, with Python 3.11 or newer:

```bash
python -m pip install -r requirements.txt
python generate_fictional_data.py
python analyze_fictional_rna.py
python run_demo.py
python make_figures.py
```

The generator recreates the same 36-row teaching CSV; the analysis writes [`outputs/fictional_summary.csv`](../outputs/fictional_summary.csv) and [`outputs/analysis_summary.json`](../outputs/analysis_summary.json). `run_demo.py` executes the same ten behavior checks against deliberately incorrect and repaired functions, writes JUnit XML and [`outputs/results.json`](../outputs/results.json); `make_figures.py` uses the CSV and saved reports to build four PNG/SVG pairs.

The code uses the fixed example inputs. The [figure-integrity tests](../tests/test_figure_integrity.py) check that the diagrams exist, their dimensions are adequate, and their key labels correspond to the current data. The [GitHub Actions workflow](../.github/workflows/scientific-regressions.yml) reruns the analysis and tests on each code change.

## Scientific boundaries

An unassayed gene is **not** an observed RNA zero. Counts of rows are not inherently counts of independent donors. A deliberate RED test run is an educational negative control rather than a failed current analysis. These diagrams do not validate real biological associations, differential expression, causal effects, or experimental power.

For the computed quantities and bounded interpretations, read [Results and interpretation](RESULTS_AND_INTERPRETATION.md). For a first experiment with regression tests, use the [hands-on guide](tutorial/FIRST_TEST_WALKTHROUGH.md).
