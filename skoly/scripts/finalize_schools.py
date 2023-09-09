import click

from skoly.scripts import ROOT
from skoly import schools


@click.command
def finalize():
    ROOT.mkdir(exist_ok=True)

    with open(ROOT / "schools.csv") as f:
        school_data = schools.load_from_ours(f)

    with open(ROOT / "final.csv", "w") as f:
        schools.write_to_final(school_data, f)
