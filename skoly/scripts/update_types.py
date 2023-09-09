import os

from skoly import utils, types

if __name__ == '__main__':
    os.makedirs("data", exist_ok=True)
    filename = "data/types.csv"

    data = utils.download_csv(types.DATASOURCE)
    official = types.load_from_official(data)

    ours = types.TypeDict()
    if os.path.exists(filename):
        with open(filename) as f:
            ours = types.load_from_ours(f)

    merged = types.merge(ours, official)
    with open(filename, "w") as f:
        types.write_to_ours(merged, f)
