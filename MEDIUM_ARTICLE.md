# When AI Writes Your RNA Analysis Code, Who Checks the Science?

*An illustrated, hands-on guide to scientific regression tests, fictional gene-expression data, Python, GitHub Actions, and independent AI-agent review.*

Imagine you are comparing RNA expression between two studies. An AI coding agent helps you write Python to read the data and summarize the results. The script runs without an error. The plots look reasonable.

But one question remains: **is the software making the scientific distinctions you intended?**

What if a gene that was never assayed is recorded as having zero RNA? What if 1,000 computational resamples from two donors are treated as 1,000 independent donors? What if a cross-study result is marked as supported even though one required study lacks enough evidence?

These mistakes may produce no Python exception. They are mistakes in scientific meaning.

This tutorial shows how to catch them using **regression tests**: short programs that check whether software still respects a defined rule after its code changes. Here, *regression testing* means checking for recurring software defects. It does **not** mean fitting a statistical regression model.

**Run the complete example:** [github.com/dushyant-mishra/scientific-regression-demo](https://github.com/dushyant-mishra/scientific-regression-demo). It includes the fictional CSV, Python scripts, ten behavior tests, additional integration/reporting tests, a GitHub Actions workflow, and figures generated from the actual test reports.

> **Everything in this example is fictional.** The genes `gene_1`, `gene_2`, and `gene_3` are invented teaching labels, not biological gene names. The donors, cells, studies, counts, outcomes, and figures are artificial. Nothing here is a claim about human biology.

## 1. The fictional RNA experiment

Our imaginary lab has measured RNA in six fictional donors, three from Study A and three from Study B. Each donor contributes two fictional cells. For each cell we keep a row for each of three invented genes, giving **12 cells × 3 genes = 36 records**.

- **gene_1** is measured in both studies and has positive counts in our example.
- **gene_2** is measured in both studies, but sometimes has a zero count.
- **gene_3** is measured in Study A; Study B's fictional panel does *not* assay it.

A few rows from the actual included file `data/fictional_rna_observations.csv`:

| Study | Donor | Cell | Gene | Assayed? | RNA count |
|---|---|---|---|---|---:|
| study_a | donor_01 | cell_01 | gene_1 | true | 12 |
| study_a | donor_01 | cell_01 | gene_2 | true | 0 |
| study_a | donor_01 | cell_01 | gene_3 | true | 4 |
| study_b | donor_04 | cell_07 | gene_3 | false | *empty* |

All these data are generated deterministically by `generate_fictional_data.py`; they are not downloaded or simulated to resemble any specific real person.

![Fictional RNA measurement matrix with positive counts, measured zeros, and structurally unassayed genes](https://raw.githubusercontent.com/dushyant-mishra/scientific-regression-demo/main/figures/figure_1_fictional_rna_matrix.png)

*Figure 1. Each row is one fictional cell. A plus sign means RNA was detected, `0` means the gene was assayed but no molecules were detected, and a dash means the gene was not assayed. Study B never assays gene_3. Figure produced from the included CSV.*

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

## 3. Write the code that represents the biology

Create a file called `science_rules.py`. Here is the first function from the downloadable project:

```python

def observation_state(*, measured: bool, count: int | None) -> str:
    if type(measured) is not bool:
        raise TypeError("measured must be a bool")
    if not measured:
        if count is not None:
            raise ValueError("an unmeasured observation must have no count")
        return "UNMEASURED"
    if type(count) is not int or count < 0:
        raise ValueError("a measured count must be a nonnegative integer")
    return "MEASURED_ZERO" if count == 0 else "MEASURED_DETECTED"
```

**Walkthrough:**

First, `measured` must be a real Boolean—`True` or `False`, not the string `"false"`. This prevents a surprisingly common mistake: nonempty strings are truthy in Python.

If `measured` is false, a numeric count is forbidden and the result is `UNMEASURED`.

If the gene was measured, a valid nonnegative integer count is required. Zero becomes `MEASURED_ZERO`; a positive value becomes `MEASURED_DETECTED`.

Our second function counts observations and unique donor IDs separately:

```python

def replication_summary(donor_ids: list[str]) -> dict[str, int]:
    if not donor_ids or any(type(d) is not str or not d.strip() for d in donor_ids):
        raise ValueError("donor_ids must contain valid nonempty donor IDs")
    return {"technical_rows": len(donor_ids), "biological_n": len(set(donor_ids))}
```

`len(donor_ids)` counts rows. `len(set(donor_ids))` counts distinct donor identifiers. A production system would also authenticate donor identity and model its experimental structure; this function only illustrates the counting rule.

The third function implements the example decision policy:

```python

def evidence_verdict(source_status, required=("study_a", "study_b")):
    if not required or len(set(required)) != len(required):
        raise ValueError("required studies cannot be empty or duplicated")
    present = [source_status[s] for s in required if s in source_status]
    if "FAIL" in present:
        return "FAIL"
    if len(present) < len(required) or "NOT_ESTIMABLE" in present:
        return "NOT_ESTIMABLE"
    return "PASS"
```

*This last excerpt shows the decision logic only; the repository version additionally checks the argument types and allowed status values. Run the full version from the repository.*

## 4. What does a regression test look like?

A regression test asks: “If somebody changes this code tomorrow, will this scientific rule still hold?”

We use Python's `pytest` package. For example:

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

The example is intentionally stark: **1,000 computer-generated rows still represent only two distinct fictional donor IDs**.

![Fictional donor accounting contrasts 1000 computational rows with 2 independent donors](https://raw.githubusercontent.com/dushyant-mishra/scientific-regression-demo/main/figures/figure_4_donor_vs_rows.png)

*Figure 2. Generated from an actual invocation of the included donor-counting function. This is a teaching example of counting units, not a statistical analysis of real RNA observations.*

For cross-study evidence:

```python

def test_insufficient_second_study_cannot_pass():
    statuses = {"study_a": "PASS", "study_b": "NOT_ESTIMABLE"}
    assert evidence_verdict(statuses) == "NOT_ESTIMABLE"
```

The complete `tests/test_science_rules.py` includes ten behavior tests, including edge cases discovered during independent review: invalid assay flags, an empty required-study list, and a known failed study alongside absent evidence.

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

![RED versus GREEN pytest runs: four pass and six fail before repair; ten pass afterward](https://raw.githubusercontent.com/dushyant-mishra/scientific-regression-demo/main/figures/figure_2_actual_red_green.png)

*Figure 3. Actual local pytest JUnit testcase counts. The intentionally defective implementation failed six tests; all ten passed against the repaired code. The chart reads `outputs/results.json`, which was generated by parsing `outputs/red_pytest.xml` and `outputs/green_pytest.xml`—not by entering expected numbers into the figure script.*

Why is this important? **A test that has never demonstrated it can catch a defect gives limited reassurance.** RED is valuable because it shows the test notices the kind of error it claims to guard against. GREEN shows that the repaired software satisfies those same tests.

## 6. The independent reviewer finds another bug

Our first version of this tutorial passed its tests and produced a convincing before/after chart. But a separate review found something embarrassing: the result-reporting script had hard-coded the numbers shown in the figure.

If another test failed tomorrow, the chart could still display yesterday's numbers.

That would make a tutorial about reproducibility less reproducible.

The updated implementation fixes this in three ways:

1. `run_demo.py` executes two subprocesses and produces JUnit XML reports for both.
2. `junit_results.py` counts the actual `<testcase>` records and their failure/error elements. An empty report is rejected.
3. `make_figures.py` builds its bars from the parsed JSON results rather than fixed numeric arrays.

We added an adversarial regression test: change the XML from two passes to one pass plus one failure, **without changing its misleading summary header**. The parser must report the actual testcase results. Another test changes input result counts and checks that the chart's bar data change too.

This is a useful lesson about AI agents and software audits: **a green test suite does not establish that the tests, reports, or charts are themselves correct**. Those components also need checks.

## 7. Why GitHub if we can run the tests locally?

Everything above can run on a laptop. GitHub is not necessary to compute a pytest result.

The practical reason for GitHub is what happens *after* the first successful run.

Imagine one person changes how the CSV is parsed. An agent refactors the functions the next day. A collaborator adds another gene panel the week after. Someone might accidentally undo a repaired rule. If tests run only when a person remembers, the mistake may go unnoticed.

GitHub stores the code and change history. **GitHub Actions** can rerun the defined checks automatically on pushes and pull requests. It also leaves reviewable logs linked to the exact Git revision.

Local tests tell us whether code passes *here and now*. Repository CI tells us whether the code committed to a shared revision still satisfies the tests. Neither one alone proves that a biological claim is true.

![Vertical workflow from defining a biological rule to tests, repair, GitHub Actions and evidence review](https://raw.githubusercontent.com/dushyant-mishra/scientific-regression-demo/main/figures/figure_3_workflow.png)

*Figure 4. A compact workflow you can adopt for RNA, DNA, or other computational research. Independent scientific review remains distinct from CI execution.*

## 8. Reproduce the tutorial on GitHub: step by step

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

**Step 3 — Rebuild the fictional dataset and analyze it.**

```bash
python generate_fictional_data.py
python analyze_fictional_rna.py
```

This writes `data/fictional_rna_observations.csv` and summary receipts in `outputs/`. In the included example, Study B has **six `UNMEASURED` records for gene_3 and zero measured-zero records for that gene**. Those values come from the actual CSV processing code.

**Step 4 — Run the full test suite.**

```bash
python -m pytest -q
```

The version documented in this article has **18 passing tests** in a local run: ten behavior tests, four data/integration tests, and four result-reporting tests. Your results may differ if you modify the code or add tests.

**Step 5 — Reproduce the RED/GREEN evidence and figures.**

```bash
python run_demo.py
python make_figures.py
```

The RED process is *supposed to fail its tests*. `run_demo.py` captures that expected failure and verifies that the GREEN process succeeds. It does **not** temporarily overwrite the production source file. See the `outputs/` JUnit XML files for the actual executed results.

**Step 6 — Create a change on a branch.** If you forked the repository, create a branch in your copy, change one implementation rule, and push the branch. You can deliberately reintroduce the `not count` defect as an educational exercise, but do not merge broken code into a branch others rely on.

**Step 7 — Open a pull request.** GitHub's **Actions** tab will show the workflow named *Fictional RNA scientific regression checks*. It checks out the submitted revision, installs Python and dependencies, runs tests, reproduces RED/GREEN, and rebuilds the figures. The saved workflow artifacts contain result logs.

**Step 8 — Review the test result, not just the green icon.** Open the workflow log. Verify the number of tests executed, whether anything was skipped, and whether the scientific rule is actually tested. If your repository supports rulesets/branch protection, you can configure its regression workflow as a required check before merging.

I executed the original test evidence locally; this article does **not** claim that a hosted GitHub Actions run has already succeeded. You can inspect the repository's Actions tab for its current hosted status.

## 9. Using an AI coding agent responsibly

A stronger instruction than “write an RNA analysis pipeline” is:

> Build a test demonstrating that an unassayed gene cannot be reported as a measured zero. First show the failing behavior, repair only the implementation, and rerun the same test. Record the commands, outputs and source revision. Do not change the expected answer to make the test green.

Then give a second reviewer a different task:

> Try to break the repaired pipeline. Include false-like strings, invalid counts, empty required-study sets, duplicated observations and misleading test-report summaries. Make each discovered defect into a test. Distinguish problems in the data, the statistical assumptions, the source code and the result-reporting scripts.

The second reviewer should not merely repeat the first agent's claims. They should independently attempt to falsify them.

## 10. What passing tests *do not* prove

This fictional example does **not** test differential expression, causal regulation, disease association, statistical power or replication of any real gene. It does not prove that a donor-level estimator is correctly calibrated: it simply catches a donor-counting mistake. And combining source-level `PASS` labels is not a substitute for proper statistical modeling of multiple studies.

A test can faithfully implement the wrong scientific assumption. A passing CI build can therefore still contain an invalid scientific analysis. The safeguard is to make assumptions visible, include positive and negative controls, review the data provenance, and subject both code and tests to independent challenge.

## 11. Reuse and citation

All data in the tutorial are fictitious, and the code is released with the repository. The README gives the exact commands and explains the toy dataset.

If you reuse the code or its teaching example, cite the **repository at the exact commit you used**, because the repository can change. The repository includes a `CITATION.cff` file so GitHub can display **Cite this repository** where supported.

Suggested citation (replace the placeholder commit hash with the one you actually used):

> dushyant-mishra. (2026). *Scientific Regression Demo: Fictional RNA Data, Regression Tests, and GitHub Actions* [Computer software and teaching materials]. GitHub. https://github.com/dushyant-mishra/scientific-regression-demo (commit: `<COMMIT_SHA>`).

There is **no DOI assigned** to this demonstration at the time of writing. If a permanent archived release/DOI is created in the future, use that release's citation metadata rather than inventing a DOI now. This Medium article can be cited separately by its final publication URL and date.

## Final thought

The most interesting part of this exercise wasn't that an AI agent could write a Python test. It was that a later review found a reporting defect **in the very code we were using to demonstrate reproducibility**.

We did not need a bigger model to fix that. We needed a clear rule, a falsifying test, authentic output, and another independent look.

For computational biology, that is a powerful habit to build:

**Define the scientific distinction → write the test → demonstrate failure → repair → rerun → review independently → protect against regression on GitHub.**

*Disclosure: Tutorial counts and figures come from executed local Python/pytest runs on fictional inputs. No real patient, human RNA/DNA data, biological findings, or verified hosted GitHub Actions outcomes are presented.*
