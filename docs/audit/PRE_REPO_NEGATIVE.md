# Pre-repository chart reporting defect — preserved historical negative

The **earliest** local demonstration (not the current GitHub repo) computed real test outcomes but included literal result counters:

```python
summary = {"red": {"passed": 3, "failed": 3, "exit_code": red.returncode},
           "green": {"passed": 6, "failed": 0, "exit_code": green.returncode}}
# Old figure script:
passes = [3, 6]
failures = [3, 0]
```

An independent reviewer mutated the defective code: pytest then reported **4 failed/2 passed**, but the old JSON/chart still said **3 failed/3 passed**. Preserve this as **H01/H02** and do not portray those graphs as observed variable counts.

The repair was already included in the first published PR: `run_demo.py` writes JUnit XML for RED and GREEN; `junit_results.py` counts `<testcase>` states and rejects empty reports; `make_figures.py` reads parsed outcomes; `tests/test_reporting_integrity.py` attacks misleading summaries and changing counts.

Pre-repository local packages `scientific_regression_github_demo.zip` and `scientific_regression_medium_article_kit.zip` exist in the original conversation but are **superseded historical artifacts**, not needed for current CI. Older figures/source must not replace current `main`. The later Git PR chain is preserved as normal Git history. This defect was intentionally removed from the reader-facing Medium article in PR #5; it belongs in this audit only.
