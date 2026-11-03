import requests
import pandas as pd

from config import API_KEY, BASE_URL

headers = {
    "key": API_KEY
}

def get_series(series_code, start_date, end_date):

    url = (
        f"{BASE_URL}"
        f"series={series_code}"
        f"&startDate={start_date}"
        f"&endDate={end_date}"
        "&type=json"
    )

    response = requests.get(url, headers=headers)

    veri = response.json()

    df = pd.DataFrame(veri["items"])

    return df
