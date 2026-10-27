"""Keep reader-facing analysis tables synchronized with the committed output CSV."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_results_match_executed_rna_classification():
    with (ROOT / "outputs/fictional_summary.csv").open(newline="", encoding="utf-8") as f:
        source = list(csv.DictReader(f))
    expected = {
        (row["study"], row["gene"]): (
            int(row["MEASURED_DETECTED"]), int(row["MEASURED_ZERO"]), int(row["UNMEASURED"])
        )
        for row in source
    }
    assert len(expected) == 6
    assert sum(sum(v) for v in expected.values()) == 36
    assert expected[("study_b", "gene_3")] == (0, 0, 6)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    section = readme.split("### What the analysis produces", 1)[1].split("## Verify the software behavior", 1)[0]
    displayed = {}
    for line in section.splitlines():
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) != 5 or parts[0] not in ("Study A", "Study B"):
            continue
        study = {"Study A": "study_a", "Study B": "study_b"}[parts[0]]
        gene = parts[1]
        displayed[(study, gene)] = tuple(map(int, parts[2:]))
    assert displayed == expected, "README analysis rows drifted from outputs/fictional_summary.csv"


def test_interpretation_totals_match_executed_rna_classification():
    with (ROOT / "outputs/fictional_summary.csv").open(newline="", encoding="utf-8") as f:
        source = list(csv.DictReader(f))
    totals = [
        sum(int(row[col]) for row in source)
        for col in ("MEASURED_DETECTED", "MEASURED_ZERO", "UNMEASURED")
    ]
    assert totals == [22, 8, 6]
    interpret = (ROOT / "docs/RESULTS_AND_INTERPRETATION.md").read_text(encoding="utf-8")
    assert "| **Total** | | **22** | **8** | **6** | **36** |" in interpret
    assert "not a statistical meta-analysis" in interpret
