

from datetime import datetime, timezone, timedelta


from data_pipeline.extract import extract_noaa_data, extract_historical_noaa_data_from_year
from data_pipeline.transform import transform_noaa_data, transform_recent_historical_station_data, transform_historical_station_data_from_year
from data_pipeline.load import load_historical_data_from_year
from .models import IrlObs, Source
from pandas import DataFrame


def run_current_noaa_pipeline():
    raw_data = extract_noaa_data()
    transformed = transform_noaa_data(raw_data)

    return transformed




def run_recent_noaa_pipeline_with_irl_obs(min_ago: int, stationId: str, irl_obs_id: str) -> DataFrame:
    '''
    returns a dataframe of available reports
    up to 'min_ago' minutes ago from station 'stationId'
     
    param:
        min_ago: an integer representing the obversations a given time in minutes before now
        stationId: an id of a NOAA station
        irl_obs_id: the foreign key to pair an in person observation with the observations within a given interval
    
    returns:
        None
    '''

    raw_data = extract_noaa_data(stationId)

    time_now = datetime.now(tz=timezone.utc)
    pt = time_now - timedelta(minutes=min_ago)
    past_time = datetime(pt.year, pt.month, pt.day, pt.hour, pt.minute, tzinfo=timezone.utc)

    transformed = transform_recent_historical_station_data(irl_obs_id=irl_obs_id, before_time=past_time, raw_data=raw_data)

    return transformed







def run_historical__noaa_pipeline_from_year(source: Source) -> None:
    '''
    loads a dataframe of available reports from a given year to a parquet 
    labeled by its company (NOAA) and its device id
     
    param:
        source: object containing the company (NOAA), the device an observation was recorded on, and the year it was observed

    returns:
        None

    '''

    raw_data = extract_historical_noaa_data_from_year(source.device, source.year)
    trasnformed = transform_historical_station_data_from_year(raw_data=raw_data)
    load_historical_data_from_year(transformed_data=trasnformed, source=source)




def build_dataset_pipeline(obs: IrlObs):
    pass

    