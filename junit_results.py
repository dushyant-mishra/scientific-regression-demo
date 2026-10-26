"""Parse ACTUAL pytest JUnit testcase nodes. No expected test counts are encoded."""
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_junit(path: Path) -> dict[str, int]:
    root = ET.parse(path).getroot()
    if root.tag not in ("testsuite", "testsuites"):
        raise ValueError("expected pytest JUnit XML")
    cases = root.findall(".//testcase")
    if not cases:
        raise ValueError("empty test report is not acceptable")
    tally = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0, "total": len(cases)}
    for case in cases:
        if case.find("error") is not None:
            tally["errors"] += 1
        elif case.find("failure") is not None:
            tally["failed"] += 1
        elif case.find("skipped") is not None:
            tally["skipped"] += 1
        else:
            tally["passed"] += 1
    if sum(tally[k] for k in ("passed", "failed", "errors", "skipped")) != tally["total"]:
        raise AssertionError("bad tally")
    return tally
