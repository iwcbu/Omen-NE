

from datetime import datetime, timezone, timedelta


from .extract import extract_noaa_data, extract_historical_noaa_data
from .transform import transform_noaa_data, transform_historical_station_data
from .load import load_historical_dataset_data
from .models import IrlObs

def run_current_noaa_pipeline():
    raw_data = extract_noaa_data()
    transformed = transform_noaa_data(raw_data)

    return transformed





def run_historical_noaa_pipeline(min_ago: int, stationId, irl_obs_id):
    '''returns a dataframe of available reports
    up to 'min_ago' minutes ago from station 'stationId' '''

    raw_data = extract_historical_noaa_data(stationId)

    time_now = datetime.now(tz=timezone.utc)
    pt = time_now - timedelta(minutes=min_ago)
    past_time = datetime(pt.year, pt.month, pt.day, pt.hour, pt.minute, tzinfo=timezone.utc)

    trasnformed = transform_historical_station_data(irl_obs_id=irl_obs_id, before_time=past_time, raw_data=raw_data)
    load_historical_dataset_data(transformed_data=trasnformed)




def build_dataset_pipeline(obs: IrlObs):
    pass

    