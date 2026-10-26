"""Integration checks actually read the published fictional CSV."""
from pathlib import Path

import pytest

from analyze_fictional_rna import analyze
from generate_fictional_data import GENES, ROOT, rows


def test_fictional_gene_names_only():
    assert GENES == ("FIC-A01", "FIC-B02", "FIC-C03")
    assert set(row["gene"] for row in rows()) == set(GENES)


def test_csv_preserves_assay_not_run_as_unmeasured():
    summary, metadata = analyze(ROOT / "data" / "fictional_rna_observations.csv")
    assert metadata["n_donors_total"] == 6
    assert metadata["observations"] == 36
    assert metadata["by_study"]["STUDY_A"] == {"cells": 6, "donors": 3}
    assert metadata["by_study"]["STUDY_B"] == {"cells": 6, "donors": 3}
    row = next(r for r in summary if r["study"] == "STUDY_B" and r["gene"] == "FIC-C03")
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
