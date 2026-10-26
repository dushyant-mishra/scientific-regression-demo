"""Integration checks actually read the published fictional CSV."""
from pathlib import Path

import pytest

from analyze_fictional_rna import analyze
from generate_fictional_data import GENES, ROOT, rows


def test_fictional_gene_names_only():
    assert GENES == ("gene_1", "gene_2", "gene_3")
    assert set(row["gene"] for row in rows()) == set(GENES)


def test_csv_preserves_assay_not_run_as_unmeasured():
    summary, metadata = analyze(ROOT / "data" / "fictional_rna_observations.csv")
    assert metadata["n_donors_total"] == 6
    assert metadata["observations"] == 36
    assert metadata["by_study"]["study_a"] == {"cells": 6, "donors": 3}
    assert metadata["by_study"]["study_b"] == {"cells": 6, "donors": 3}
    row = next(r for r in summary if r["study"] == "study_b" and r["gene"] == "gene_3")
    assert row["UNMEASURED"] == 6
    assert row["MEASURED_ZERO"] == 0
    assert row["MEASURED_DETECTED"] == 0
    assert sum(r["MEASURED_ZERO"] for r in summary) > 0


def test_generated_data_equal_to_checked_in_data(tmp_path):
    import csv
    file = ROOT / "data" / "fictional_rna_observations.csv"
    with file.open(newline="", encoding="utf-8") as stream:
        actual = list(csv.DictReader(stream))
    assert actual == list(rows())


def test_plain_language_identifiers_remain_consistent():
    # The article, dataset, charts and README use these exact fictional IDs.
    generated = list(rows())
    assert sorted({r["gene"] for r in generated}) == ["gene_1", "gene_2", "gene_3"]
    assert sorted({r["donor_id"] for r in generated}) == [f"donor_{i:02d}" for i in range(1, 7)]
    assert sorted({r["cell_id"] for r in generated}) == [f"cell_{i:02d}" for i in range(1, 13)]
    assert sorted({r["study"] for r in generated}) == ["study_a", "study_b"]
    donor_to_cells = {}
    for row in generated:
        donor_to_cells.setdefault(row["donor_id"], set()).add(row["cell_id"])
    assert all(len(cell_ids) == 2 for cell_ids in donor_to_cells.values())
