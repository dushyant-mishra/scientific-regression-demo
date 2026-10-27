# Analysis, results and scientific interpretation

## What was actually analyzed?

This repository runs a **small fictional RNA data-handling experiment**. It demonstrates how code should distinguish a measured RNA zero from a gene that was never assayed, and how regression tests can detect software that erases this distinction.

The input is [`data/fictional_rna_observations.csv`](../data/fictional_rna_observations.csv), generated deterministically by [`generate_fictional_data.py`](../generate_fictional_data.py). It contains two constructed studies, six donor identifiers (three per study), two cells per donor (twelve cells total), and three gene entries per cell (36 gene-by-cell records). All gene names and counts are synthetic.

The six CSV fields are `study`, `donor_id`, `cell_id`, `gene`, `assayed`, and `count`. An unassayed entry has `assayed=false` and a **blank count**. A measured zero has `assayed=true` and `count=0`. A detected measurement has `assayed=true` and `count>0`.

The parser in [`analyze_fictional_rna.py`](../analyze_fictional_rna.py) validates the frozen example schema, record identities, donor consistency within cells, nonnegative integer measured counts, and blank counts for unassayed entries; then it calls [`observation_state()`](../science_rules.py) to classify each entry.

## Results from the committed output

The following is transcribed from [`outputs/fictional_summary.csv`](../outputs/fictional_summary.csv), which the analysis script can recreate.

| Study | Gene | MEASURED_DETECTED | MEASURED_ZERO | UNMEASURED | Rows |
| --- | --- | ---: | ---: | ---: | ---: |
| study_a | gene_1 | 6 | 0 | 0 | 6 |
| study_a | gene_2 | 3 | 3 | 0 | 6 |
| study_a | gene_3 | 4 | 2 | 0 | 6 |
| study_b | gene_1 | 6 | 0 | 0 | 6 |
| study_b | gene_2 | 3 | 3 | 0 | 6 |
| study_b | gene_3 | 0 | 0 | 6 | 6 |
| **Total** | | **22** | **8** | **6** | **36** |

The companion [`outputs/analysis_summary.json`](../outputs/analysis_summary.json) reports 36 observations, six cells and three donors per study, and six distinct donor identifiers across the whole synthetic example.

### Interpretation 1: Missing assay coverage is not observed zero expression

Study B's six `gene_3` records are all `UNMEASURED`. **None is `MEASURED_ZERO`** because the synthetic Study B assay panel excludes that gene. A downstream comparison that substitutes six zeros for those records invents observed measurements and would answer the wrong question.

For a concrete contrast, `study_a / cell_01 / gene_3` is assayed with count 4; `study_b / cell_07 / gene_3` is not assayed and has no count; `study_a / cell_01 / gene_2` is assayed with count 0. These three records mean three different things.

A count of zero means **zero detected RNA transcripts in that observation**, not that the gene is absent from the genome, always inactive, or truly biologically unexpressed.

### Interpretation 2: Rows are not independent donors

In a **separate constructed test**, the list of donor identifiers contains 500 repeats of `donor_01` and 500 of `donor_02`. The function `replication_summary()` must return `technical_rows=1000` and `biological_n=2` (here, **two distinct identifiers**).

This is not another representation of the six-donor RNA CSV, not an actual resampling procedure, and **not proof that the two donors are statistically independent**. A real design could require explicit models for donor nesting, relatedness, batches, and other sources of dependence. The only thing tested here is *how the supplied identifiers are counted*.

### Interpretation 3: Missing evidence is not positive evidence

In a third independent illustration, `evidence_verdict()` accepts **preassigned** source status labels. Under the toy software policy, all required studies must be labeled `PASS` for an overall `PASS`. A known `FAIL` takes precedence, and a required missing/`NOT_ESTIMABLE` source prevents promotion to `PASS`.

These status labels are **not calculated from the RNA CSV**, and the example is **not a statistical meta-analysis or biological evidence-integration method**. It solely demonstrates how to encode and test a specified software decision policy.

## What the regression tests establish

The [ten switchable behavior tests](../tests/test_science_rules.py) are executed twice by [`run_demo.py`](../run_demo.py) against the intentionally incorrect [`science_rules_buggy.py`](../science_rules_buggy.py) and repaired [`science_rules.py`](../science_rules.py), without rewriting the tests:

| Software implementation | Passed | Failed | Errors |
| --- | ---: | ---: | ---: |
| Deliberately buggy (RED) | 4 | 6 | 0 |
| Repaired (GREEN) | 10 | 0 | 0 |

These counts come from the checked-in [`outputs/results.json`](../outputs/results.json), which is generated from JUnit XML records, not manually asserted in the illustration. A failing RED comparison is **expected**: it shows the tests detect some intentionally inserted defects. Passing GREEN only verifies the behaviors covered by those ten tests. The broader test suite also checks dataset and report integrity, input edge cases, figure validity, and historical audit consistency.

In particular, **none** of these tests demonstrates that a gene is differentially expressed, establishes the statistical power of an experiment, estimates causal effects, validates biological replication, or justifies inference about a disease.

## Reproduce the analysis and inspect the outputs

From a checkout of the repository with Python 3.11 or newer:

```bash
python -m pip install -r requirements.txt
python generate_fictional_data.py
python analyze_fictional_rna.py
python -m pytest -q
python run_demo.py
python make_figures.py
```

Inspect the regenerated summary at `outputs/fictional_summary.csv`, metadata at `outputs/analysis_summary.json`, the JSON/JUnit test receipts under `outputs/`, and the plots under `figures/`. The image-generation methods and each graphic's interpretation are in [Figures and methods](FIGURES_AND_METHODS.md).

These commands operate on the **fixed teaching fixture** and write to tracked local output paths. Reproducing them does not require real patient data or a cloud service; only installing dependencies requires package access. To adapt the idea to actual cohorts, define new scientifically valid rules, schemas, unit-of-analysis assumptions, control examples, and tests. The fixed 36-row reader is not a general-purpose RNA analysis pipeline.

## Limits and provenance

- Synthetic gene names, counts, studies, and donor IDs cannot support real biological discovery.
- Assay omission is represented explicitly by the `assayed` field; other datasets require verified coverage metadata. Do not infer unassayed status from a zero count alone.
- Counting distinct donor IDs is not a complete biological-independence or statistical-inference model.
- The RED/GREEN comparison is a software regression demonstration; a green build is not a biological validation certificate.
- For reproducibility, [cite the precise commit](../CITATION.cff) and consult the [workflow checks](../.github/workflows/scientific-regressions.yml). The [historical audit](audit/README.md) preserves older snapshot evidence without overriding present source files.
