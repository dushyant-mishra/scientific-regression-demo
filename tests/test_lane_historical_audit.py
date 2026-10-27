"""Ensure source data and retained audit receipts agree with the historical record."""
from scripts.validate_lane_audit import validate


def test_historical_audit_receipts_and_repaired_outcomes():
    evidence = validate()
    assert evidence["prs"] == 6
    assert evidence["rows"] == 36
    assert evidence["defects"] >= 12
