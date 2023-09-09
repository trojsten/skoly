from pprint import pprint

import click

from skoly import utils, programme_metadata, schools, programme
from skoly.scripts import ROOT


@click.command
def update_programmes():
    data = utils.download_csv(programme_metadata.DATASOURCE)
    meta = programme_metadata.load_from_official(data)

    with open(ROOT / "schools.csv") as f:
        school_data = schools.load_from_ours(f)

    data = utils.download_csv(programme.DATASOURCE)
    programmes = programme.load_from_official(data, school_data, meta)

    for key, school in school_data.items():
        if school.eduid not in programmes:
            continue
        school.official_years = programmes[school.eduid]
        school_data[key] = school

    with open(ROOT / "schools.csv", "w") as f:
        schools.write_to_ours(school_data, f)
