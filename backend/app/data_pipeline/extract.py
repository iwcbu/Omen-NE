# backend/app/data_pipeline/extract.py

import requests


from models import RawStationRow


def extract_noaa_data() -> str:
    '''extracts the raw data from noaa's latest observations
       and returns it as a string'''

    url = 'https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt'

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.text