# The Code Runs. But Is the Science Right?

*An RNA analysis can finish without errors and still change the meaning of the data. Here is how a small Python test can catch the mistake—and how to keep it from coming back.*

Imagine bringing together RNA measurements from two studies. One study measured a particular gene. The other never included that gene in its assay.

You ask an AI coding assistant to combine the files. The script runs. It produces a tidy table and a plot. Nothing crashes.

But the table now contains a zero for the gene that the second study never measured.

That zero looks ordinary. It isn't.

A **measured zero** means the assay was performed and detected no transcripts in that observation. **Not measured** means there is no observation to interpret. If we turn the second case into the first, we have quietly invented data. A program can do that without producing a single Python error.

This is the distinction I want to protect—not just for today's script, but whenever someone edits it later.

## One gene, three kinds of evidence

Consider this small example from a teaching dataset. The gene names and counts are invented, but the data-handling problem is common.

| Observation | Was the gene assayed? | RNA count | What we know |
|---|---|---:|---|
| Study A, cell_01, gene_3 | Yes | 4 | The assay detected RNA |
| Study B, cell_07, gene_3 | No | — | We have no measurement |
| Study A, cell_01, gene_2 | Yes | 0 | The assay detected none |

The first two rows concern the **same gene**. Study A detected RNA for `gene_3`; Study B did not assay `gene_3` at all. The last row illustrates something different: a real measured zero for `gene_2`. The dash is not a different way of writing zero. It means the gene wasn't assayed.

The complete example contains six donors and twelve cells. Study B never assays `gene_3`, so its six entries for that gene should stay *unmeasured*. The rest of the cells let us see positive counts and measured zeros side by side.

