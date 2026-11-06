# Reproduce and verify the scientific teaching analysis

This is a **reader-facing reproducibility checklist** for the synthetic RNA data-handling demonstration. It is not a research claim about a real cohort. All numbers below describe the fixed fictional fixture or executed software tests.

## 1. Run the example

Requirements: Python 3.11 or later, a terminal, and package installation access.

```bash
git clone https://github.com/dushyant-mishra/scientific-regression-demo.git
cd scientific-regression-demo
python -m pip install -r requirements.txt
python generate_fictional_data.py
python analyze_fictional_rna.py
python -m pytest -q
python run_demo.py
```

`python` may be `python3` on some systems or `py` on Windows. On a shared workstation, use a virtual environment to avoid changing existing packages. The generation scripts write to tracked local paths; run them from a clean checkout when you want to compare regenerated files.

The `run_demo.py` command intentionally executes a faulty implementation. Its internal **RED** pytest process exits nonzero, which the runner handles as *expected evidence of a caught bug*. `run_demo.py` itself should finish successfully when the RED run has failures and the GREEN run passes completely.

## 2. Verify the RNA observations

Inspect [`data/fictional_rna_observations.csv`](../data/fictional_rna_observations.csv) and [`outputs/fictional_summary.csv`](../outputs/fictional_summary.csv).

- **36** synthetic gene-by-cell records, **12** cell IDs, **6** distinct donor IDs, **3** placeholder genes and **2** studies.
- `study_a / cell_01 / gene_3`: `assayed=true`, `count=4`, **MEASURED_DETECTED**.
- `study_a / cell_01 / gene_2`: `assayed=true`, `count=0`, **MEASURED_ZERO**.
- `study_b / cell_07 / gene_3`: `assayed=false`, **blank** count, **UNMEASURED**.
- All **six** `study_b / gene_3` entries are marked unassayed, not measured-zero.
- The grouped analysis totals are **22 measured-detected, 8 measured-zero, and 6 unmeasured** across 36 rows.

**Crucial boundary:** an empty count *by itself* does not establish that a gene was never assayed. In this example, `assayed=false` supplies that information. In a real cohort, assay-coverage metadata and its provenance need independent verification; correct software cannot repair incorrect metadata automatically. A measured count of zero means nothing was detected in the observation, not that the gene is always biologically inactive.

The analysis deliberately accepts only its fixed fixture. Do not apply it to clinical data without defining and testing a suitable real-data schema, assay metadata, study design and analysis plan.

## 3. Verify the two software implementations

The unchanged [ten scientific-rule tests](../tests/test_science_rules.py) are run against:

- [`science_rules_buggy.py`](../science_rules_buggy.py): **intentionally defective, teaching-only** code, expected **4 passed / 6 failed / 0 errors**.
- [`science_rules.py`](../science_rules.py): corrected rule implementation, expected **10 passed / 0 failed / 0 errors**.

Inspect [`outputs/results.json`](../outputs/results.json) for the exact recorded counts and source/report SHA-256 digests. The counts are parsed from JUnit testcase records produced by `run_demo.py`; they are not hard-coded.

The six failing tests exercise **multiple** data-handling and input-validation rules, not six independent RNA experiments. The additional examples are **separate**: 1,000 repeated donor labels have only two distinct donor IDs, and preassigned study-evidence labels are subject to a specified software policy. These examples do not estimate biological independence or perform meta-analysis.

A GREEN result means the implementation satisfied *the checks that were written*. It does not establish that the input metadata, chosen rule, biological model, or scientific inference is correct.

## 4. Check the generated outputs

After the commands above, open:

| Output | What to inspect |
| --- | --- |
| [`outputs/fictional_summary.csv`](../outputs/fictional_summary.csv) | Classified counts by study and placeholder gene |
| [`outputs/analysis_summary.json`](../outputs/analysis_summary.json) | Dataset census and summary provenance |
| [`outputs/results.json`](../outputs/results.json) | Exact RED/GREEN test totals and source/JUnit digests |
| [`outputs/red_pytest.xml`](../outputs/red_pytest.xml) and [`outputs/green_pytest.xml`](../outputs/green_pytest.xml) | Individual JUnit testcase evidence |

The **main pytest suite** checks data, source logic, reports, and documentation consistency. Its test count can change as tests are added; use the current CI run rather than treating a past total as a permanent requirement.

For methodological limitations and the meaning of the results, read [Results and interpretation](RESULTS_AND_INTERPRETATION.md). For a beginner exercise in deliberately breaking and repairing one rule, use the [first-test walkthrough](tutorial/FIRST_TEST_WALKTHROUGH.md).

## 5. GitHub-hosted verification

The [GitHub Actions workflow](../.github/workflows/scientific-regressions.yml) installs dependencies, regenerates the synthetic data and analysis, runs the main suite, and runs the deliberate RED/GREEN comparison. It uploads the executed output records as a workflow artifact.

Check the [current workflow results](https://github.com/dushyant-mishra/scientific-regression-demo/actions/workflows/scientific-regressions.yml) against the **exact commit** being examined. A successful workflow demonstrates that the specified checks completed; it is not a certificate of biological validity.

For a reusable citation, use [`CITATION.cff`](../CITATION.cff) and identify the exact commit. Historical changes and workflow outcomes are available through Git history and the merged pull requests.

## Repository scope

This public repository is for **running, inspecting and interpreting the scientific teaching analysis**. It contains the demonstration source, synthetic data, automated tests, recorded results, and documentation needed to reproduce and understand them.
