# When AI Writes Your RNA Analysis Code, Who Checks the Science?

*An illustrated, hands-on guide to scientific regression tests, RNA data, Python, GitHub Actions, and independent AI-agent review.*

Imagine you are comparing RNA expression between two studies. An AI coding agent helps you write Python to read the data and summarize the results. The script runs without an error. The plots look reasonable.

But one question remains: **is the software making the scientific distinctions you intended?**

What if a gene that was never assayed is recorded as having zero RNA? What if 1,000 rows labeled with just two donor IDs are treated as 1,000 independent donors? What if a cross-study result is marked as supported even though one required study lacks enough evidence?

These mistakes may produce no Python exception. They are mistakes in scientific meaning.

This tutorial shows how to catch them using **regression tests**: short programs that check whether software still respects a defined rule after its code changes. Here, *regression testing* means checking for recurring software defects. It does **not** mean fitting a statistical regression model.

**Run the complete example:** [github.com/dushyant-mishra/scientific-regression-demo](https://github.com/dushyant-mishra/scientific-regression-demo). It includes the example dataset, Python scripts, ten behavior tests, additional checks, a GitHub Actions workflow, and figures from the test runs.

> **About the data:** This is a made-up teaching dataset. `gene_1`, `gene_2`, and `gene_3` are placeholder names, and none of the measurements comes from a real study.

## 1. The RNA experiment

Our main RNA dataset contains two studies with three donors each. Every donor contributes two cells, and each cell has three gene entries. That gives **6 donors, 12 cells, and 36 gene-by-cell records**.

**Keep the two examples separate:** the RNA dataset has six donors. Later, to explain pseudoreplication, we use a *different*, deliberately small example with **two donor IDs repeated across 1,000 computational rows**. Those 1,000 rows are not from this RNA dataset.

- **gene_1** is measured in both studies and has positive counts in our example.
- **gene_2** is measured in both studies, but sometimes has a zero count.
- **gene_3** is measured in Study A; Study B's assay panel does *not* include it.

A few rows from the actual included file `data/fictional_rna_observations.csv`:

| Study | Donor | Cell | Gene | Assayed? | RNA count |
|---|---|---|---|---|---:|
| study_a | donor_01 | cell_01 | gene_1 | true | 12 |
| study_a | donor_01 | cell_01 | gene_2 | true | 0 |
| study_a | donor_01 | cell_01 | gene_3 | true | 4 |
| study_b | donor_04 | cell_07 | gene_3 | false | *empty* |

The included `generate_fictional_data.py` script recreates the dataset whenever you run it.

![RNA measurement matrix with positive counts, measured zeros, and structurally unassayed genes](https://raw.githubusercontent.com/dushyant-mishra/scientific-regression-demo/main/figures/figure_1_rna_measurements_v2.png)

*Figure 1. Each row represents one cell. A plus sign means RNA was detected, `0` means the gene was assayed but no molecules were detected, and a dash means the gene was not assayed. Study B never assays gene_3. Figure produced from the included CSV.*

### Why the difference matters

DNA contains genes. RNA sequencing provides measurements of RNA transcripts from those genes. If an assay returns a zero RNA count, we observed **zero detected transcripts in that particular observation**. That does not prove the gene is absent from the genome or biologically inactive.

If a gene was never included in an assay, we have **no RNA measurement for that gene**. Filling that gap with zero would invent an observation.

We therefore want three software states:

| State | Meaning |
|---|---|
| `MEASURED_DETECTED` | Assayed and count greater than zero |
| `MEASURED_ZERO` | Assayed and count equal to zero |
| `UNMEASURED` | Not assayed; there is no count |

This is the first scientific rule we will protect.

## 2. Three scientific rules to turn into tests

**Rule A: Zero is not missing.** The software must preserve `MEASURED_ZERO` separately from `UNMEASURED`.

**Rule B: More rows do not necessarily mean more independent donors.** Repeated draws, cells, or technical measurements can increase the number of observations without increasing the number of biological donors. Our toy example assumes donors are independent units; real experiments may need more elaborate nesting or dependence models.

**Rule C: Insufficient evidence must not become success.** For our *illustrative* cross-study decision policy, both studies must pass to issue `PASS`. A required study marked `NOT_ESTIMABLE` prevents that result. A known `FAIL` takes precedence over missing evidence. This is **not** a universal rule for combining statistical evidence; it is a particular rule we choose to make explicit and testable.

None of these rules determines whether a gene is differentially expressed. They protect the meaning of the input and output labels before more sophisticated statistics are attempted.

## 3. Follow the code, one rule at a time

Before looking at the tests, try the three examples from the repository:

```bash
python try_examples.py
```

You should see `MEASURED_ZERO` for the measured zero, `UNMEASURED` for the gene that was not assayed, **1,000 rows but only two distinct donors** in the separate repeated-observation example, and `NOT_ESTIMABLE` for the study without enough evidence. Each of these outputs comes from a function in [`science_rules.py`](https://github.com/dushyant-mishra/scientific-regression-demo/blob/main/science_rules.py).

### Rule A — A zero is not missing data

```python
def observation_state(*, measured: bool, count: int | None) -> str:
    """Distinguish a measured zero from a gene that was not assayed."""
    # A string such as "false" must not be mistaken for the Boolean False.
    if type(measured) is not bool:
        raise TypeError("measured must be a bool")

    if not measured:
        if count is not None:
            raise ValueError("an unmeasured observation must have no count")
        return "UNMEASURED"

    # Booleans are integers in Python, so require exactly int here.
    if type(count) is not int or count < 0:
        raise ValueError("a measured count must be a nonnegative integer")

    if count == 0:
        return "MEASURED_ZERO"
    return "MEASURED_DETECTED"
```

Read it from top to bottom:

1. Check that `measured` is an actual Boolean (`True` or `False`), not the string `"false"`.
2. If the gene was not assayed, require `count=None` and return `UNMEASURED`.
3. Otherwise, require a nonnegative integer count. Return `MEASURED_ZERO` for 0 or `MEASURED_DETECTED` for a positive number.

The `*` in the function signature means we must name the arguments when calling it—for example, `observation_state(measured=True, count=0)`. This helps prevent mixing up the assay flag and the count.

### Rule B — Rows and donors are different counts

```python
def replication_summary(donor_ids: list[str]) -> dict[str, int]:
    """Count observation rows and distinct donor IDs separately."""
    if not donor_ids:
        raise ValueError("donor_ids must contain valid nonempty donor IDs")

    for donor_id in donor_ids:
        if type(donor_id) is not str or not donor_id.strip():
            raise ValueError("donor_ids must contain valid nonempty donor IDs")

    return {
        "technical_rows": len(donor_ids),
        "biological_n": len(set(donor_ids)),
    }
```

Here, `len(donor_ids)` counts all supplied rows. `set(donor_ids)` keeps each donor identifier only once, so `len(set(donor_ids))` counts distinct donors. The input checks prevent empty or malformed donor labels.

### Rule C — Missing evidence cannot turn into a PASS

The third function, `evidence_verdict()`, uses this decision order:

```text
If a required study has a known FAIL → FAIL
Otherwise, if any required study is missing or NOT_ESTIMABLE → NOT_ESTIMABLE
Otherwise, if all required studies PASS → PASS
```

The [complete Python function](https://github.com/dushyant-mishra/scientific-regression-demo/blob/main/science_rules.py) also checks the supplied study names and status values. This is a chosen rule for our exercise, not a general statistical method for combining studies.

To explore the repository, read **`try_examples.py` → `science_rules.py` → `tests/test_science_rules.py`** in that order. The CSV reader and figure-generation code can come later.

## 4. What does a regression test look like?

A regression test asks: “If somebody changes this code tomorrow, will this scientific rule still hold?”

We use Python's `pytest` package. To try the small test examples below in your own test file, begin with:

```python
from science_rules import observation_state, replication_summary, evidence_verdict
```

Then write a test like this:

```python

def test_zero_is_not_unmeasured():
    assert observation_state(measured=True, count=0) == "MEASURED_ZERO"
    assert observation_state(measured=False, count=None) == "UNMEASURED"
```

Each `assert` is an expected behavior. If a future refactor turns both inputs into the same output, this test fails.

For donor accounting:

```python

def test_technical_rows_are_not_independent_donors():
    ids = ["donor_01"] * 500 + ["donor_02"] * 500
    result = replication_summary(ids)
    assert result == {"technical_rows": 1000, "biological_n": 2}
```

This **separate two-donor example** constructs 500 entries labeled `donor_01` and 500 labeled `donor_02`. It does not generate new biological measurements or actually perform resampling. It illustrates how counting repeated rows as independent donors would be wrong; it does not describe the six-donor RNA CSV.

![Donor accounting contrasts 1000 computational rows with 2 independent donors](https://raw.githubusercontent.com/dushyant-mishra/scientific-regression-demo/main/figures/figure_4_donor_units_v2.png)

*Figure 2. A separate two-donor demonstration: 1,000 repeated row labels correspond to two distinct donors, not to 1,000 independent biological replicates.*

For cross-study evidence:

```python

def test_insufficient_second_study_cannot_pass():
    statuses = {"study_a": "PASS", "study_b": "NOT_ESTIMABLE"}
    assert evidence_verdict(statuses) == "NOT_ESTIMABLE"
```

The repository's actual test file has a small import switch so the *same ten tests* can run against either the buggy or corrected implementation. You do not need to change that switch yourself. The complete `tests/test_science_rules.py` includes ten behavior tests, including edge cases discovered during independent review: invalid assay flags, an empty required-study list, and a known failed study alongside absent evidence.

## 5. Deliberately introduce bugs: RED → GREEN

One common AI-assisted programming failure is code that looks shorter and cleaner but erases an important distinction. Consider this **deliberately broken** function:

```python

def observation_state(*, measured, count):
    return "MEASURED_ZERO" if not count else "MEASURED_DETECTED"
```

Python treats `0` and `None` as false-like values. This function therefore converts both an observed zero and a gene that was never measured into `MEASURED_ZERO`. It also ignores the `measured` flag entirely.

Our repository includes `science_rules_buggy.py` with this defect and two others: treating each row as an independent donor and accepting a cross-study PASS if any study passes.

We ran **the same ten tests** against the buggy implementation and the repaired one. We did not edit the tests between runs.

Actual local pytest results:

```text
RED   4 passed, 6 failed, 0 errors
GREEN 10 passed, 0 failed, 0 errors
```

![RED versus GREEN pytest runs: four pass and six fail before repair; ten pass afterward](https://raw.githubusercontent.com/dushyant-mishra/scientific-regression-demo/main/figures/figure_2_test_results_v2.png)

*Figure 3. Results from running the same ten tests against the defective and corrected implementations. Before the repair, six tests fail; afterward, all ten pass.*

Why is this important? **A test that has never demonstrated it can catch a defect gives limited reassurance.** RED is valuable because it shows the test notices the kind of error it claims to guard against. GREEN shows that the repaired software satisfies those same tests.

## 6. Why GitHub if we can run the tests locally?

Everything above can run on a laptop. GitHub is not necessary to compute a pytest result.

The practical reason for GitHub is what happens *after* the first successful run.

Imagine one person changes how the CSV is parsed. An agent refactors the functions the next day. A collaborator adds another gene panel the week after. Someone might accidentally undo a repaired rule. If tests run only when a person remembers, the mistake may go unnoticed.

GitHub stores the code and change history. **GitHub Actions** can rerun the defined checks automatically on pushes and pull requests. It also leaves reviewable logs linked to the exact Git revision.

Local tests tell us whether code passes *here and now*. Repository CI tells us whether the code committed to a shared revision still satisfies the tests. Neither one alone proves that a biological claim is true.

![Vertical workflow from defining a biological rule to tests, repair, GitHub Actions and evidence review](https://raw.githubusercontent.com/dushyant-mishra/scientific-regression-demo/main/figures/figure_3_regression_workflow_v2.png)

*Figure 4. A compact workflow you can adopt for RNA, DNA, or other computational research. Independent scientific review remains distinct from CI execution.*

## 7. Reproduce the tutorial on GitHub: step by step

The example project is public at **[scientific-regression-demo](https://github.com/dushyant-mishra/scientific-regression-demo)**. You may clone it and run it as-is, or fork it to experiment with changes.

**Step 1 — Open or fork the repository.** On GitHub, open the repository and click **Fork** if you want your own copy. Or clone it locally:

```bash
git clone https://github.com/dushyant-mishra/scientific-regression-demo.git
cd scientific-regression-demo
```

**Step 2 — Install dependencies.** Python 3.11 or newer is recommended for this example. In your terminal, run:

```bash
python -m pip install -r requirements.txt
```

`pytest` runs the tests. `matplotlib` draws the figures. Everything else uses Python's standard library.

**Step 3 — Rebuild the dataset and analyze it.**

```bash
python try_examples.py
python generate_fictional_data.py
python analyze_fictional_rna.py
```

The first command prints three small worked examples. The next two rebuild `data/fictional_rna_observations.csv` and create summary files in `outputs/`. In the included example, Study B has **six `UNMEASURED` records for gene_3 and zero measured-zero records for that gene**. Those values come from the actual CSV processing code.

**Step 4 — Run the full test suite.**

```bash
python -m pytest -q
```

At the audited [27 October 2026 GitHub Actions run](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40553329081), **25 tests passed** on commit [`75ecd86`](https://github.com/dushyant-mishra/scientific-regression-demo/commit/75ecd86cec470843b5352f80ef1a67d92f89eba3). Ten are the behavior tests used in the RED/GREEN demonstration; the rest check the dataset, cell-to-donor consistency, reporting, figures, and audit/handoff records. The total can change as tests are added, so use the command above to check the version you cloned.

**Step 5 — Reproduce the RED/GREEN evidence and figures.**

```bash
python run_demo.py
python make_figures.py
```

The RED run is *supposed to fail its tests*. `run_demo.py` runs both versions without overwriting `science_rules.py`. The saved outputs show which checks failed and which passed.

**Step 6 — Create a change on a branch.** If you forked the repository, create a branch in your copy, change one implementation rule, and push the branch. You can deliberately reintroduce the `not count` defect as an educational exercise, but do not merge broken code into a branch others rely on.

**Step 7 — Open a pull request.** GitHub's **Actions** tab will show the workflow named *RNA scientific regression checks*. It checks out the submitted revision, installs Python and dependencies, runs tests, reproduces RED/GREEN, and rebuilds the figures. The saved workflow artifacts contain result logs.

**Step 8 — Review the test result, not just the green icon.** Open the workflow log. Verify the number of tests executed, whether anything was skipped, and whether the scientific rule is actually tested. If your repository supports rulesets/branch protection, you can configure its regression workflow as a required check before merging.

The results discussed earlier were captured from local runs. For hosted results on the current repository revision, check the **Actions** tab and inspect the workflow logs.

## 8. Using an AI coding agent responsibly

A stronger instruction than “write an RNA analysis pipeline” is:

> Build a test demonstrating that an unassayed gene cannot be reported as a measured zero. First show the failing behavior, repair only the implementation, and rerun the same test. Record the commands, outputs and source revision. Do not change the expected answer to make the test green.

Then give a second reviewer a different task:

> Try to break the repaired RNA data-handling pipeline. Include invalid assay flags, missing counts, duplicate donor identifiers, an empty required-study set and conflicting study statuses. For every genuine defect, write a new test and explain which scientific rule it protects.

The second reviewer should not merely repeat the first agent's claims. They should independently attempt to falsify them.

## 9. What passing tests *do not* prove

This exercise does **not** test differential expression, causal regulation, disease association, statistical power or biological replication. It does not prove that a donor-level estimator is correctly calibrated: it simply catches a donor-counting mistake. And combining source-level `PASS` labels is not a substitute for proper statistical modeling of multiple studies.

A test can faithfully implement the wrong scientific assumption. A passing CI build can therefore still contain an invalid scientific analysis. The safeguard is to make assumptions visible, include positive and negative controls, review the data provenance, and subject both code and tests to independent challenge.

## 10. Reuse and citation

The code, data generator, and instructions are available in the repository. The README has the exact commands needed to reproduce the figures and test results.

If you reuse the code or its teaching example, cite the **repository at the exact commit you used**, because the repository can change. The repository includes a `CITATION.cff` file so GitHub can display **Cite this repository** where supported.

Suggested citation (replace the placeholder commit hash with the one you actually used):

> dushyant-mishra. (2026). *Scientific Regression Demo: RNA Data, Regression Tests, and GitHub Actions* [Computer software and teaching materials]. GitHub. https://github.com/dushyant-mishra/scientific-regression-demo (commit: `<COMMIT_SHA>`).

There is **no DOI assigned** to this demonstration at the time of writing. If a permanent archived release/DOI is created in the future, use that release's citation metadata rather than inventing a DOI now. This Medium article can be cited separately by its final publication URL and date.

## Final thought

The important habit is to turn scientific assumptions into tests that run whenever the analysis changes.

Here, the rules are concrete: a gene that was not assayed is not a measured zero; repeated observations do not create additional independent donors; and insufficient evidence cannot silently become a positive result. The same tests work locally and in GitHub Actions, with results tied to the code revision that produced them.

AI coding agents can help write and repair the implementation. A second reviewer can challenge the tests and try cases the first agent missed. Neither replaces the researcher's responsibility to define the scientific rule.

**Define the rule → demonstrate a failing case → repair the code → rerun unchanged tests → review the evidence → guard against regressions on GitHub.**
