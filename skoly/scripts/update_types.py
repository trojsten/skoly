import click

from skoly import utils, types
from skoly.scripts import ROOT


@click.command
def update_types():
    ROOT.mkdir(exist_ok=True)
    filename = ROOT / "types.csv"

    data = utils.download_csv(types.DATASOURCE)
    official = types.load_from_official(data)

    ours = types.TypeDict()
    if filename.exists():
        with open(filename) as f:
            ours = types.load_from_ours(f)

    merged = types.merge(ours, official)
    with open(filename, "w") as f:
        types.write_to_ours(merged, f)
