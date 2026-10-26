"""Independent integrity checks for the previous hardcoded-figure bug."""
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from junit_results import parse_junit


def test_junit_tally_is_read_from_real_testcase_nodes(tmp_path):
    p = tmp_path / "demo.xml"
    p.write_text('''<testsuite><testcase name="a"/><testcase name="b"><failure/></testcase><testcase name="c"><error/></testcase><testcase name="d"><skipped/></testcase></testsuite>''')
    assert parse_junit(p) == {"total": 4, "passed": 1, "failed": 1, "errors": 1, "skipped": 1}


def test_changed_testcase_changes_report_even_if_suite_header_lies(tmp_path):
    p = tmp_path / "changing.xml"
    p.write_text('<testsuite tests="99" failures="0"><testcase name="a"/><testcase name="b"/></testsuite>')
    assert parse_junit(p)["passed"] == 2
    p.write_text('<testsuite tests="99" failures="0"><testcase name="a"><failure/></testcase><testcase name="b"/></testsuite>')
    out = parse_junit(p)
    assert out["passed"] == 1 and out["failed"] == 1 and out["total"] == 2


def test_empty_report_is_rejected(tmp_path):
    p = tmp_path / "empty.xml"
    p.write_text('<testsuite tests="0"/>')
    with pytest.raises(ValueError):
        parse_junit(p)


def test_chart_bars_track_changed_report_counts():
    from make_figures import test_bar_counts
    a = {"red": {"passed": 4, "failed": 6, "errors": 0}, "green": {"passed": 10, "failed": 0, "errors": 0}}
    assert test_bar_counts(a) == [(4, 6), (10, 0)]
    b = {"red": {"passed": 2, "failed": 8, "errors": 0}, "green": {"passed": 10, "failed": 0, "errors": 0}}
    assert test_bar_counts(b) == [(2, 8), (10, 0)]
