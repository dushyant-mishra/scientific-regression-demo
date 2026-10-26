"""Run unchanged tests against buggy and corrected implementations.

Both executions create JUnit XML; results.json is derived ONLY from those reports.
No source files are rewritten/swapped as part of the demo.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from junit_results import parse_junit

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "outputs"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(label: str, module: str) -> dict:
    xml = OUTPUT / f"{label}_pytest.xml"
    env = os.environ.copy()
    env["SCIENCE_RULES_MODULE"] = module
    args = [sys.executable, "-m", "pytest", "-q", "tests/test_science_rules.py", f"--junitxml={xml}"]
    process = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True)
    (OUTPUT / f"{label}_run.txt").write_text(process.stdout + process.stderr, encoding="utf-8")
    result = parse_junit(xml)
    result["exit_code"] = process.returncode
    result["junit_sha256"] = digest(xml)
    return result


def main():
    OUTPUT.mkdir(exist_ok=True)
    red = run("red", "science_rules_buggy")
    green = run("green", "science_rules")
    if red["failed"] + red["errors"] == 0 or red["exit_code"] == 0:
        raise RuntimeError("RED run did not demonstrate a fault")
    if green["failed"] or green["errors"] or green["skipped"] or green["exit_code"]:
        raise RuntimeError("GREEN run did not pass completely")
    if red["total"] != green["total"]:
        raise RuntimeError("the before/after test census changed")
    result = {
        "scope": "FICTIONAL_DEMO_LOCAL_PYTEST_NOT_GITHUB_HOSTED_EVIDENCE",
        "test_module": "tests/test_science_rules.py",
        "red_source_sha256": digest(ROOT / "science_rules_buggy.py"),
        "green_source_sha256": digest(ROOT / "science_rules.py"),
        "red": red,
        "green": green,
    }
    (OUTPUT / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"RED: {red['passed']} passed, {red['failed']} failed, {red['errors']} errors")
    print(f"GREEN: {green['passed']} passed, {green['failed']} failed, {green['errors']} errors")
    print("All counts parsed from real JUnit testcase records.")


if __name__ == "__main__":
    main()
