"""Reproducible editorial RNA illustrations; values read from repo CSV and JUnit-derived JSON.

Optional dependencies: requirements-editorial.txt.
Outputs: two visually designed landscape figures and two independently composed mobile figures,
each with an SVG master (including title/description) and a PNG Medium export.
"""
import argparse, csv, json
from pathlib import Path
import svgwrite, cairosvg

INK='#17253B'; MUTED='#44536A'; BG='#F7F8FC'; WHITE='#FFFFFF'
PURPLE='#6449B8'; LAVENDER='#EAE6FC'; TEAL='#087368'; MINT='#E8F9F3'
AMBER='#925806'; CREAM='#FFF1D1'; RED='#B02B48'; ROSE='#FFE8EF'
NAVY='#243553'; BORDER='#D7E1EC'

def luminance(h):
    q=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    x=lambda a: a/12.92 if a<=0.04045 else ((a+0.055)/1.055)**2.4
    r,g,b=[x(a) for a in q]
    return .2126*r+.7152*g+.0722*b

def ratio(a,b):
    hi,lo=sorted((luminance(a),luminance(b)),reverse=True)
    return (hi+.05)/(lo+.05)

TEXT_CONTRAST={
  'dark text on canvas':(INK,BG),'muted text on canvas':(MUTED,BG),
  'purple on lavender':(PURPLE,LAVENDER),'teal on mint':(TEAL,MINT),
  'amber on cream':(AMBER,CREAM),'white on red':(WHITE,RED),
  'white on teal':(WHITE,TEAL),'white on navy':(WHITE,NAVY),
}
def read_evidence(root):
    with (root/'data/fictional_rna_observations.csv').open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    lookup={(a['study'],a['cell_id'],a['gene']):a for a in rows}
    assert len(rows)==len(lookup)==36
    measured=lookup['study_a','cell_01','gene_3']
    unassayed=lookup['study_b','cell_07','gene_3']
    zero=lookup['study_a','cell_01','gene_2']
    assert measured['assayed']=='true' and measured['count'].isdigit() and int(measured['count'])>0
    assert unassayed['assayed']=='false' and unassayed['count']==''
    assert zero['assayed']=='true' and zero['count']=='0'
    assert len([x for x in rows if x['study']=='study_b' and x['gene']=='gene_3' and x['assayed']=='false' and x['count']==''])==6
    d=json.loads((root/'outputs/results.json').read_text(encoding='utf-8'))
    red,green=d['red'],d['green']
    assert red['total']==green['total']>0
    assert all(x['passed']+x['failed']+x['errors']+x['skipped']==x['total'] for x in (red,green))
    assert red['failed']+red['errors']>0 and green['failed']+green['errors']==green['skipped']==0
    for name,pair in TEXT_CONTRAST.items():
        assert ratio(*pair)>=4.5,(name,ratio(*pair))
    return {'measured':measured,'unassayed':unassayed,'zero':zero,'red':red,'green':green}

class Art:
    def __init__(self,w,h,title,description):
        self.w=w;self.h=h
        self.d=svgwrite.Drawing(size=(f'{w}px',f'{h}px'),viewBox=f'0 0 {w} {h}')
        self.d.set_desc(title=title,desc=description)
        self.rect(0,0,w,h,BG)
    def rect(self,x,y,w,h,color,r=0,stroke='none',sw=0):
        assert x>=0 and y>=0 and x+w<=self.w and y+h<=self.h
        self.d.add(self.d.rect(insert=(x,y),size=(w,h),rx=r,ry=r,fill=color,stroke=stroke,stroke_width=sw))
    def circle(self,x,y,r,color,stroke='none',sw=0):
        assert x-r>=0 and y-r>=0 and x+r<=self.w and y+r<=self.h
        self.d.add(self.d.circle(center=(x,y),r=r,fill=color,stroke=stroke,stroke_width=sw))
    def line(self,x,y,x2,y2,color,sw=4):
        self.d.add(self.d.line(start=(x,y),end=(x2,y2),stroke=color,stroke_width=sw,stroke_linecap='round'))
    def text(self,v,x,y,size=30,color=INK,bold=False,center=False):
        assert 0<=x<=self.w and 0<=y<=self.h
        self.d.add(self.d.text(str(v),insert=(x,y),font_size=size,font_family='DejaVu Sans',
                               font_weight='bold' if bold else 'normal',
                               text_anchor='middle' if center else 'start',fill=color))
    def pill(self,s,x,y,w,h,bg,fg,size):
        self.rect(x,y,w,h,bg,h/2)
        self.text(s,x+w/2,y+h/2+size*.34,size,fg,True,True)
    def write(self,path):
        svg=path.with_suffix('.svg');png=path.with_suffix('.png')
        svg.parent.mkdir(parents=True,exist_ok=True)
        self.d.saveas(str(svg))
        cairosvg.svg2png(url=str(svg),write_to=str(png),output_width=max(1600,self.w) if self.w>self.h else max(1200,self.w))
        return [str(svg),str(png)]

