# backend/app/data_pipeline/extract.py

import requests


def extract_noaa_data() -> str:
    '''extracts the raw data from noaa's latest observations
       and returns it as a string'''

    url = 'https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt'

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.text



station_ids = ['44013', '44098', '44030', 'WEXM1', '44007', '44150', '44011']


def extract_historical_noaa_data(station: str) -> str:
    url = "https://www.ndbc.noaa.gov/data/realtime2/" + station + ".txt"

    if station not in station_ids:
        raise ValueError("station id irrelevant for north east predictions")

    res = requests.get(url)
    data = res.text

    return data

if __name__ == "__main__":
    extract_historical_noaa_data('44007')
