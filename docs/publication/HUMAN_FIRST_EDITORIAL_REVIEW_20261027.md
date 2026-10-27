# Human-first Medium rewrite — editorial review receipt (27 October 2026)

**Purpose:** revise the canonical Medium manuscript to read as an article for working biologists rather than a repository instruction manual. This receipt documents agent self-review; it is **not** an independent human comprehension test or a Medium editor preview.

**Baseline:** `7483d44556a0ec7a7e5aad1e576240f2663659ca` (26-test hosted CI green).
**Primary files:** `MEDIUM_ARTICLE.md` (new concise story), `docs/tutorial/FIRST_TEST_WALKTHROUGH.md` (standalone reproducible guide), `README.md` (correct navigation and current historical CI receipt).

## Iterative audit passes and actual corrections

**Pass 1 — Reader narrative and continuity.** The original manuscript (~3,665 words with 8 GitHub steps) placed terminal/Python installation before the reader's motivation, interrupted the scientific story with three disconnected software lessons, and repeated technical cautions. Rewrote it around one question: what if an unassayed RNA gene becomes a measured zero? Separated the end-to-end operational steps into a linked tutorial. On rereading the draft, the opening initially compared different genes where the prose promised the same gene; corrected the table to show `gene_3` assayed in Study A and unassayed in Study B, plus `gene_2` as an actual measured-zero example. Replaced a raw HTML link with Markdown.

**Pass 2 — Rendering and usability.** Caught escaped Markdown backticks (38 in the draft article, 72 in the guide), which would have shown literal punctuation instead of formatted inline code and fenced Python examples. Restored proper Markdown formatting in both files. Replaced the README's stale fragment link to the removed first-time setup section with a direct link to the standalone guide.

**Pass 3 — Scientific/source consistency.** Re-read the actual `science_rules.py`, `science_rules_buggy.py`, `tests/test_science_rules.py`, and `data/fictional_rna_observations.csv` against every central claim. Verified 36 measurement rows, six donor identifiers, twelve cells, three genes, six unassayed `study_b/gene_3` rows, and eight measured zeros. Confirmed the deliberately broken one-line function in the article matches `science_rules_buggy.py`. Confirmed the proposed two-assertion test agrees with the current correct function. Added the plain-language **Expected: UNMEASURED; Got: MEASURED_ZERO** consequence. Updated README's previously dated 25-test citation to the audited 26-test revision and preserved the earlier history elsewhere. Included lightweight MIT-license and `CITATION.cff` attribution.

**Pass 4 — Human reading rhythm / premature technical overload.** Reassessed paragraph lengths, section purpose, links, code quantity, and scientific disclaimers. Removed the full-suite test arithmetic from the Medium story while keeping a link to the hosted evidence, leaving operational counts in the README and beginner guide. Retitled the opening section as an intelligible biological question. The article now contains one concrete measurement table, two minimal code snippets, three data-grounded figures, and a short invitation to the independent walkthrough. No terminal setup is required to *read* the article.

## Publication and scientific constraints

- The three teaching examples remain separate: the six-donor RNA CSV; the two-donor-ID/1,000-constructed-row illustration; and the exercise with manually assigned `PASS`/`NOT_ESTIMABLE` labels.
- The article's regression test example is a readable, importable variant of the repository's first scientific behavior test. The full repository keeps its unchanged switchable ten-test suite for the intentionally RED and corrected GREEN comparison.
- Biological significance, statistical independence, differential expression, causal inference, medical validity, and general cross-study evidence synthesis are **not** established by these code tests.
- Source implementations, RNA data, figures, historical audit, recorded output and GitHub workflow are unchanged by this editorial rewrite.
- Publication on Medium, Medium mobile/desktop rendering, and a real human novice's end-to-end walkthrough are **not yet verified**.
- After review, require successful CI on the exact proposed PR head. Do not claim CI passing proves human readability.

## Acceptance conditions

1. The first illustration faithfully contrasts Study A's `gene_3` with Study B's missing assay and includes a true measured zero.
2. A reader can understand the idea before encountering Python setup instructions; the separate guide offers an executable local and optional fork/Actions path.
3. The Python example and reported intended defect match the actual correct/buggy modules, not invented outputs.
4. All Markdown links, fenced code, figure references and README navigation resolve in the repository.
5. The existing full suite, historical audit validation, and ten-test RED/GREEN demonstration remain successful on the PR head.
6. No claim of Medium publication or independent human user testing.
