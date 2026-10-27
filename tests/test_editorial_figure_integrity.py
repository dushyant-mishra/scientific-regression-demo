"""Publication visual contracts: scientific provenance, contrast, mobile type, SVG semantics."""
import json
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import pytest
from make_editorial_figures import read_evidence, TEXT_CONTRAST, ratio

ROOT=Path(__file__).resolve().parents[1]
NAMES=[
    'editorial_01_rna_evidence_landscape_v1',
    'editorial_01_rna_evidence_mobile_v1',
    'editorial_02_test_tripwire_landscape_v1',
    'editorial_02_test_tripwire_mobile_v1',
]
SVGNS='{http://www.w3.org/2000/svg}'

def test_editorial_science_is_read_from_real_sources():
    evidence=read_evidence(ROOT)
    assert evidence['measured']['gene']=='gene_3'
    assert evidence['measured']['count']=='4'
    assert evidence['unassayed']['gene']=='gene_3'
    assert evidence['unassayed']['assayed']=='false'
    assert evidence['unassayed']['count']==''
    assert evidence['zero']['gene']=='gene_2'
    assert evidence['zero']['count']=='0'
    r,g=evidence['red'],evidence['green']
    assert (r['passed'],r['failed'],r['errors'])==(4,6,0)
    assert (g['passed'],g['failed'],g['errors'])==(10,0,0)

def test_small_text_colors_meet_standard_contrast():
    for label,(fg,bg) in TEXT_CONTRAST.items():
        assert ratio(fg,bg)>=4.5,label

def test_editorial_art_assets_exist_with_accessibility_metadata():
    for name in NAMES:
        svg=ROOT/'figures'/f'{name}.svg'
        png=ROOT/'figures'/f'{name}.png'
        assert svg.is_file() and png.is_file(),name
        assert png.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n',name
        w,h=struct.unpack('>II',png.read_bytes()[16:24])
        assert w>=1200 and h>=800,(name,w,h)
        root=ET.parse(svg).getroot()
        assert root.find(SVGNS+'title') is not None,name
        assert root.find(SVGNS+'desc') is not None,name
        assert len(list(root.iter(SVGNS+'text')))>=12,name
        if 'mobile' in name:
            assert '900 1' in root.attrib.get('viewBox',''),name
            # At 390 rendered CSS pixels, native font size 29px maps to 12.56px.
            sizes=[float(el.get('font-size')) for el in root.iter(SVGNS+'text')]
            assert min(sizes)>=29,(name,min(sizes))

def test_science_diagram_stays_synchronized_with_raw_counts():
    content=(ROOT/'figures/editorial_01_rna_evidence_mobile_v1.svg').read_text()
    assert 'gene_3: assayed' in content
    assert 'gene_3: NOT assayed' in content
    assert 'gene_2 · Study A · cell_01 · count 0' in content
    assert 'No assay  ≠  observed zero' in content

def test_test_tile_figures_are_not_biological_results():
    for name in ('editorial_02_test_tripwire_landscape_v1','editorial_02_test_tripwire_mobile_v1'):
        txt=(ROOT/'figures'/f'{name}.svg').read_text()
        assert '4 passed' in txt and '6 failed' in txt
        assert '10 passed' in txt and '0 failed' in txt
        assert 'gene expression' in txt or 'biological evidence' in txt

def test_reader_rejects_assay_label_mutation(tmp_path):
    import csv
    from shutil import copyfile
    data=tmp_path/'data'; data.mkdir()
    outputs=tmp_path/'outputs'; outputs.mkdir()
    copyfile(ROOT/'outputs/results.json',outputs/'results.json')
    with (ROOT/'data/fictional_rna_observations.csv').open(newline='') as f:
        rows=list(csv.DictReader(f))
    mutated=False
    for x in rows:
        if x['study']=='study_b' and x['cell_id']=='cell_07' and x['gene']=='gene_3':
            x['assayed']='true'
            mutated=True
    assert mutated
    with (data/'fictional_rna_observations.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    with pytest.raises(AssertionError):
        read_evidence(tmp_path)
