"""Validate the durable historical audit records without any network access."""
import csv
import hashlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]

# The frozen historical manifest retains the article's original Git blob SHA,
# but publication writing now lives outside the runnable analysis repository.
HISTORICAL_GIT_ONLY = {"MEDIUM_ARTICLE.md"}


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _junit(path):
    root = ElementTree.parse(path).getroot()
    if root.tag not in {"testsuite", "testsuites"}:
        raise AssertionError(f"not JUnit XML: {path}")
    cases = root.findall(".//testcase")
    if not cases:
        raise AssertionError(f"empty JUnit XML: {path}")
    result = dict(passed=0, failed=0, errors=0, skipped=0, total=len(cases))
    for case in cases:
        if case.find("error") is not None:
            result["errors"] += 1
        elif case.find("failure") is not None:
            result["failed"] += 1
        elif case.find("skipped") is not None:
            result["skipped"] += 1
        else:
            result["passed"] += 1
    return result


def validate(root=ROOT):
    manifest = json.loads((root / "docs/audit/BASELINE_20261027.json").read_text())
    assert manifest["schema"] == "scientific-regression-audit/v1"
    assert manifest["nature"] == "HISTORICAL_SNAPSHOT_NOT_CURRENT_VERDICT"
    assert re.fullmatch(r"[a-f0-9]{40}", manifest["frozen_baseline_commit"])
    assert len(manifest["baseline_artifacts"]) >= 35
    for path, fact in manifest["baseline_artifacts"].items():
        assert not Path(path).is_absolute() and ".." not in Path(path).parts, path
        assert re.fullmatch(r"[0-9a-f]{40}", fact["git_blob"]), path
        if path not in HISTORICAL_GIT_ONLY:
            assert (root / path).is_file(), f"Missing tracked historical path: {path}"
    prs = manifest["prs"]
    assert [r["pr"] for r in prs] == list(range(1, 7))
    for r in prs:
        assert r["conclusion"] == "success" and re.fullmatch(r"[a-f0-9]{40}", r["head_sha"])
        assert r["url"].endswith("/actions/runs/" + str(r["workflow_run"]))
    with (root / "docs/audit/DEFECT_REGISTER.csv").open(newline="") as f:
        defects = list(csv.DictReader(f))
    assert len(defects) >= 12 and len({d["id"] for d in defects}) == len(defects)
    assert {"H01", "H02", "H08", "H11"}.issubset({d["id"] for d in defects})
    with (root / "data/fictional_rna_observations.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 36
    assert len({r["cell_id"] for r in rows}) == 12
    assert len({r["donor_id"] for r in rows}) == 6
    assert {r["gene"] for r in rows} == {"gene_1", "gene_2", "gene_3"}
    missing = [r for r in rows if r["study"] == "study_b" and r["gene"] == "gene_3"]
    assert len(missing) == 6 and all(r["assayed"] == "false" and r["count"] == "" for r in missing)
    result = json.loads((root / "outputs/results.json").read_text())
    assert "LOCAL" in result["scope"] and "NOT_GITHUB_HOSTED" in result["scope"]
    for label, source in (("red", "science_rules_buggy.py"), ("green", "science_rules.py")):
        report = root / f"outputs/{label}_pytest.xml"
        assert result[f"{label}_source_sha256"] == _sha256(root / source)
        assert result[label]["junit_sha256"] == _sha256(report)
        tally = _junit(report)
        assert all(result[label][k] == v for k, v in tally.items())
        expected = manifest["baseline_metrics"][label]
        assert all(result[label][k] == v for k, v in expected.items())
    assert result["red"]["exit_code"] != 0 and result["green"]["exit_code"] == 0
    for name in ("figure_1_rna_measurements_v2", "figure_2_test_results_v2",
                 "figure_3_regression_workflow_v2", "figure_4_donor_units_v2"):
        assert (root / "figures" / (name + ".png")).is_file()
        assert (root / "figures" / (name + ".svg")).is_file()
    # Validate the active public scientific entrypoint, not an off-repository
    # Medium manuscript. The immutable baseline manifest remains unchanged.
    body = (root / "README.md").read_text()
    assert "6 donors" in body and "two-donor" in body
    assert "figure_1_rna_measurements_v2.png" in body
    assert (root / "docs/RESULTS_AND_INTERPRETATION.md").is_file()
    return {"prs": len(prs), "defects": len(defects), "rows": len(rows), "baseline_paths": len(manifest["baseline_artifacts"])}


if __name__ == "__main__":
    print("Historical audit checks:", json.dumps(validate(), sort_keys=True))
