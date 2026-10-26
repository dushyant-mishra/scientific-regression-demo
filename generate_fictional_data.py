"""Generate deliberately fictional RNA count observations for this tutorial.

No real genes, donors, subjects, or sequencing data are used.
"""
import csv
from pathlib import Path

GENES = ("FIC-A01", "FIC-B02", "FIC-C03")  # Invented, not real gene symbols
FIELDNAMES = ("study", "donor_id", "cell_id", "gene", "assayed", "count")
ROOT = Path(__file__).resolve().parent


def rows():
    for index in range(1, 7):
        study = "STUDY_A" if index <= 3 else "STUDY_B"
        donor = f"DONOR_{index:02d}"
        for cell_index in (1, 2):
            cell = f"FIC_CELL_{index:02d}_{cell_index}"
            # Deterministic fictional values chosen to demonstrate zeros and detection.
            a = 12 if index == 1 and cell_index == 1 else 3 + index + cell_index
            b = 0 if (index + cell_index) % 2 == 0 else index + 1
            c = 4 if index == 1 and cell_index == 1 else (index + cell_index) % 4
            for gene, count in zip(GENES, (a, b, c)):
                assayed = not (study == "STUDY_B" and gene == "FIC-C03")
                yield {
                    "study": study,
                    "donor_id": donor,
                    "cell_id": cell,
                    "gene": gene,
                    "assayed": "true" if assayed else "false",
                    "count": str(count) if assayed else "",
                }


def main():
    dest = ROOT / "data" / "fictional_rna_observations.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows())
    print(f"Wrote {dest.relative_to(ROOT)}: 36 fictional gene/cell observations")


if __name__ == "__main__":
    main()
