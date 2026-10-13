# backend/app/data_pipeline/load.py


from data_pipeline.extract import extract_historical_noaa_data_from_year
from data_pipeline.transform import transform_historical_station_data_from_year
from datetime import datetime, timezone, timedelta
import pandas as pd
import pyarrow as pq
from pathlib import Path
from data_pipeline.models import Source


def load_historical_data_from_year(transformed_data: pd.DataFrame, source: Source):
    '''
    loads processed historical data into its given company's device's directory as a parquet.

    param:
        transformed_data: dataframe of processed NOAA data
        source: an object with the company and device that recorded these observations and the year they are from
    returns:
        path of where the parquet made was created / overwritten
    
    '''

    BASE_DIR = Path(__file__).resolve().parents[2]
    
    device_dir = BASE_DIR / "data" / "processed" / source.company / source.device
    device_dir.mkdir(parents=True, exist_ok=True)

    path = device_dir / f"{source.year}.parquet"
    

    transformed_data.to_parquet(path)
    return path

    



if __name__ == '__main__':
    s1 = Source('noaa', '44098', 2025)
    s2 = Source('noaa', '44007', 2025)

    for s in [s1, s2]:
        rd = extract_historical_noaa_data_from_year(s.device, s.year)
        td = transform_historical_station_data_from_year(raw_data=rd)
        path_to_parquet = load_historical_data_from_year(transformed_data=td, source=s)

        data = pd.read_parquet(path_to_parquet)
        print()
        print(s.__str__())
        print(path_to_parquet)
        print()
        print(data)
        print()