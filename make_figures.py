"""Render publication figures from recorded pytest and fictional CSV results.

None of the RED/GREEN counts or gene measurement classes is hard-coded.
"""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "savefig.facecolor": "white"})
COLORS = {"ink": "#20334A", "sub": "#475569", "green": "#287D75", "red": "#BD4C4A", "blue": "#3578A8", "pale": "#D4E6F4", "gray": "#E6E8EA", "line": "#CBD5E1"}


def save(fig, slug):
    fig.savefig(OUT / (slug + ".png"), dpi=200, facecolor="white")
    fig.savefig(OUT / (slug + ".svg"), facecolor="white")
    plt.close(fig)


def test_bar_counts(data):
    """Return bar data only from the supplied parsed-run receipt."""
    return [(data[k]["passed"], data[k]["failed"] + data[k]["errors"]) for k in ("red", "green")]


def chart_tests():
    d = json.loads((ROOT / "outputs/results.json").read_text())
    labels = ["RED: intentional bug", "GREEN: repaired code"]
    values = [d["red"], d["green"]]
    counts = [int(x["total"]) for x in values]
    bar_counts = test_bar_counts(d)
    fig, ax = plt.subplots(figsize=(10, 5.0), layout="constrained")
    y = [1, 0]
    for i, row in enumerate(values):
        passed, failed = bar_counts[i]
        ax.barh(y[i], passed, color=COLORS["green"], height=.43, edgecolor="none")
        ax.barh(y[i], failed, left=passed, color=COLORS["red"], height=.43, edgecolor="none")
        if passed:
            ax.text(passed/2, y[i], f"{passed} passed", va="center", ha="center", weight="bold", color="white", fontsize=11)
        if failed:
            ax.text(passed+failed/2, y[i], f"{failed} failed", va="center", ha="center", weight="bold", color="white", fontsize=11)
    ax.set_yticks(y, labels, color=COLORS["ink"])
    ax.tick_params(axis="y", length=0, pad=12)
    ax.set_xlim(0, max(counts) + 1)
    ax.set_xticks(range(max(counts)+1))
    ax.set_xlabel("Executed tests in the same suite", color=COLORS["ink"])
    ax.grid(axis="x", alpha=.12)
    ax.set_axisbelow(True)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.suptitle("Do the tests catch the scientific-rule bugs?", fontsize=19, weight="bold", color=COLORS["ink"])
    ax.set_title("Results parsed from local pytest JUnit reports • not invented counts", color=COLORS["sub"], fontsize=10, pad=19)
    save(fig, "figure_2_actual_red_green")


def chart_matrix():
    rows = list(csv.DictReader((ROOT / "data/fictional_rna_observations.csv").open()))
    genes = sorted({r["gene"] for r in rows})
    cells = list(dict.fromkeys(r["cell_id"] for r in rows))
    lookup = {(r["cell_id"], r["gene"]): r for r in rows}
    fig, ax = plt.subplots(figsize=(9.2, 7.8))
    fig.subplots_adjust(left=.21,right=.83,top=.84,bottom=.19)
    for rownum, cell in enumerate(cells):
        for j, gene in enumerate(genes):
            r = lookup[(cell,gene)]
            color = COLORS["gray"] if r["assayed"] == "false" else (COLORS["pale"] if r["count"] == "0" else COLORS["blue"])
            text = "—" if r["assayed"] == "false" else ("0" if r["count"] == "0" else "+")
            ax.add_patch(plt.Rectangle((j-.45,rownum-.44),.9,.88,facecolor=color,edgecolor="white",linewidth=1.5))
            ax.text(j,rownum,text,ha="center",va="center",color="white" if color==COLORS["blue"] else COLORS["ink"],weight="bold",fontsize=13)
    ax.axhline(5.5,color=COLORS["ink"],linewidth=1.8)
    ax.text(2.58,2.3,"Study A",ha="left",va="center",color=COLORS["sub"],fontsize=10)
    ax.text(2.58,8.4,"Study B",ha="left",va="center",color=COLORS["sub"],fontsize=10)
    ax.set_xticks(range(len(genes)),genes)
    ax.set_yticks(range(len(cells)),cells)
    ax.tick_params(length=0,pad=7)
    ax.xaxis.tick_top()
    ax.invert_yaxis()
    ax.set_xlim(-.5,3.45)
    ax.set_ylim(len(cells)-.5,-.5)
    for s in ax.spines.values():s.set_visible(False)
    ax.set_title("A fictional RNA experiment: zero is not missing", fontsize=18,weight="bold",color=COLORS["ink"],pad=50,loc="left")
    fig.legend(handles=[Patch(color=COLORS["blue"],label="RNA detected (+)"),Patch(color=COLORS["pale"],label="Measured count = 0"),Patch(color=COLORS["gray"],label="Gene not assayed (—)")],loc="lower center",ncol=3,frameon=False,bbox_to_anchor=(.52,.045),fontsize=10)
    save(fig,"figure_1_fictional_rna_matrix")