def icon(c,x,y,color,n,assayed):
    c.circle(x,y,68,WHITE,color,5)
    if assayed:
        positions=[(-25,-25),(24,-22),(-20,22),(24,23),(0,0),(30,5),(-28,0),(4,29)]
        for dx,dy in positions[:min(n,len(positions))]:
            c.circle(x+dx,y+dy,8,color)
    else:
        c.line(x-39,y+39,x+39,y-39,color,8)

def biology_landscape(e):
    c=Art(1600,1010,'Same gene, different RNA evidence',
          'Fictional RNA table: Study A cell_01 gene_3 count '+e['measured']['count']+
          ', Study B cell_07 gene_3 not assayed, and separately Study A cell_01 gene_2 measured zero.')
    c.pill('THE SCIENTIFIC MIX-UP',68,60,250,49,LAVENDER,PURPLE,20)
    c.text('Same gene. Different evidence.',70,188,65,INK,True)
    c.text('Study B did not assay gene_3. A blank must not become zero.',72,240,27,MUTED)
    cards=[(70,MINT,TEAL,'STUDY A  ·  cell_01','gene_3 was assayed',e['measured']['count'],True),
           (815,CREAM,AMBER,'STUDY B  ·  cell_07','gene_3 was not assayed','—',False)]
    for x,bg,fg,lab,desc,v,assayed in cards:
        c.rect(x,292,715,424,WHITE,28,BORDER,2)
        c.rect(x+18,310,679,88,bg,20)
        c.text(lab,x+43,364,29,fg,True)
        c.text(desc,x+43,449,34,INK,True)
        c.text('RNA count',x+43,503,25,MUTED)
        c.text(v,x+43,628,112,fg,True)
        icon(c,x+571,550,fg,int(v) if assayed else 0,assayed)
        c.text('Measured RNA' if assayed else 'No observation exists',x+43,686,27,INK,True)
    c.rect(70,750,1460,115,LAVENDER,22)
    c.pill('DIFFERENT GENE',100,781,279,50,WHITE,PURPLE,23)
    c.text('gene_2  ·  Study A  ·  cell_01  ·  assayed count '+e['zero']['count'],409,815,31,INK,True)
    c.text('This is a measured zero. It is NOT equivalent to the unassayed gene above.',100,848,25,MUTED)
    c.rect(70,901,1460,63,NAVY,16)
    c.text('THE RULE: Check whether the assay happened before interpreting its count.',96,943,27,WHITE,True)
    return c

def biology_mobile(e):
    c=Art(900,1700,'Mobile: a measured gene is not an unassayed gene',
          'Study A cell_01 gene_3 has positive count; Study B cell_07 gene_3 was not assayed; gene_2 is a separate measured zero.')
    c.pill('THE SCIENTIFIC MIX-UP',50,48,381,62,LAVENDER,PURPLE,29)
    c.text('Same gene.',50,196,76,INK,True)
    c.text('Different evidence.',50,281,70,INK,True)
    c.text('A missing assay is not a zero.',50,348,34,MUTED)
    for y,lab,sub,v,fg,bg,assayed in [
       (397,'STUDY A · cell_01','gene_3: assayed',e['measured']['count'],TEAL,MINT,True),
       (801,'STUDY B · cell_07','gene_3: NOT assayed','—',AMBER,CREAM,False)]:
        c.rect(50,y,800,374,WHITE,28,BORDER,2)
        c.rect(72,y+20,755,91,bg,21)
        c.text(lab,100,y+80,33,fg,True)
        c.text(sub,94,y+170,41,INK,True)
        c.text('RNA count',94,y+236,29,MUTED)
        c.text(v,95,y+333,109,fg,True)
        icon(c,704,y+257,fg,int(v) if assayed else 0,assayed)
    c.rect(50,1232,800,212,LAVENDER,24)
    c.text('A real measured zero:',84,1308,37,INK,True)
    c.text('gene_2 · Study A · cell_01 · count '+e['zero']['count'],84,1378,34,PURPLE,True)
    c.rect(50,1490,800,135,NAVY,24)
    c.text('The scientific rule',82,1548,33,WHITE,True)
    c.text('No assay  ≠  observed zero',82,1601,38,WHITE,True)
    return c

