import io

import requests


def download_csv(url) -> io.StringIO:
    r = requests.get(url)
    return io.StringIO(r.content.decode("utf-8-sig"))  # 'utf-8-sig' - treat BOM as metadata, not as file content

