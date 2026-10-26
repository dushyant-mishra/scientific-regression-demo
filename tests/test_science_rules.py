"""Deliberately simple scientific behavior tests with a switchable implementation.

SCIENCE_RULES_MODULE=science_rules_buggy is for the RED demonstration ONLY.
"""
import importlib
import os

import pytest

rules = importlib.import_module(os.environ.get("SCIENCE_RULES_MODULE", "science_rules"))


def test_01_zero_is_not_unmeasured():
    assert rules.observation_state(measured=True, count=0) == "MEASURED_ZERO"
    assert rules.observation_state(measured=False, count=None) == "UNMEASURED"


def test_02_technical_rows_are_not_independent_donors():
    x = ["DONOR_01"] * 500 + ["DONOR_02"] * 500
    assert rules.replication_summary(x) == {"technical_rows": 1000, "biological_n": 2}


def test_03_insufficient_second_study_cannot_pass():
    assert rules.evidence_verdict({"STUDY_A": "PASS", "STUDY_B": "NOT_ESTIMABLE"}) == "NOT_ESTIMABLE"


def test_04_positive_count_is_detected():
    assert rules.observation_state(measured=True, count=3) == "MEASURED_DETECTED"


def test_05_two_distinct_donors_count_as_two():
    assert rules.replication_summary(["D1", "D2"])["biological_n"] == 2


def test_06_two_required_studies_pass():
    assert rules.evidence_verdict({"STUDY_A": "PASS", "STUDY_B": "PASS"}) == "PASS"


def test_07_assay_flag_must_be_a_real_bool():
    with pytest.raises((TypeError, ValueError)):
        rules.observation_state(measured="false", count=0)


def test_08_empty_required_study_set_is_invalid():
    with pytest.raises(ValueError):
        rules.evidence_verdict({}, required=())


def test_09_known_failure_takes_precedence_over_missing_study():
    assert rules.evidence_verdict({"STUDY_A": "FAIL"}) == "FAIL"


def test_10_invalid_count_is_rejected():
    with pytest.raises((TypeError, ValueError)):
        rules.observation_state(measured=True, count=-1)
