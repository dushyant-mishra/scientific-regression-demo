# Editorial graphics scientific and accessibility qualification — 27 October 2026

## Scope and custody

This qualification records two new source-derived teaching diagrams in **both landscape and independently composed mobile portrait** versions (eight total SVG/PNG assets). The earlier prototype and its audit are not presented as publication ready. Historical figure v2/v3 files required by the audit validator remain tracked and untouched.

Canonical source: \`make_editorial_figures.py\`. Inputs: \`data/fictional_rna_observations.csv\` and \`outputs/results.json\`. Optional renderer dependencies: \`requirements-editorial.txt\`. CI generates figures before running tests; there is no external RNA measurement or model-inferred label in these illustrations.

## Science cross-check

- Study A / \`cell_01\` / \`gene_3\`: **assayed**, observed count **4**. This is the *same gene* Study B lacks.
- Study B / \`cell_07\` / \`gene_3\`: **not assayed**, **blank** count. The entire Study B block has six unassayed \`gene_3\` entries.
- Study A / \`cell_01\` / \`gene_2\`: **assayed**, count **0**; shown separately as a *real measured zero*.
- Same ten behavior tests with the expected answers unchanged: intentionally buggy RED **4 pass / 6 fail**, corrected GREEN **10 pass / 0 fail**. The test tiles show counts, not individual test identity or biological significance.
- The donor-ID example elsewhere in the article continues to use the distinct v3 figure and is explicitly a different constructed example.

## Publication files

| Story | Desktop / wide | Portrait for Medium/mobile |
| --- | --- | --- |
| RNA measurement semantics | \`figures/editorial_01_rna_evidence_landscape_v1.png\` and matching SVG | \`figures/editorial_01_rna_evidence_mobile_v1.png\` and matching SVG |
| Scientific rule tests | \`figures/editorial_02_test_tripwire_landscape_v1.png\` and matching SVG | \`figures/editorial_02_test_tripwire_mobile_v1.png\` and matching SVG |

The article embeds the **portrait PNGs**, which retain readable type when displayed in a ~390-pixel column. PNG exports are 1600 px wide on desktop and 1200 px wide in portrait; SVG masters have embedded \`title\` and \`desc\`, visible text rather than flattened glyph outlines, and direct labels.

## Accessibility checks

All eight configured small-text foreground/background color pairs exceed the standard 4.5:1 contrast requirement. Measured WCAG 2 luminance contrast ratios, rounded:

| Pair | Ratio |
|---|---:|
| Dark navy / near-white canvas | 14.50:1 |
| Muted dark text / canvas | 7.35:1 |
| Purple / lavender | 5.40:1 |
| Dark teal / mint | 5.26:1 |
| Dark amber / cream | 5.18:1 |
| White / red tile | 6.39:1 |
| White / teal tile | 5.73:1 |
| White / dark navy bar | 12.29:1 |

Colors are supplemented with explicit labels, a dash versus numeric values, and ✓ / × tile symbols. SVG masters include descriptive metadata. The mobile layouts have a **minimum authored font size of 29 units in a 900-unit-wide viewBox**, corresponding to ~12.6 display pixels at 390 px, with most essential text much larger.

## Reproducibility and guardrails

\`tests/test_editorial_figure_integrity.py\` checks source-specific scientific facts, test totals, SVG title/description, PNG dimensions, mobile typographic floor, exact article-facing labels, and contrast ratios; it also mutates the assay flag to ensure the fixture qualifier rejects a scientifically inconsistent figure input.

The source figure generator rejects missing/nonconforming assay identities, missing \`gene_3\` coverage, mismatched test census, GREEN failures, or foreground/background contrast below 4.5:1.

The graphics are **explanatory illustrations**, not assay photos, new biological results, or statistical validation. The illustrated detected count uses symbolic marks for the selected count and should not be interpreted as a photomicrograph or an RNA molecule calibration.

## Remaining acceptance limitations

- Hosted CI verifies regeneration and scientific contracts, **not** actual Medium website rendering.
- The 390-pixel preview was inspected in the rendering environment; a real mobile browser and real novice user have not been tested.
- Do not treat the figure's synthetic counts or software test passes as evidence of differential expression, significance, donor independence, or general cross-study validity.
- Subsequent edits must rerun the source generator, the figure-integrity tests, and the historical audit validator before merging.
