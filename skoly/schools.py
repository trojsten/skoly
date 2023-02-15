import csv
import typing
from dataclasses import dataclass

from skoly.types import TypeDict

DATASOURCE = "https://crinfo.iedu.sk/RISPortal/register/ExportCSV?id=1"


@dataclass
class School:
    eduid: str              # EDUID
    id: str                 # KODSKO
    official_type: str      # TypSaSZKod
    official_name: str      # Nazov
    official_short: str     # NazovSkrateny
    official_address: str
    our_name: str = ""
    our_short: str = ""


SchoolDict = dict[str, School]


def make_address(raw_data: dict[str, str]) -> str:
    street = raw_data["Ulica"].strip()
    number = raw_data["OrientacneCislo"].strip()
    city = raw_data["Obec"].strip()

    first_part = f"{street} {number}".strip()
    if first_part:
        return f"{first_part}, {city}"
    else:
        return city


def _should_load(raw_data: dict[str, str], types: TypeDict) -> bool:
    if raw_data["STAV"] != "v prevádzke":
        return False
    if raw_data["TypSaSZKod"] not in types:
        return False
    if not types[raw_data["TypSaSZKod"]].group:
        return False
    return True


def load_from_official(file: typing.IO, types: TypeDict) -> SchoolDict:
    schools = SchoolDict()
    reader = csv.DictReader(file, delimiter=";")

    for row in reader:
        if not _should_load(row, types):
            continue

        schools[row["EDUID"]] = School(
            row["EDUID"],
            row["KODSKO"],
            row["TypSaSZKod"],
            row["Nazov"],
            row["NazovSkrateny"],
            make_address(row),
        )

    return schools


def load_from_ours(file: typing.IO) -> SchoolDict:
    schools = SchoolDict()
    reader = csv.DictReader(file)

    for row in reader:
        schools[row["eduid"]] = School(
            row["eduid"],
            row["id"],
            row["official_type"],
            row["official_name"],
            row["official_short"],
            row["official_address"],
            row["our_name"],
            row["our_short"],
        )

    return schools


def merge(ours: SchoolDict, official: SchoolDict) -> SchoolDict:
    merged = SchoolDict()
    for of in official.values():
        if of.id in ours:
            of.our_name = ours[of.id].our_name
            of.our_short = ours[of.id].our_short
        merged[of.id] = of
    return merged


def write_to_ours(data: SchoolDict, file: typing.IO):
    writer = csv.DictWriter(file, fieldnames=["eduid", "id", "official_type", "official_name", "official_short",
                                              "official_address", "our_name", "our_short"])
    writer.writeheader()

    rows = sorted(list(data.values()), key=lambda t: t.id)
    writer.writerows([x.__dict__ for x in rows])
