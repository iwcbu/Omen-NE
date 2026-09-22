# backend/app/data_pipeline/load.py


from extract import extract_historical_noaa_data
from transform import transform_historical_station_data
from datetime import datetime, timezone, timedelta
import pandas as pd


def load_historical_dataset_data(transformed_data: pd.DataFrame):
    pass
