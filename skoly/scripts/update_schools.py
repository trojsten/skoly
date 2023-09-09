import os

from skoly import schools, utils, types

if __name__ == '__main__':
    os.makedirs("data", exist_ok=True)
    filename = "data/schools.csv"

    with open("data/types.csv") as f:
        type_data = types.load_from_ours(f)

    data = utils.download_csv(schools.DATASOURCE)
    official = schools.load_from_official(data, type_data)

    ours = schools.SchoolDict()
    if os.path.exists(filename):
        with open(filename) as f:
            ours = schools.load_from_ours(f)

    merged = schools.merge(ours, official)
    with open(filename, "w") as f:
        schools.write_to_ours(merged, f)
