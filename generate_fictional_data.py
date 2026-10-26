"""Create the small RNA count table used throughout the tutorial."""
import csv
from pathlib import Path

GENES = ("gene_1", "gene_2", "gene_3")
FIELDNAMES = ("study", "donor_id", "cell_id", "gene", "assayed", "count")
ROOT = Path(__file__).resolve().parent


def rows():
    # Six donors, with two cells per donor. The first three donors belong to study_a.
    for donor_number in range(1, 7):
        study = "study_a" if donor_number <= 3 else "study_b"
        donor = f"donor_{donor_number:02d}"

        for cell_number_within_donor in (1, 2):
            cell_number = (donor_number - 1) * 2 + cell_number_within_donor
            cell = f"cell_{cell_number:02d}"

            # Fixed teaching counts: some detected, some zero, and some unassayed.
            gene_1_count = (
                12 if donor_number == 1 and cell_number_within_donor == 1
                else 3 + donor_number + cell_number_within_donor
            )
            gene_2_count = (
                0 if (donor_number + cell_number_within_donor) % 2 == 0
                else donor_number + 1
            )
            gene_3_count = (
                4 if donor_number == 1 and cell_number_within_donor == 1
                else (donor_number + cell_number_within_donor) % 4
            )
            counts = (gene_1_count, gene_2_count, gene_3_count)

            for gene, count in zip(GENES, counts):
                assayed = not (study == "study_b" and gene == "gene_3")
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
    print(f"Wrote {dest.relative_to(ROOT)}: 36 gene/cell observations")


if __name__ == "__main__":
    main()
