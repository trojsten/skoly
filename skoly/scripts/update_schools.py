import click

from skoly import schools, utils, types
from skoly.scripts import ROOT


@click.command
def update_schools():
    ROOT.mkdir(exist_ok=True)
    filename = ROOT / "schools.csv"

    with open(ROOT / "types.csv") as f:
        type_data = types.load_from_ours(f)

    data = utils.download_csv(schools.DATASOURCE)
    official = schools.load_from_official(data, type_data)

    ours = schools.SchoolDict()
    if filename.exists():
        with open(filename) as f:
            ours = schools.load_from_ours(f)

    merged = schools.merge(ours, official)
    with open(filename, "w") as f:
        schools.write_to_ours(merged, f)
