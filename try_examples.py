"""Run three examples before exploring the full tests.

Usage: python try_examples.py
"""

from science_rules import evidence_verdict, observation_state, replication_summary


def main() -> None:
    print("1. Measured zero versus a gene not assayed")
    print("   gene_2, measured count 0:", observation_state(measured=True, count=0))
    print("   gene_3, not assayed:", observation_state(measured=False, count=None))

    print("\n2. Observation rows versus independent donors")
    donor_ids = ["donor_01"] * 500 + ["donor_02"] * 500
    counts = replication_summary(donor_ids)
    print("   Rows:", counts["technical_rows"])
    print("   Distinct donors:", counts["biological_n"])

    print("\n3. Missing study evidence")
    statuses = {"study_a": "PASS", "study_b": "NOT_ESTIMABLE"}
    print("   Combined status:", evidence_verdict(statuses))


if __name__ == "__main__":
    main()
