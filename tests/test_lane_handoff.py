"""The next coding agent can find a consistent, non-authorizing handoff."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_handoff_custody_and_entrypoints():
    record = json.loads((ROOT / "docs/handoff/ACTIVE_STATE.json").read_text())
    assert record["schema"] == "scientific-regression-lane-handoff/v1"
    assert record["takeover_start_commit"] == "a5dd0292d2fec1d3bc50878c566fc486f0f100bc"
    assert record["merged_historical_audit_pr"] == 7
    assert record["medium_publication_status"] == "NOT_VERIFIED_NOT_CLAIMED"
    assert record["real_biological_results"] == "NONE"
    assert record["expected_current_baseline"]["donors"] == 6
    for path in (
        "docs/handoff/README.md", "docs/handoff/TAKEOVER_20261027.md",
        "docs/handoff/EXECUTION_PLAYBOOK.md", "docs/handoff/PENDING_WORK.md",
        "docs/handoff/PUBLICATION_CHECKLIST.md",
        "docs/handoff/SUCCESSOR_AGENT_INSTRUCTIONS.md",
        "docs/audit/README.md", "docs/audit/BASELINE_20261027.json",
        "docs/audit/DEFECT_REGISTER.csv", "docs/RESULTS_AND_INTERPRETATION.md",
        "docs/FIGURES_AND_METHODS.md", "CITATION.cff",
        "try_examples.py", "outputs/results.json",
    ):
        assert (ROOT / path).is_file(), path
    readme = (ROOT / "README.md").read_text()
    assert "docs/audit/README.md" in readme
    assert "docs/RESULTS_AND_INTERPRETATION.md" in readme
    assert "data/fictional_rna_observations.csv" in readme