def chart_workflow():
    steps = [
      ("1  Define the biology", "Measured zero is different from an unassayed gene."),
      ("2  Write and run a falsifying test", "The deliberately faulty code should fail."),
      ("3  Repair and challenge the code", "Fix the function; independently test edge cases."),
      ("4  Push to GitHub", "Actions reruns tests when code changes."),
      ("5  Read the evidence", "Review JUnit reports, code diffs and figures."),
    ]
    fig, ax = plt.subplots(figsize=(8.5,8.8),layout="constrained")
    ax.set_xlim(0,10)
    ax.set_ylim(0,12.2)
    ax.axis("off")
    ax.set_title("From biology to continuously checked code",fontsize=18,weight="bold",loc="left",pad=25,color=COLORS["ink"])
    for i,(head,desc) in enumerate(steps):
        y=10.7-i*2.18
        rect=FancyBboxPatch((.55,y-.5),8.9,1.5,boxstyle="round,pad=0.12,rounding_size=.18",facecolor="#EDF3F8" if i%2==0 else "#ECF6F3",edgecolor=COLORS["line"],linewidth=1.3)
        ax.add_patch(rect)
        ax.text(1.0,y+.51,head,fontsize=13,weight="bold",ha="left",va="center",color=COLORS["ink"])
        ax.text(1.0,y-.09,desc,fontsize=10.4,ha="left",va="center",color=COLORS["sub"])
        if i < len(steps)-1:
            ax.annotate("",xy=(5,y-1.06),xytext=(5,y-0.66),arrowprops={"arrowstyle":"-|>","color":COLORS["sub"],"lw":1.4})
    save(fig,"figure_3_workflow")


def chart_replicates():
    from science_rules import replication_summary
    ids=["donor_01"]*500+["donor_02"]*500
    result=replication_summary(ids)
    fig,ax=plt.subplots(figsize=(8.5,4.8),layout="constrained")
    xx=[0,1]
    yy=[result["technical_rows"],result["biological_n"]]
    ax.bar(xx,yy,color=[COLORS["blue"],COLORS["green"]],width=.57)
    ax.set_xticks(xx,["Resampled rows", "Independent donors"],fontsize=11)
    for x,v in zip(xx,yy): ax.text(x,v+25,f"{v:,}",ha="center",fontsize=14,weight="bold",color=COLORS["ink"])
    ax.set_ylim(0,max(yy)*1.18)
    ax.set_ylabel("Count",color=COLORS["ink"])
    ax.set_title("1,000 computational rows ≠ 1,000 donors",fontsize=18,weight="bold",loc="left",pad=20,color=COLORS["ink"])
    fig.text(.16,.89,"Two fictional donors; 500 computational draws per donor",color=COLORS["sub"],fontsize=10.5)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.grid(axis="y",alpha=.13)
    ax.set_axisbelow(True)
    save(fig,"figure_4_donor_vs_rows")


def main():
    chart_matrix();chart_tests();chart_workflow();chart_replicates()
    print("Saved 4 PNG + 4 SVG figures; test counts and assay states read from output files")


if __name__=="__main__": main()
