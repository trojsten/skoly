import csv
import typing
from collections import defaultdict


DATASOURCE = "https://crinfo.iedu.sk/RISPortal/register/ExportCSV?id=3"


ProgrammeMeta = dict[str, set[str]]


def _get_type(row: dict) -> str | None:
    type = None
    stupen = row["StupenVzdelaniaSKOV"]
    length = row["DlzkaStudiaKod"]
    odbor = row["OdborVzdelaniaSKOV"]

    if "gymnázium" in odbor:
        type = "gym"
    elif stupen == "primárne vzdelanie" or "základná škola" in odbor:
        type = "zs"
    elif "stredné" in stupen:
        type = "ss"

    if type:
        if length:
            return f"{type}:{int(length)/10:.0f}"
        return type


def load_from_official(file: typing.IO) -> ProgrammeMeta:
    meta = defaultdict(lambda: set())
    reader = csv.DictReader(file, delimiter=";")

    for row in reader:
        if row["Forma"] != "Bežný":
            continue

        if row["Stav"] != "Aktívny":
            continue

        type = _get_type(row)
        if type:
            meta[row["KodSKOV"]].add(type)

    return meta
