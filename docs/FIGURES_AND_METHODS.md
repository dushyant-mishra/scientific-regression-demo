# Figures and reproducible visualization methods

The figures in this repository explain the **fictional RNA measurement states and software regression tests**. They are not microscopy, new biological measurements, or statistical evidence of expression differences.

## What each figure means

| Graphic | Source | Interpretation |
| --- | --- | --- |
| [RNA measurement matrix](../figures/figure_1_rna_measurements_v2.png) | `data/fictional_rna_observations.csv` | Per-cell `+` means detected, `0` means assayed with no transcripts detected, and `—` means not assayed. Study B lacks measurements of `gene_3`. |
| [Illustrated RNA comparison (portrait)](../figures/editorial_01_rna_evidence_mobile_v1.png) | Same fictional CSV | Study A `cell_01/gene_3` was assayed with count 4, while Study B `cell_07/gene_3` was not assayed. Study A `cell_01/gene_2` is a separately identified measured zero. |
| [RED/GREEN test chart](../figures/figure_2_test_results_v2.png) | `outputs/results.json`, parsed from real JUnit testcase entries | Four tests pass and six fail with intentionally defective rules; the same ten all pass with repaired rules. |
| [Illustrated test tiles (portrait)](../figures/editorial_02_test_tripwire_mobile_v1.png) | Same RED/GREEN receipt | Each tile represents one executed behavior test; colors and symbols distinguish passes from failures. Their display order is illustrative and does **not** identify individual test names. |
| [Donor-identifier illustration](../figures/figure_4_donor_units_v3.png) | Separate constructed row-label list in `make_figures.py` | 1,000 repeated rows contain **two distinct donor identifiers**. This does not establish statistical independence or describe the main six-donor RNA CSV. |
| [Scientific regression workflow](../figures/figure_3_regression_workflow_v2.png) | Explanatory sequence | Define a scientific rule, make a failing test, repair the code, rerun the test, and protect against future regression in CI. |

The wide versions of the illustrated RNA and test-tile graphics are also available under `figures/editorial_01_rna_evidence_landscape_v1.*` and `figures/editorial_02_test_tripwire_landscape_v1.*`. Each version has both PNG and SVG outputs.

## How the figures are generated

The conventional charts are made by [`make_figures.py`](../make_figures.py). The more illustrative wide and portrait versions are made by [`make_editorial_figures.py`](../make_editorial_figures.py), which **reads** the fixed CSV and `outputs/results.json` instead of supplying those scientific values manually.

Reproduce the input, classifications, test report, and standard charts:

```bash
python -m pip install -r requirements.txt
python generate_fictional_data.py
python analyze_fictional_rna.py
python run_demo.py
python make_figures.py
```

To build the independently composed portrait and landscape illustrations:

```bash
python -m pip install -r requirements-editorial.txt
python make_editorial_figures.py
```

The SVG masters retain text labels, explicit titles, and descriptions; PNGs are generated at high pixel resolutions for easier viewing. The fixed CSV schema and recorded test source limit what each graphic may truthfully display.

## What is checked automatically?

The repository's [figure tests](../tests/test_figure_integrity.py) and [illustrated-figure tests](../tests/test_editorial_figure_integrity.py) verify dimensions, linked asset presence, gene labels, raw-data associations, pass/fail values, accessible SVG metadata, mobile lettering floors, and the generator's configured small-text contrast pairs (at least **4.5:1**). A negative fixture mutates an assay flag and verifies that the figure data-reader rejects the inconsistent input.

The [GitHub Actions workflow](../.github/workflows/scientific-regressions.yml) runs image regeneration and integrity checks along with the scientific behavior tests. These mechanical checks are valuable but **cannot prove all layout or scientific interpretation questions**: image legibility still deserves human inspection, and biological assumptions require domain review.

## Historical figures and interpretation boundary

Older figure versions remain in `figures/` where the [historical audit validator](../scripts/validate_lane_audit.py) requires them. Their presence is **provenance**, not a reason to prefer an older graphic or imply that old figures prove a biological result.

All data and reported numerical outcomes here are constructed teaching examples. They do not estimate differential expression, donor independence, statistical significance, or any disease finding. For the numerical data and its scientific meaning, start at [Results and interpretation](RESULTS_AND_INTERPRETATION.md).
