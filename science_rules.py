"""Three data-handling rules used in the RNA regression-test tutorial.

The functions classify observations and check evidence labels. They do not
estimate RNA expression differences or establish a biological finding.
"""


def observation_state(*, measured: bool, count: int | None) -> str:
    """Distinguish a measured zero from a gene that was not assayed."""
    # A string such as "false" must not be mistaken for the Boolean False.
    if type(measured) is not bool:
        raise TypeError("measured must be a bool")

    if not measured:
        if count is not None:
            raise ValueError("an unmeasured observation must have no count")
        return "UNMEASURED"

    # Booleans are integers in Python, so require exactly int here.
    if type(count) is not int or count < 0:
        raise ValueError("a measured count must be a nonnegative integer")

    if count == 0:
        return "MEASURED_ZERO"
    return "MEASURED_DETECTED"


def replication_summary(donor_ids: list[str]) -> dict[str, int]:
    """Count observation rows and distinct donor IDs separately."""
    if not donor_ids:
        raise ValueError("donor_ids must contain valid nonempty donor IDs")

    for donor_id in donor_ids:
        if type(donor_id) is not str or not donor_id.strip():
            raise ValueError("donor_ids must contain valid nonempty donor IDs")

    return {
        "technical_rows": len(donor_ids),
        "biological_n": len(set(donor_ids)),
    }


def evidence_verdict(
    source_status: dict[str, str],
    required: tuple[str, ...] = ("study_a", "study_b"),
) -> str:
    """Apply the tutorial's rule for combining preassigned study statuses.

    A known FAIL wins; missing or NOT_ESTIMABLE evidence prevents PASS.
    This rule is an illustration, not a statistical meta-analysis method.
    """
    if type(required) is not tuple or not required:
        raise ValueError("required must be a nonempty tuple of unique study names")
    if any(type(name) is not str or not name for name in required):
        raise ValueError("required must be a nonempty tuple of unique study names")
    if len(set(required)) != len(required):
        raise ValueError("required must be a nonempty tuple of unique study names")
    if type(source_status) is not dict:
        raise TypeError("source_status must be a dict")

    allowed_statuses = {"PASS", "FAIL", "NOT_ESTIMABLE"}
    available_statuses = [
        source_status[study]
        for study in required
        if study in source_status
    ]
    if any(
        type(status) is not str or status not in allowed_statuses
        for status in available_statuses
    ):
        raise ValueError("unknown status in a required study")

    # A documented failure stays a failure, even if another study is missing.
    if "FAIL" in available_statuses:
        return "FAIL"

    # Never promote an absent or unevaluable study to PASS.
    if len(available_statuses) < len(required):
        return "NOT_ESTIMABLE"
    if "NOT_ESTIMABLE" in available_statuses:
        return "NOT_ESTIMABLE"

    return "PASS"