![RNA measurement matrix showing detected counts, measured zeros and unassayed genes](https://raw.githubusercontent.com/dushyant-mishra/scientific-regression-demo/main/figures/figure_1_rna_measurements_v2.png)

*Figure 1. Plus signs mark detected RNA; 0 means assayed but not detected; dashes mean the gene was not assayed. The figure comes from the included teaching dataset.*

It's easy to say, "Of course missing is not zero." The harder question is: **how do we make the software remember that distinction?**

## Turn the scientific rule into a test

We can put the expectation into a few lines of Python. The example repository has a function called `observation_state()` that receives two pieces of information: whether an assay was performed and the count, if one exists.

Here is a small test you can read even if you have never written one:

```python
from science_rules import observation_state

def test_zero_is_different_from_unmeasured():
    assert observation_state(measured=True, count=0) == "MEASURED_ZERO"
    assert observation_state(measured=False, count=None) == "UNMEASURED"
```

Read `assert` as **"this must be true."**

The first check says that a real assay with count zero must be classified as `MEASURED_ZERO`. The second says that a gene not assayed, with no count at all (`None` in Python), must be classified as `UNMEASURED`.

We haven't proved anything about gene expression. We have specified what the software is *allowed to say about the measurement*.

Now comes the useful part: we can see whether the test notices when code gets that meaning wrong.

## Make it fail on purpose

Suppose a coding assistant simplifies the classification logic to this:

```python
return "MEASURED_ZERO" if not count else "MEASURED_DETECTED"
```

It looks compact. It is also wrong.

In Python, both `0` and `None` behave as false-like values in that condition. The code never asks whether the gene was assayed. It returns `MEASURED_ZERO` in both cases.

The difference is plain: **Expected: `UNMEASURED`. Got: `MEASURED_ZERO`.** Our second `assert` fails. The test has caught a scientific error that wouldn't necessarily stop the analysis from running.

The [example repository](https://github.com/dushyant-mishra/scientific-regression-demo) preserves an intentionally defective implementation alongside the corrected one. It runs **the same ten behavior tests** against each version, without changing the expected answers.

![Test outcomes from the deliberately defective and corrected implementations](https://raw.githubusercontent.com/dushyant-mishra/scientific-regression-demo/main/figures/figure_2_test_results_v2.png)

*Figure 2. In the deliberately defective version, six of ten tests fail. In the corrected version, all ten pass. The ten tests cover three data-handling rules, not just the zero-versus-unmeasured example.*

The failures are a feature of this demonstration. A test that stays green even when we insert the very mistake it is supposed to detect would not give us much confidence.

This is what **regression testing** means here: checking that a known software behavior stays correct as the code changes. It has nothing to do with fitting a statistical regression model.

## A fix today isn't protection tomorrow

Imagine you catch the zero-versus-unmeasured bug and repair it. Next month, someone cleans up the data-loading code. Or an AI agent rewrites the function to make it faster. The original mistake could return, and a normal run might still finish successfully.

That's where GitHub Actions becomes useful.

GitHub stores the code and its revision history. A GitHub Actions workflow can rerun the tests automatically when a collaborator—or an AI coding agent—pushes a change or proposes one for review.

Instead of merely seeing that *the script ran*, the team can see whether the new version still respects the scientific rule. If the rule breaks, the check turns red and the log points to the failing test.

This doesn't require scientists to abandon AI-assisted coding. It gives the assistant a more meaningful target than "make the program run": **preserve this biological distinction, and show me the test that would catch you if you didn't.**

## The idea extends beyond missing RNA counts

Missing values are only one place where apparently tidy results can hide an incorrect assumption.

**Rows are not donors.** Imagine a table with 1,000 rows but only two distinct donor identifiers, each repeated 500 times. Counting rows and counting donors gives very different answers. Our second demonstration tests that distinction. It does not claim that counting IDs alone proves statistical independence.

![Bar chart comparing 1000 repeated rows with two distinct donor IDs](https://raw.githubusercontent.com/dushyant-mishra/scientific-regression-demo/main/figures/figure_4_donor_units_v3.png)

*Figure 3. These are constructed row labels, not 1,000 biological samples or an actual resampling experiment.*

**Missing evidence is not positive evidence.** In a third, separate exercise, we assign two studies simple labels such as `PASS` and `NOT_ESTIMABLE`. Under the exercise's chosen rule, one missing required result cannot silently become an overall `PASS`. Those labels are supplied for teaching; they are not calculated from the RNA counts, nor are they a general method of combining studies.

All three examples follow the same pattern: write down the scientific meaning that must survive a code change, then test it against an example that could break it.

## Try one test yourself

You don't have to understand the whole repository to try the central idea. Start with the [hands-on walkthrough](https://github.com/dushyant-mishra/scientific-regression-demo/blob/main/docs/tutorial/FIRST_TEST_WALKTHROUGH.md). It shows how to download the project, run a single test, introduce the wrong classification on purpose, and restore the correct answer. A separate optional exercise shows how the same mistake appears in GitHub Actions on your own fork.

The [full project](https://github.com/dushyant-mishra/scientific-regression-demo) includes the example RNA table, the correct and deliberately incorrect functions, the unchanged comparison tests, and the scripts that generate these figures. In the audited run on [27 October 2026](https://github.com/dushyant-mishra/scientific-regression-demo/actions/runs/40559492066), the full repository suite passed 26 tests; the separate ten-test demonstration produced six expected failures before repair and none afterward. Those are software-test results, not biological findings.

The materials are available under an [MIT license](https://github.com/dushyant-mishra/scientific-regression-demo/blob/main/LICENSE). If you reuse them, cite the repository at the commit you used; its [citation file](https://github.com/dushyant-mishra/scientific-regression-demo/blob/main/CITATION.cff) gives the software attribution.

You can also give an AI coding assistant a task like this:

> Write a test showing that a gene excluded from an assay cannot be reported as a measured zero. Show me the test failing on an intentionally wrong implementation before fixing the code. Keep the expected result unchanged.

Then ask another reviewer to try to break both the implementation *and the test*.

Passing tests cannot tell us whether the experimental design, statistical model, or biological interpretation is sound. Tests can faithfully enforce a mistaken assumption. The researcher still has to decide which assumptions are scientifically defensible.

But once we've made a defensible rule explicit, we don't have to rely on remembering it every time the code changes.

**A program running without errors answers a software question. Whether it has answered the scientific question is something we still need to check.**
