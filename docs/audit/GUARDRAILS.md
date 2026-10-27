# Do-not-repeat constraints

1. Preserve exact past verdicts and PR CI heads. Rerun historical reviews only when a new, reproducible defect affects the current code; cite the prior defect ID.
2. Keep the deliberately broken `science_rules_buggy.py` as an **intentional teaching control**. Expected RED failures are not live-code failures.
3. Keep zero-versus-unassayed, donors-versus-rows, and missing-evidence-versus-PASS semantics. The toy cross-study policy is not statistical evidence synthesis.
4. Do not transfer real JEPA datasets/checkpoints or internal scientific audits into this unrelated public repository.
5. Use natural, beginner-friendly explanations; no repeated fictional-data disclaimers; no FIC-prefixed IDs; no introspective LLM editing narrative. User explicitly requested these edits in PRs #2/#3/#5.
6. Treat four properties separately: passing local tests, passing hosted CI on an exact commit, biological validity, and publication on Medium.
7. Regenerate *all* PNG and SVG figures after source/data changes; visually inspect text, clipping, axes and captions; validate GitHub raw image links and update versioned URL names where caching is relevant.
8. Make article code snippets runnable or explicitly labeled excerpts. Teach the first-run path `try_examples.py` → `science_rules.py` → `tests/test_science_rules.py`.
9. Confirm actual data numbers: 6 donors, 12 cells, 36 gene×cell rows, six unassayed `study_b/gene_3`. The 2-donor, 1,000-row example is entirely separate.
10. Preserve `CITATION.cff` and cite commit SHA; **no DOI exists**. Avoid creating a release, DOI, adding real data, or making public biological claims without new authorization.
11. Use branch/PR, exact-head CI, independent review for material changes. Do not merge a RED source variant into production code.
