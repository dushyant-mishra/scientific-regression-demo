"""INTENTIONALLY WRONG: used ONLY to demonstrate a failing test suite.

Do not use this module to analyze any study.
"""


def observation_state(*, measured: bool, count: int | None) -> str:
    # BUG: both None and zero are false-like; the assay flag is ignored.
    return "MEASURED_ZERO" if not count else "MEASURED_DETECTED"


def replication_summary(donor_ids: list[str]) -> dict[str, int]:
    # BUG: technical observations are presented as independent donors.
    return {"technical_rows": len(donor_ids), "biological_n": len(donor_ids)}


def evidence_verdict(
    source_status: dict[str, str],
    required: tuple[str, ...] = ("STUDY_A", "STUDY_B"),
) -> str:
    # BUG: any PASS wins, even when required evidence is absent or negative.
    return "PASS" if "PASS" in source_status.values() else "FAIL"
