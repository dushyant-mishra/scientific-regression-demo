"""Teaching-only union merge: keep introduced zero padding separate from assays.

This is a small standard-library example, NOT an AnnData reimplementation or a
real single-cell integration method. Its assay panel comes from explicit flags
in the fixed fictional CSV; a real dataset needs independently checked metadata.
"""
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
import csv


@dataclass(frozen=True)
class CellPanel:
    study: str
    cell_id: str
    measured_counts: Mapping[str, int]
    assayed_genes: frozenset[str]


@dataclass(frozen=True)
class MergedValue:
    value: int
    measured: bool

    @property
    def introduced_zero(self) -> bool:
        return not self.measured


def union_merge(cells: Sequence[CellPanel]) -> tuple[tuple[str, ...], dict[tuple[str, str], dict[str, MergedValue]]]:
    """Return all genes across panels, with numeric padding AND a provenance mask.

    Assay coverage must be supplied explicitly. A filtered-out measured gene
    cannot silently be reinterpreted as unassayed; it triggers an error.
    """
    if not cells:
        raise ValueError("at least one cell with explicit assay coverage is required")

    union: set[str] = set()
    by_cell: dict[tuple[str, str], CellPanel] = {}
    for cell in cells:
        if not isinstance(cell, CellPanel):
            raise TypeError("each input must be a CellPanel with assay metadata")
        if not isinstance(cell.study, str) or not cell.study.strip() or not isinstance(cell.cell_id, str) or not cell.cell_id.strip():
            raise ValueError("study and cell_id must be nonempty strings")
        if type(cell.assayed_genes) is not frozenset:
            raise TypeError("assayed_genes must be an explicit frozenset, not missing or inferred")
        if not isinstance(cell.measured_counts, Mapping):
            raise TypeError("measured_counts must be a mapping")
        if not cell.assayed_genes or any(type(gene) is not str or not gene.strip() for gene in cell.assayed_genes):
            raise ValueError("assayed_genes must contain valid gene names")
        if set(cell.measured_counts) != cell.assayed_genes:
            raise ValueError("measured gene columns differ from the supplied assay coverage; check filtering/metadata")
        for count in cell.measured_counts.values():
            if type(count) is not int or count < 0:
                raise ValueError("each measured count must be a nonnegative integer")
        identity = (cell.study, cell.cell_id)
        if identity in by_cell:
            raise ValueError("duplicate study/cell identity")
        by_cell[identity] = cell
        union.update(cell.assayed_genes)

    genes = tuple(sorted(union))
    merged = {
        identity: {
            gene: MergedValue(cell.measured_counts[gene], True)
            if gene in cell.assayed_genes else MergedValue(0, False)
            for gene in genes
        }
        for identity, cell in sorted(by_cell.items())
    }
    return genes, merged


def load_fictional_cells(path: Path | None = None) -> list[CellPanel]:
    """Build per-cell expression panels from validated, explicitly flagged CSV.

    The fixture includes unassayed rows for teaching; remove those rows from
    each per-cell matrix, retaining their assay flags as separate coverage.
    """
    from analyze_fictional_rna import analyze
    from generate_fictional_data import ROOT

    path = path or ROOT / "data" / "fictional_rna_observations.csv"
    analyze(path)  # Validate the fixed 36-row fixture before any transformation.
    measurements: dict[tuple[str, str], dict[str, int]] = {}
    panels: dict[tuple[str, str], set[str]] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            key = (row["study"], row["cell_id"])
            counts = measurements.setdefault(key, {})
            panel = panels.setdefault(key, set())
            if row["assayed"] == "true":
                panel.add(row["gene"])
                counts[row["gene"]] = int(row["count"])
    return [
        CellPanel(study, cell_id, measurements[(study, cell_id)], frozenset(genes))
        for (study, cell_id), genes in sorted(panels.items())
    ]


def main() -> None:
    genes, merged = union_merge(load_fictional_cells())
    real_zero = merged[("study_a", "cell_01")]["gene_2"]
    introduced_zero = merged[("study_b", "cell_07")]["gene_3"]
    measured_count = merged[("study_a", "cell_01")]["gene_3"]
    print("Union of genes:", ", ".join(genes))
    print(f"Study A / cell_01 / gene_2: value={real_zero.value}, measured={real_zero.measured}")
    print(f"Study B / cell_07 / gene_3: value={introduced_zero.value}, measured={introduced_zero.measured}")
    print(f"Study A / cell_01 / gene_3: value={measured_count.value}, measured={measured_count.measured}")
    print("A zero-only matrix cannot tell the first two cases apart. Keep the measured mask.")


if __name__ == "__main__":
    main()
