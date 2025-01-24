import csv
import typing
from dataclasses import dataclass

from skoly.types import TypeDict

DATASOURCE = "https://crinfo.iedu.sk/RISPortal/register/ExportCSV?id=1"


@dataclass
class School:
    eduid: str  # EDUID
    id: str  # KODSKO
    official_name: str  # Nazov
    official_short: str  # NazovSkrateny
    official_address: str
    official_years: set[str] | None = None
    our_name: str = ""
    our_short: str = ""
    our_years: set[str] | None = None


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
            row["official_name"],
            row["official_short"],
            row["official_address"],
            set(row["official_years"].split(",")) if row["official_years"] else None,
            row["our_name"],
            row["our_short"],
            set(row["our_years"].split(",")) if row["our_years"] else None,
        )

    return schools


def merge(ours: SchoolDict, official: SchoolDict) -> SchoolDict:
    merged = SchoolDict()
    for of in official.values():
        if of.eduid in ours:
            of.our_name = ours[of.eduid].our_name
            of.our_short = ours[of.eduid].our_short
            of.our_years = ours[of.eduid].our_years
        merged[of.eduid] = of
    return merged


def write_to_ours(data: SchoolDict, file: typing.IO):
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "eduid",
            "id",
            "official_name",
            "official_short",
            "official_address",
            "official_years",
            "our_name",
            "our_short",
            "our_years",
        ],
    )
    writer.writeheader()

    rows = sorted(list(data.values()), key=lambda t: t.id)
    for school in rows:
        writer.writerow(
            {
                "eduid": school.eduid,
                "id": school.id,
                "official_name": school.official_name,
                "official_short": school.official_short,
                "official_address": school.official_address,
                "official_years": ",".join(sorted(school.official_years))
                if school.official_years
                else "",
                "our_name": school.our_name,
                "our_short": school.our_short,
                "our_years": ",".join(sorted(school.our_years))
                if school.our_years
                else "",
            }
        )


def write_to_final(data: SchoolDict, file: typing.IO):
    writer = csv.DictWriter(
        file, fieldnames=["eduid", "id", "name", "short", "address", "years"]
    )
    writer.writeheader()

    rows = sorted(list(data.values()), key=lambda t: t.id)
    for school in rows:
        years = school.our_years or school.official_years
        writer.writerow(
            {
                "eduid": school.eduid,
                "id": school.id,
                "name": school.our_name or school.official_name,
                "short": school.our_short or school.official_short,
                "address": school.official_address,
                "years": ",".join(years) if years else "",
            }
        )
