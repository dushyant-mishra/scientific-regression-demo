"""Read the fictional CSV and summarize the *measurement statuses* (not biology)."""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from generate_fictional_data import FIELDNAMES, GENES, ROOT
from science_rules import observation_state


def analyze(input_file: Path) -> tuple[list[dict], dict]:
    counters = defaultdict(Counter)
    donor_by_study = defaultdict(set)
    cells_by_study = defaultdict(set)
    seen = set()
    with input_file.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDNAMES:
            raise ValueError("fictional CSV header differs from frozen example schema")
        for row in reader:
            if row["gene"] not in GENES:
                raise ValueError("unexpected or non-fictional gene symbol")
            study, donor, cell, gene = (row[k] for k in ("study", "donor_id", "cell_id", "gene"))
            if study not in ("study_a", "study_b") or not donor or not cell:
                raise ValueError("invalid study, donor, or cell")
            identity = (study, cell, gene)
            if identity in seen:
                raise ValueError("duplicate measurement identity")
            seen.add(identity)
            if row["assayed"] not in ("true", "false"):
                raise ValueError("assayed must be lowercase true/false")
            measured = row["assayed"] == "true"
            raw = row["count"]
            if not measured and raw != "":
                raise ValueError("unmeasured RNA record must have an empty count")
            if measured and not (raw.isascii() and raw.isdecimal()):
                raise ValueError("measured RNA counts must be nonnegative integers")
            count = int(raw) if measured else None
            state = observation_state(measured=measured, count=count)
            counters[(study, gene)][state] += 1
            donor_by_study[study].add(donor)
            cells_by_study[study].add(cell)
    if len(seen) != 36:
        raise ValueError("expected exactly 36 illustrative measurement rows")
    if donor_by_study["study_a"] & donor_by_study["study_b"]:
        raise ValueError("donor identities overlap across studies")
    summary = []
    for (study, gene), ct in sorted(counters.items()):
        summary.append({
            "study": study, "gene": gene,
            "MEASURED_DETECTED": ct["MEASURED_DETECTED"],
            "MEASURED_ZERO": ct["MEASURED_ZERO"],
            "UNMEASURED": ct["UNMEASURED"],
        })
    # Count cells, not repeated gene/cell measurement rows, as technical observations.
    totals = {study: {"cells": len(cells), "donors": len(donor_by_study[study])}
              for study, cells in sorted(cells_by_study.items())}
    return summary, {"fictional": True, "observations": len(seen), "by_study": totals,
                     "n_donors_total": len(set().union(*donor_by_study.values()))}


def main():
    detail, meta = analyze(ROOT / "data" / "fictional_rna_observations.csv")
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    with (out / "fictional_summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(detail[0]))
        writer.writeheader()
        writer.writerows(detail)
    (out / "analysis_summary.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(meta, indent=2))
    for row in detail:
        print(row)


if __name__ == "__main__":
    main()
