# backend/app/data_pipeline/load.py


from .extract import extract_historical_noaa_data
from .transform import transform_historical_station_data
from datetime import datetime, timezone, timedelta
import pandas as pd
import pyarrow as pq
from pathlib import Path


def load_historical_dataset_data(transformed_data: pd.DataFrame):
    now = datetime.now()
    today = '_'.join([str(now.month), str(now.day), str(now.year)])
    BASE_DIR = Path(__file__).resolve().parents[2]
    datasets_dir = BASE_DIR / "data" / "datasets"
    path = datasets_dir / f"surf_dataset_{today}.parquet"
    

    if path.exists():
        prev = pd.read_parquet(path)
        batch = pd.concat([prev, transformed_data], ignore_index=True)
        batch = batch.drop_duplicates(subset=["irl_obs_id", "timestamp"])
        batch.to_parquet(path)
    else:
        transformed_data.to_parquet(path)

    



if __name__ == '__main__':
    raw_data = extract_historical_noaa_data('44007')

    rn = datetime.now(tz=timezone.utc)
    before = rn - timedelta(hours=1)
    transformed_data = transform_historical_station_data(irl_obs_id=1, before_time=before, raw_data=raw_data)
    load_historical_dataset_data(transformed_data=transformed_data)