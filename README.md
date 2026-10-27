# RNA regression tests: a small example you can run

[![Tests](https://github.com/dushyant-mishra/scientific-regression-demo/actions/workflows/scientific-regressions.yml/badge.svg)](https://github.com/dushyant-mishra/scientific-regression-demo/actions/workflows/scientific-regressions.yml)

A Python script can run without errors and still get the biology wrong. This little project shows how to catch three mistakes before they become part of an analysis:

- Calling a gene's RNA count **zero** when the gene was **never assayed**.
- Counting repeated observations as if they came from different donors.
- Reporting that two studies support a finding when one has too little information to judge it.

This is a teaching dataset: `gene_1`, `gene_2`, and `gene_3` are placeholder names, and the observations were generated for this exercise.

## The example

Our RNA dataset contains two studies, three donors per study, two cells per donor, and three gene entries per cell. That's **6 donors, 12 cells, and 36 gene-by-cell rows** in [the CSV](data/fictional_rna_observations.csv).

Later, the donor-counting test uses a **separate two-donor example** with 1,000 repeated row labels. It is not a different count of the donors in this CSV.

| Study | Donor | Cell | Gene | Assayed? | RNA count |
|---|---|---|---|---|---:|
| study_a | donor_01 | cell_01 | gene_1 | true | 12 |
| study_a | donor_01 | cell_01 | gene_2 | true | 0 |
| study_a | donor_01 | cell_01 | gene_3 | true | 4 |
| study_b | donor_04 | cell_07 | gene_3 | false | *(blank)* |

The second row is a **measured zero**: the assay looked for RNA from `gene_2` and detected none in that cell. The fourth row is **not a zero**: Study B did not assay `gene_3` at all. That difference matters when combining datasets.

![RNA measurement table drawn from the CSV](figures/figure_1_rna_measurements_v2.png)

## Try it on your computer

You need Python 3.11 or later and Git. In a terminal:

```bash
git clone https://github.com/dushyant-mishra/scientific-regression-demo.git
cd scientific-regression-demo
python -m pip install -r requirements.txt
python try_examples.py
python generate_fictional_data.py
python analyze_fictional_rna.py
python -m pytest -q
python run_demo.py
python make_figures.py
```

Start with `try_examples.py`: it prints the three scientific rules in action without needing to understand pytest. `generate_fictional_data.py` recreates the CSV. `analyze_fictional_rna.py` classifies each record as detected, measured zero, or unmeasured. `pytest` checks the rules. `run_demo.py` runs **the same tests twice**: first against deliberately broken code, then against the repair. `make_figures.py` rebuilds the charts from the saved CSV and actual test reports.

At the audited GitHub revision [`75ecd86`](https://github.com/dushyant-mishra/scientific-regression-demo/commit/75ecd86cec470843b5352f80ef1a67d92f89eba3) (27 October 2026), the [hosted workflow](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40553329081) reproduced the examples and reported:

```text
Full repository suite: 25 passed
Deliberately broken code: 4 passed, 6 failed
Repaired code: 10 passed, 0 failed
```

Those numbers are recorded test results, not biological findings. The 25-test total includes a reader check that each cell's gene rows agree on their donor ID. Test totals may change if tests are added or edited. The chart reads the saved pytest/JUnit reports instead of assuming those numbers.

![Actual RED and GREEN test results](figures/figure_2_test_results_v2.png)

## Why put it on GitHub?

You can run everything locally. GitHub is useful because code changes: a collaborator or coding agent might accidentally bring back an old error. The [GitHub Actions workflow](.github/workflows/scientific-regressions.yml) reruns the tests for pushes and pull requests, so reviewers can see **which committed version** passed and read its logs.

Try it yourself: fork the repository, make a new branch, change the correct function in `science_rules.py` to treat `None` as zero, and open a pull request. The tests should fail. Restore the correct function, push again, and watch them pass. Don't merge the broken change.

A green check only says that the tests passed. It doesn't prove a biological hypothesis, that the tests are complete, or that the statistical method is correct. This exercise checks data-handling rules; it does not estimate differential expression or disease associations.

## Which files should I read first?

1. [`try_examples.py`](try_examples.py) — run three examples and see their outputs.
2. [`science_rules.py`](science_rules.py) — read the three functions those examples call.
3. [`tests/test_science_rules.py`](tests/test_science_rules.py) — see how a test checks the expected answer.

The other scripts read the CSV, record test results, and build the figures. You can explore them afterward.

## Where to look

- [**Article and walkthrough**](MEDIUM_ARTICLE.md) — the reasoning behind each test, screenshots/figures, and a GitHub step-by-step guide.
- [`data/fictional_rna_observations.csv`](data/fictional_rna_observations.csv) — the example measurements.
- [`science_rules.py`](science_rules.py) and [`science_rules_buggy.py`](science_rules_buggy.py) — correct and deliberately wrong versions.
- [`tests/`](tests) — checks for biological rules, CSV processing and report integrity.
- [`outputs/`](outputs) and [`figures/`](figures) — the local run receipts and plots (PNG and SVG).
- [`run_demo.py`](run_demo.py) — produces the RED/GREEN reports without changing your source files.

## Using and citing the example

You're welcome to clone, fork and adapt the code under the [MIT license](LICENSE). If you use it in teaching or writing, please cite the repository. GitHub's **Cite this repository** menu reads [`CITATION.cff`](CITATION.cff). For reproducibility, add the commit SHA you actually used:

> dushyant-mishra. (2026). *Scientific Regression Demo: RNA Data, Regression Tests, and GitHub Actions* [Software and teaching materials]. GitHub. https://github.com/dushyant-mishra/scientific-regression-demo (commit `<SHA>`).

There is no DOI for this project. You can cite the [article](MEDIUM_ARTICLE.md) separately after it is published on Medium.


## Maintaining this tutorial

The completed historical reviews are indexed in [the audit](docs/audit/README.md). New contributors and coding agents can start from [the takeover guide](docs/handoff/README.md) rather than repeating old reviews.
