# Your first scientific regression test: an RNA zero that isn't a zero

This is a **hands-on guide** to the repository's [RNA data-handling analysis](../../README.md). It gives you the commands and edits to see a test catch a scientifically incorrect interpretation, and connects the exercise to the [actual results](../RESULTS_AND_INTERPRETATION.md).

**What you'll do:** run a working example; add one test; introduce a mistake; watch the test fail; restore the code; and, optionally, see GitHub catch the same change.

You don't need real RNA data or a GitHub account for the local exercise. The included measurements are invented for teaching.

## 1. Open the project on your computer

You need Python **3.11 or later** and a terminal. A terminal is simply a window where you can type a command: PowerShell on Windows, or Terminal on macOS/Linux.

Check whether Python is installed:

~~~text
python --version
~~~

If that does not work, try `py --version` (Windows) or `python3 --version` (macOS/Linux). Use whichever command works in the rest of this guide wherever it says `python`. If none works, install Python from [python.org](https://www.python.org/downloads/) and repeat the version check.

**Without Git:** Open the [project on GitHub](https://github.com/dushyant-mishra/scientific-regression-demo), select **Code → Download ZIP**, and extract the ZIP. Open a terminal in the extracted project folder. On Windows you can open that folder in File Explorer, type `powershell` into its address bar, and press Enter. On macOS, type `cd ` into Terminal, drag the project folder into the window, and press Enter. (On Linux, open a terminal inside the extracted folder using your file manager.)

**If Git is already installed:** You can instead run:

~~~bash
git clone https://github.com/dushyant-mishra/scientific-regression-demo.git
cd scientific-regression-demo
~~~

Either method works. You should now be inside the folder containing `science_rules.py`, `requirements.txt`, and `try_examples.py`.

## 2. Run the built-in example

Install the two packages used by this project:

~~~bash
python -m pip install -r requirements.txt
~~~

Then run:

~~~bash
python try_examples.py
~~~

The first example should include:

~~~text
gene_2, measured count 0: MEASURED_ZERO
gene_3, not assayed: UNMEASURED
~~~

Why these answers? For `gene_2`, an assay was performed but detected zero transcripts. For `gene_3`, no assay was performed, so there is no count to interpret. These are different scientific statements.

If Python reports that it cannot find `try_examples.py`, you are probably in the wrong folder. Open the project folder in your file manager and reopen the terminal there. If `pytest` cannot be imported later, rerun the installation command above using the same Python command.

## 3. Write one test yourself

Open a plain-text code editor such as VS Code. Inside the existing `tests` folder, create a new file named exactly:

`test_my_first_rule.py`

Paste these lines into the file and save:

~~~python
from science_rules import observation_state


def test_unassayed_gene_is_not_a_measured_zero():
    result = observation_state(measured=False, count=None)
    assert result == "UNMEASURED"
~~~

Read the last line as: **"I expect an unassayed gene to be reported as unmeasured."** If the program reports something else, the test must fail.

With your terminal still in the main project folder, run only your new test:

~~~bash
python -m pytest -q tests/test_my_first_rule.py
~~~

You should see **1 passed**. A function whose name starts with `test_` is recognized by the `pytest` testing tool; `assert` states an expected outcome.

## 4. Break the code, then repair it

Open `science_rules.py`, find the function `observation_state()`, and locate this one line:

~~~python
return "UNMEASURED"
~~~

Temporarily change **only that line** to:

~~~python
return "MEASURED_ZERO"
~~~

Save the file and run **the same** test command again:

~~~bash
python -m pytest -q tests/test_my_first_rule.py
~~~

You should now see **1 failed**, with an assertion indicating that `MEASURED_ZERO` did not equal the expected `UNMEASURED`.

Nothing is wrong with pytest: it has noticed the exact scientific mistake you introduced. Restore the line to `return "UNMEASURED"`, save, and rerun. You should see **1 passed** again.

**Important:** Do not change the test's expected answer just to turn a failure green. Keep the scientific rule fixed; repair the code.

You have just demonstrated the central idea: a test that is capable of rejecting an incorrect scientific interpretation.

## 5. Explore the larger demonstration

The included repository has a deliberately wrong implementation, `science_rules_buggy.py`, and a corrected one, `science_rules.py`. Rather than editing files back and forth, this command runs the same existing ten behavior tests against both:

~~~bash
python run_demo.py
~~~

The expected comparison is:

~~~text
RED: 4 passed, 6 failed, 0 errors
GREEN: 10 passed, 0 failed, 0 errors
~~~

The **RED failures are intentional**; the program `run_demo.py` still completes successfully because it checks that the negative example really fails and the repaired one passes.

Run the broader suite with:

~~~bash
python -m pytest -q
~~~

At the [audited revision from 27 October 2026](https://github.com/dushyant-mishra/scientific-regression-demo/commit/7483d44556a0ec7a7e5aad1e576240f2663659ca), there were **26 passing repository tests**. Your run may have **27** if you kept your new test, or a different number if the project has changed. This is *not* the same as the ten-test RED/GREEN comparison.

To regenerate the figures, run `python generate_fictional_data.py`, `python analyze_fictional_rna.py`, and then `python make_figures.py`.

## 6. Optional: see GitHub Actions catch a mistake

Local tests depend on somebody remembering to run them. GitHub Actions can check again when someone changes code.

You can do this optional exercise entirely in a browser. You will need a GitHub account and your own **fork**, meaning your own copy of the project. Do **not** open a deliberately broken pull request against the original author's repository.

1. Open the [original project](https://github.com/dushyant-mishra/scientific-regression-demo) on GitHub and select **Fork → Create fork**. Navigate to **your** fork, not the original repository.
2. Use the branch selector (normally labeled `main`) and create a branch called `practice/first-science-test`. Make sure you are viewing this branch before editing any file.
3. Open `science_rules.py`, use the edit control, and change `return "UNMEASURED"` to `return "MEASURED_ZERO"`. Commit the change to your **practice branch**, not `main`.
4. Open **Actions** in your fork. GitHub may ask you to enable workflows on a newly forked repository. Find the run named **RNA scientific regression checks** for your practice-branch commit. It should **fail**, because the unchanged tests detect the deliberately broken rule.
5. Open that run, select the **tests** job, and expand **Run all regression and reporting tests**. Look for the failing zero-versus-unmeasured test.
6. Restore `return "UNMEASURED"` on the **same branch**, commit again, and inspect the new Actions run. The full check should now **pass**.

You don't need to open or merge a pull request to learn from these two runs. If you decide to open a practice PR, select **your fork's `main`** as the base—never the original project.

The workflow also deliberately runs the broken teaching comparator in a separate step. Its expected six RED test failures appear **inside a successful workflow**. That is different from the overall workflow failing because a real regression was committed to the practice branch.

## 7. Take the idea to your own data

Choose a rule from your analysis that could be silently violated. Write it first in ordinary scientific language. Then design two small example inputs: one that must be accepted and one that must be rejected.

A good first question is not "Can the model run?" but **"What scientifically incorrect answer would my code be capable of producing without crashing?"**

A passing test doesn't prove that the experimental design, statistics, or biological conclusion is valid. It protects the *specific behavior you decided to test*. Review that decision as carefully as the code.

### A small glossary

**Regression test:** a check that software still behaves as intended after code changes—not statistical regression.

**Assertion:** a statement that must be true for a test to pass.

**Commit:** a saved version of files in Git.

**Branch:** an isolated line of changes that you can review before merging.

**GitHub Actions:** an automated process that runs checks for code changes.

**Pull request:** a proposal to incorporate changes from one branch into another; you can review it without merging it.
