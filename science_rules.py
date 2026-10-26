"""Three small *software rules* for a fictional RNA analysis.

These functions do not estimate differential expression or establish biology.
"""


def observation_state(*, measured: bool, count: int | None) -> str:
    """Classify a gene observation without turning missing assay support into zero."""
    if type(measured) is not bool:
        raise TypeError("measured must be a bool")
    if not measured:
        if count is not None:
            raise ValueError("an unmeasured observation must have no count")
        return "UNMEASURED"
    if type(count) is not int or count < 0:
        raise ValueError("a measured count must be a nonnegative integer")
    return "MEASURED_ZERO" if count == 0 else "MEASURED_DETECTED"


def replication_summary(donor_ids: list[str]) -> dict[str, int]:
    """Report row count separately from the number of distinct donor IDs."""
    if not donor_ids or any(type(d) is not str or not d.strip() for d in donor_ids):
        raise ValueError("donor_ids must contain valid nonempty donor IDs")
    return {"technical_rows": len(donor_ids), "biological_n": len(set(donor_ids))}


def evidence_verdict(
    source_status: dict[str, str],
    required: tuple[str, ...] = ("study_a", "study_b"),
) -> str:
    """An illustrative, *predeclared* rule for combining source-level statuses.

    An observed FAIL takes precedence; missing/NOT_ESTIMABLE blocks PASS.
    This is not a general meta-analysis procedure.
    """
    if (type(required) is not tuple or not required or
            any(type(x) is not str or not x for x in required) or
            len(set(required)) != len(required)):
        raise ValueError("required must be a nonempty tuple of unique study names")
    if type(source_status) is not dict:
        raise TypeError("source_status must be a dict")
    allowed = {"PASS", "FAIL", "NOT_ESTIMABLE"}
    present = [source_status[s] for s in required if s in source_status]
    if any(type(v) is not str or v not in allowed for v in present):
        raise ValueError("unknown status in a required study")
    if "FAIL" in present:
        return "FAIL"
    if len(present) < len(required) or "NOT_ESTIMABLE" in present:
        return "NOT_ESTIMABLE"
    return "PASS"
