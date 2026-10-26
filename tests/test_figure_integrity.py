"""Prevent figures and links from drifting away from the current RNA example."""
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
FIGURES = {
    "figure_1_rna_measurements_v2",
    "figure_2_test_results_v2",
    "figure_3_regression_workflow_v2",
    "figure_4_donor_units_v2",
}


def test_figure_outputs_are_complete_and_large_enough_for_publication():
    for stem in FIGURES:
        png = ROOT / "figures" / (stem + ".png")
        svg = ROOT / "figures" / (stem + ".svg")
        assert png.is_file() and svg.is_file(), stem
        b = png.read_bytes()
        assert b[:8] == b"\x89PNG\r\n\x1a\n", stem
        width, height = struct.unpack(">II", b[16:24])
        assert width >= 1000 and height >= 650, (stem, width, height)
        assert svg.stat().st_size > 1000, stem


def test_matrix_labels_match_generated_data_and_no_obsolete_gene_names():
    import csv
    with (ROOT / "data" / "fictional_rna_observations.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    matrix = (ROOT / "figures" / "figure_1_rna_measurements_v2.svg").read_text()
    for gene in sorted({r["gene"] for r in rows}):
        assert gene in matrix, gene
    for cell in sorted({r["cell_id"] for r in rows}):
        assert cell in matrix, cell
    for svg in (ROOT / "figures").glob("*.svg"):
        text = svg.read_text()
        assert not re.search(r"FIC[-_]\w+|A fictional RNA experiment|Two fictional donors", text), svg


def test_readme_and_article_reference_existing_current_figures():
    for document in ("README.md", "MEDIUM_ARTICLE.md"):
        content = (ROOT / document).read_text()
        referenced = re.findall(r"figures/(figure_[\w]+\.png)", content)
        assert referenced, document
        assert all((ROOT / "figures" / img).is_file() for img in referenced), (document, referenced)
        assert not any("figure_1_fictional_rna_matrix" in img for img in referenced), document
    assert "figure_1_rna_measurements_v2.png" in (ROOT / "README.md").read_text()
    assert "figure_1_rna_measurements_v2.png" in (ROOT / "MEDIUM_ARTICLE.md").read_text()