def tiles(c,x,y,passes,failures,tilew=101,tileh=88,gap=15):
    for i,status in enumerate(['pass']*passes+['fail']*failures):
        xx=x+(i%5)*(tilew+gap);yy=y+(i//5)*(tileh+gap)
        c.rect(xx,yy,tilew,tileh,TEAL if status=='pass' else RED,19)
        c.text('✓' if status=='pass' else '×',xx+tilew/2,yy+tileh*.74,63,WHITE,True,True)

def test_landscape(e):
    r,g=e['red'],e['green'];t=r['total']
    c=Art(1600,970,'The same ten tests detect intentionally buggy code',
          f'Test receipts: buggy {r["passed"]} pass and {r["failed"]+r["errors"]} fail, corrected {g["passed"]} pass and {g["failed"]+g["errors"]} fail. Tiles show aggregate counts, not test IDs.')
    c.pill('SOFTWARE SAFETY CHECK',70,54,357,52,LAVENDER,PURPLE,23)
    c.text('Will the tests catch the bug?',72,180,65,INK,True)
    c.text(f'The same {t} tests. Same expected answers. Two code versions.',72,242,30,MUTED)
    for x,bg,fg,label,p,f,detail in [
        (70,ROSE,RED,'BEFORE: WRONG CODE',r['passed'],r['failed']+r['errors'],'Intentional negative example'),
        (815,MINT,TEAL,'AFTER: CORRECTED',g['passed'],g['failed']+g['errors'],'Repaired implementation')]:
        c.rect(x,282,714,502,WHITE,28,BORDER,2)
        c.rect(x+20,304,674,92,bg,20)
        c.text(label,x+50,359,29,fg,True)
        c.text('Checks detect problems' if f else f'All {t} behavior checks pass',x+48,458,32,INK,True)
        c.text(detail,x+48,508,26,MUTED)
        tiles(c,x+62,538,p,f)
        c.text(f'{p} passed',x+50,761,31,TEAL,True)
        c.text(f'{f} failed',x+386,761,31,RED if f else MUTED,True)
    c.rect(70,820,1460,95,NAVY,19)
    c.text('ONE TILE = ONE EXECUTED TEST',100,867,28,WHITE,True)
    c.text('Software checks ≠ biological evidence',856,867,26,WHITE)
    return c

def test_mobile(e):
    r,g=e['red'],e['green'];t=r['total']
    c=Art(900,1750,'Mobile: the same software tests before and after repair',
          f'Buggy: {r["passed"]} pass, {r["failed"]+r["errors"]} fail. Repaired: {g["passed"]} pass, {g["failed"]+g["errors"]} fail. These are software tests.')
    c.pill('SOFTWARE SAFETY CHECK',50,48,388,61,LAVENDER,PURPLE,29)
    c.text('Does the test',50,198,70,INK,True)
    c.text('catch the bug?',50,278,70,INK,True)
    c.text(f'Same {t} checks. Same expected answers.',50,343,33,MUTED)
    for y,lab,heading,fg,bg,p,f in [
        (408,'BEFORE · WRONG CODE','Intentional failures',RED,ROSE,r['passed'],r['failed']+r['errors']),
        (954,'AFTER · REPAIRED','All checks passing',TEAL,MINT,g['passed'],g['failed']+g['errors'])]:
        c.rect(50,y,800,500,WHITE,28,BORDER,2)
        c.rect(72,y+21,756,91,bg,20)
        c.text(lab,99,y+82,34,fg,True)
        c.text(heading,91,y+188,44,INK,True)
        tiles(c,95,y+214,p,f,112,93,24)
        c.text(f'{p} passed',90,y+464,36,TEAL,True)
        c.text(f'{f} failed',495,y+464,36,RED if f else MUTED,True)
    c.rect(50,1500,800,170,NAVY,24)
    c.text('Each tile = one test',84,1567,36,WHITE,True)
    c.text('Not evidence of gene expression.',84,1629,30,WHITE)
    return c

def main(root):
    e=read_evidence(root)
    figures={
      'editorial_01_rna_evidence_landscape_v1':biology_landscape(e),
      'editorial_01_rna_evidence_mobile_v1':biology_mobile(e),
      'editorial_02_test_tripwire_landscape_v1':test_landscape(e),
      'editorial_02_test_tripwire_mobile_v1':test_mobile(e),
    }
    for name,fig in figures.items():
        print(fig.write(root/'figures'/name))
    print('Evidence: source rows=36; RED',e['red']['passed'],'pass',e['red']['failed']+e['red']['errors'],'fail; GREEN',e['green']['passed'],'pass',e['green']['failed']+e['green']['errors'],'fail')
    print('All configured foreground/background text contrast pairs >= 4.5:1')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    main(parser.parse_args().root)
