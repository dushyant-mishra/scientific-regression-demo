"""Reject internally conflicting lineage in an otherwise well-formed RNA CSV.

This is a prospective data-integrity regression, not a reopened historical defect.
"""
import csv
from pathlib import Path

import pytest

from analyze_fictional_rna import analyze
from generate_fictional_data import FIELDNAMES, ROOT


def test_one_cell_cannot_have_genes_assigned_to_different_donors(tmp_path: Path):
    with (ROOT / "data" / "fictional_rna_observations.csv").open(
        newline="", encoding="utf-8"
    ) as stream:
        rows = list(csv.DictReader(stream))

    # Preserve the 36 measurement identities, six distinct donors and assay states.
    # Only one gene row in cell_01 is reassigned to donor_02.
    bad_row = next(
        row for row in rows
        if row["cell_id"] == "cell_01" and row["gene"] == "gene_1"
    )
    bad_row["donor_id"] = "donor_02"

    mutated = tmp_path / "conflicting_cell_donor.csv"
    with mutated.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    with pytest.raises(ValueError, match="cell.*multiple donors"):
        analyze(mutated)
