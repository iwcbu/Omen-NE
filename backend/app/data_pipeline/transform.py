# backend/app/data_pipeline/transform.py

from data_pipeline.extract import extract_noaa_data, extract_historical_noaa_data_from_year

import pandas as pd
from datetime import datetime, timedelta, timezone



# =====================================================
#
#                  CURRENT DATA 
#
# =====================================================


def transform_noaa_data(raw_data: str):

    data = []
    station_ids = ['44013', '44098', '44030', 'WEXM1', '44007', '44150', '44011']

    for sid in station_ids:

        start = raw_data.find(sid)
        if start == -1:
            continue

        end = start
        while raw_data[end] != '\n' and end < len(raw_data):
            end += 1

        row = raw_data[start: end].split()

        year = row.pop(3)
        month = row.pop(3)
        day = row.pop(3)
        hour = row.pop(3)
        minute = row.pop(3)

        date = '-'.join([year,month,day])
        time = ':'.join(["T"+hour,minute,"00Z"])
        timestamp = date+time

        row.insert(3, timestamp)
        row.pop(12)
        row = row[:-2]


        data.append(row)

    columns = [
        "timestamp",

        "wind_direction",
        "wind_speed",
        "gust",

        "signicant_wave_height",
        "dominant_wave_period",
        "average_wave_period",
        "dominant_wave_direction_origin",
        
        "atmospheric_pressure",
        "air_temp",
        "water_temp",
        
    ]

    df = pd.DataFrame(data, columns=columns)
    df = df.replace("MM", pd.NA)

    df['id'] = df['id'].astype("string")
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)

    for col in columns:
        if col != 'id' and col != 'timestamp':
            df[col] = pd.to_numeric(df[col], errors="coerce")

    print()
    print(df)


    return df


# =====================================================
#
#                  HISTORICAL DATA 
#
# =====================================================



def transform_recent_historical_station_data(irl_obs_id: int, before_time: datetime, raw_data: str):
    '''
        transforms raw NOAA observations before a certain time into structured dataframes, paired with an in person observation.
        
        params:  
            irl_obs_id: foreign key to an in person observation
            before_time: time restraint on the oldest observation wanted  
            raw_data: raw text containing historical NOAA measurements from a specific year
    
        returns:
            a dataframe containing normalized timestamps, foreign key to an in person observation,
            numeric, measurements, and missing values represented as NaN
    
        raises:
            ValueError: if the input data is empty or malformed
        
        '''

    
    if raw_data == "" or raw_data.strip() == "":
        raise ValueError("Input data is empty or malformed")


    data = []
    split_data = raw_data.split('\n')   

    i = 2
    while i < len(split_data):

       

        row = split_data[i]
        row = row.split()

        year = int(row.pop(0))
        month = int(row.pop(0))
        day = int(row.pop(0))
        hour = int(row.pop(0))
        minute = int(row.pop(0))


        timestamp = datetime(year, month, day, hour, minute, tzinfo=timezone.utc)

        if timestamp < before_time:
            break

        row.insert(0, timestamp)
        row.insert(0, irl_obs_id)
        row = row[:-3]

        data.append(row)

        i += 1

    columns = [
        "timestamp",

        "wind_direction",
        "wind_speed",
        "gust",

        "signicant_wave_height",
        "dominant_wave_period",
        "average_wave_period",
        "dominant_wave_direction_origin",
        
        "atmospheric_pressure",
        "air_temp",
        "water_temp",
        
    ]


    df = pd.DataFrame(data, columns=columns)
    df = df.replace("MM", pd.NA)
    print(df)

    return df









def transform_historical_station_data_from_year(raw_data: str):
    '''
    transforms raw NOAA observations into structured dataframes
    
    params:    
        raw_data: raw text containing historical NOAA measurements from a specific year

    returns:
        a dataframe containing normalized timestamps, numeric
        measurements, and missing values represented as NaN

    raises:
        ValueError: if the input data is empty or malformed
    
    '''


    if raw_data == "" or raw_data.strip() == "":
        raise ValueError("Input data is empty or malformed")


    data = []
    split_data = raw_data.split('\n')

    for i in range(2, len(split_data)-1):
        row = split_data[i]
        row = row.split()

        year = int(row.pop(0))
        month = int(row.pop(0))
        day = int(row.pop(0))
        hour = int(row.pop(0))
        minute = int(row.pop(0))

        timestamp = datetime(year, month, day, hour, minute, tzinfo=timezone.utc)
        row.insert(0, timestamp)
        row = row[:-3]

        data.append(row)

        i += 1

    columns = [
        "timestamp",

        "wind_direction",
        "wind_speed",
        "gust",

        "signicant_wave_height",
        "dominant_wave_period",
        "average_wave_period",
        "dominant_wave_direction_origin",

        "atmospheric_pressure",
        "air_temp",
        "water_temp",
        
    ]


    df = pd.DataFrame(data, columns=columns)

    df.attrs["units"] = {
        "timestamp": "UTC",
        "wind_direction": "degrees_true",
        "wind_speed": "m/s",
        "gust": "m/s",
        "signicant_wave_height": "m",
        "dominant_wave_period": "s",
        "average_wave_period": "s",
        "dominant_wave_direction_origin": "degrees_true",
        "atmospheric_pressure": "hPa",
        "air_temp": "°C",
        "water_temp": "°C",
    }


    df = df.replace('99.0', pd.NA)
    df = df.replace('99.00', pd.NA)
    df = df.replace('999.0', pd.NA)
    df = df.replace('999', pd.NA)
    df = df.replace('9999', pd.NA)
    df = df.replace('9999.0', pd.NA)

    for col in columns:
        if col == 'timestamp':
            continue

        df[col].astype(float)


    return df





if __name__ == "__main__":
    print()
    print(' transform_historical_station_data(min_ago, raw_data)')

    time_now = datetime.now(timezone.utc)
    tb = time_now - timedelta(minutes=40)
    time_before = datetime(tb.year, tb.month, tb.day, tb.hour, tb.minute, tzinfo=timezone.utc)

    rd = extract_historical_noaa_data_from_year('44007', 2025)
    td = transform_historical_station_data_from_year(rd)
    print(td)
    print()