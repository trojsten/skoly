import csv
import typing
from collections import defaultdict

from skoly.programme_metadata import ProgrammeMeta
from skoly.schools import SchoolDict

DATASOURCE = "https://crinfo.iedu.sk/RISPortal/register/ExportCSV?id=4"

ProgrammeDict = dict[str, set[str]]


def load_from_official(file: typing.IO, schools: SchoolDict, meta: ProgrammeMeta) -> ProgrammeDict:
    programmes = defaultdict(lambda: set())
    reader = csv.DictReader(file, delimiter=";")

    for row in reader:
        if row["SaSZ_EDUID"] not in schools:
            continue

        if row["KodSKOV"] not in meta:
            continue

        programmes[row["SaSZ_EDUID"]].update(meta[row["KodSKOV"]])

    return programmes
