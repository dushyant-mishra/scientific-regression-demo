"""Regression checks for numeric zero padding without fabricated measurements."""
import pytest

from merge_with_provenance import CellPanel, load_fictional_cells, union_merge


def test_same_numeric_zero_keeps_distinct_origins_in_fixed_fixture():
    genes, merged = union_merge(load_fictional_cells())
    assert genes == ("gene_1", "gene_2", "gene_3")
    real_zero = merged[("study_a", "cell_01")]["gene_2"]
    padded_zero = merged[("study_b", "cell_07")]["gene_3"]
    assert real_zero.value == padded_zero.value == 0
    assert real_zero.measured is True and real_zero.introduced_zero is False
    assert padded_zero.measured is False and padded_zero.introduced_zero is True
    assert merged[("study_a", "cell_01")]["gene_3"].value == 4
    assert merged[("study_a", "cell_01")]["gene_3"].measured is True


def test_union_retains_unique_genes_and_measured_zeros():
    a = CellPanel("A", "cell_1", {"shared": 3, "only_a": 0}, frozenset({"shared", "only_a"}))
    b = CellPanel("B", "cell_2", {"shared": 1, "only_b": 5}, frozenset({"shared", "only_b"}))
    genes, merged = union_merge([a, b])
    assert genes == ("only_a", "only_b", "shared")
    assert merged[("A", "cell_1")]["only_a"].measured is True
    assert merged[("B", "cell_2")]["only_a"].introduced_zero is True
    assert merged[("A", "cell_1")]["only_b"].introduced_zero is True
    assert merged[("B", "cell_2")]["only_b"].value == 5


def test_missing_assay_metadata_is_rejected_not_guessed():
    cell = CellPanel("A", "cell_1", {"gene_x": 0}, None)
    with pytest.raises(TypeError, match="assayed_genes"):
        union_merge([cell])


def test_filtered_measured_gene_is_not_mislabeled_unassayed():
    cell = CellPanel("A", "cell_1", {"gene_x": 2}, frozenset({"gene_x", "gene_y"}))
    with pytest.raises(ValueError, match="filtering/metadata"):
        union_merge([cell])


def test_count_outside_panel_is_not_accepted():
    cell = CellPanel("A", "cell_1", {"gene_x": 2, "gene_y": 0}, frozenset({"gene_x"}))
    with pytest.raises(ValueError, match="filtering/metadata"):
        union_merge([cell])


@pytest.mark.parametrize("bad_count", [None, -1, 3.5, True, "0"])
def test_invalid_measurement_rejected(bad_count):
    cell = CellPanel("A", "cell_1", {"gene_x": bad_count}, frozenset({"gene_x"}))
    with pytest.raises(ValueError, match="nonnegative integer"):
        union_merge([cell])


def test_duplicate_cell_identity_rejected():
    cell = CellPanel("A", "cell_1", {"gene_x": 0}, frozenset({"gene_x"}))
    with pytest.raises(ValueError, match="duplicate"):
        union_merge([cell, cell])


def test_empty_input_rejected():
    with pytest.raises(ValueError, match="at least one"):
        union_merge([])
