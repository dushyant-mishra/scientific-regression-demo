# Execution playbook: reproduce without rereading old chats

Use a clean Python 3.11+ environment and Git. Example commands:

```bash
git clone https://github.com/dushyant-mishra/scientific-regression-demo.git
cd scientific-regression-demo
python -m pip install -r requirements.txt
python try_examples.py
python generate_fictional_data.py
python analyze_fictional_rna.py
python -m pytest -q
python scripts/validate_lane_audit.py
python run_demo.py
python make_figures.py
```

## What to expect

1. `try_examples.py`: a measured zero is `MEASURED_ZERO`, an unassayed gene is `UNMEASURED`, the separate 1,000-row repeat example has only two distinct donor IDs, and a missing source yields `NOT_ESTIMABLE`.
2. `generate_fictional_data.py`: deterministically writes CSV. `analyze_fictional_rna.py`: 36 records, six donors/twelve cells, study B unassayed `gene_3`. Baseline `outputs/fictional_summary.csv` contains six unassayed `study_b/gene_3`, zero observed zeros for that gene in study B.
3. `python -m pytest -q`: at original baseline **22 passed**; after audit/handoff, new audit tests increase the count. Report the actual current number; don't paste 22 as though it's timeless.
4. `python run_demo.py`: intentionally buggy implementation RED **4 pass/6 fail**, repaired implementation GREEN **10 pass/0 fail**. The command should return success if the *expected* RED negative and GREEN positive occur.
5. `python scripts/validate_lane_audit.py`: audit provenance, saved JUnit counts and source hashes must be internally consistent.
6. `python make_figures.py`: builds four pairs of PNG/SVG. Review actual rendered figures at both desktop and narrow widths; inspect image references in README and article.
7. `git status --short`: determine whether reproducibility steps changed tracked outputs. Either make a purposeful commit or explain source-of-drift; don't silently submit regenerated changes.

## Evidence chain

```text
source CSV -> strict reader -> analysis_summary + summary CSV
           -> science_rules + behavior tests -> pytest
buggy/fixed modules -> JUnit testcase XML -> results.json -> RED/GREEN Figure 2
CSV -> Figure 1; donor_count example -> Figure 4
current code + figures + article -> push/PR -> GitHub Actions exact-head run
```

Useful files: `outputs/{red,green}_pytest.xml`, `outputs/results.json` source/JUnit SHA-256, `outputs/{red,green}_run.txt`, `docs/audit/BASELINE_20261027.json`, [defect register](../audit/DEFECT_REGISTER.csv). Raw numbers are **local** saved receipts; use GitHub's Actions run link for hosted CI.

## Common non-errors / genuine errors

- **Expected:** the deliberately faulty implementation fails six tests in RED. A green GitHub workflow depends on the **wrapper** confirming this expected failure.
- **Unexpected:** GREEN fails, tests changed between two runs, assay-missing coerces to zero, source hash doesn't match result receipt, CSV schema invalid, article points to nonexistent or stale figure, or audit manifest is altered.
- **Not established:** genuine donor-level statistical precision, disease association, causal biology, external scientific acceptance or Medium publication.

## Reuse gate

Before new implementation or rerun: check `git rev-parse HEAD`, current PR/CI status, `docs/audit/DEFECT_REGISTER.csv`, and changed files. A new audit must identify a new observation; historical repairs should be referenced, not repeated.
