import csv
import typing
from dataclasses import dataclass


DATASOURCE = "https://crinfo.iedu.sk/RISPortal/ciselnik/ExportCSV?id=11"


@dataclass
class Type:
    id: str
    name: str
    group: str | None


TypeDict = dict[str, Type]


def load_from_official(file: typing.IO) -> TypeDict:
    types = TypeDict()
    reader = csv.DictReader(file, delimiter=";")

    for row in reader:
        types[row["KOD"]] = Type(
            id=row["KOD"],
            name=row["NAZOV_SK"],
            group=None,
        )

    return types


def load_from_ours(file: typing.IO) -> TypeDict:
    types = TypeDict()
    reader = csv.DictReader(file)

    for row in reader:
        types[row["id"]] = Type(
            id=row["id"],
            name=row["name"],
            group=row["group"],
        )

    return types


def merge(ours: TypeDict, official: TypeDict) -> TypeDict:
    merged = TypeDict()
    for of in official.values():
        if of.id in ours:
            of.group = ours[of.id].group
        merged[of.id] = of
    return merged


def write_to_ours(data: TypeDict, file: typing.IO):
    writer = csv.DictWriter(file, fieldnames=["id", "name", "group"])
    writer.writeheader()

    rows = sorted(list(data.values()), key=lambda t: t.id)
    writer.writerows([x.__dict__ for x in rows])
