
from extract import extract_noaa_data
from transform import transform_noaa_data
from load import load_data_to_db

def run_noaa_pipeline():
    raw_data = extract_noaa_data()
    transformed = transform_noaa_data(raw_data)
    load_data_to_db(transformed)