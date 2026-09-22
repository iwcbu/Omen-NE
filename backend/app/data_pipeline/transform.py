# backend/app/data_pipeline/transform.py

from extract import extract_noaa_data, extract_historical_noaa_data

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
        'id', 
        'latitude', 
        'longitude', 
        'timestamp',

        'wind_direction', 
        'wind_speed', 
        'gust', 

        'avg_wave_height', 
        'primary_wave_period', 
        'avg_wave_period', 
        'avg_wave_direction', 

        'atmospheric_pressure',
        'air_temp', 
        'water_temp', 
        'dewpoint'
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



def transform_historical_station_data(before_time: datetime, raw_data: str):

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
        row = row[:-3]

        data.append(row)

        i += 1

    columns = [
        'timestamp',

        'wind_direction', 
        'wind_speed', 
        'gust', 

        'avg_wave_height', 
        'primary_wave_period', 
        'avg_wave_period', 
        'avg_wave_direction', 

        'atmospheric_pressure',
        'air_temp', 
        'water_temp', 
        'dewpoint',
        
    ]


    df = pd.DataFrame(data, columns=columns)
    df = df.replace("MM", pd.NA)
    print(df)

    return df



if __name__ == "__main__":
    print('transform_noaa_data(raw_data)')
    rd = extract_noaa_data()
    transform_noaa_data(rd)
    print()


if __name__ == "__main__":
    print()
    print(' transform_historical_station_data(min_ago, raw_data)')

    time_now = datetime.now(timezone.utc)
    tb = time_now - timedelta(minutes=40)
    time_before = datetime(tb.year, tb.month, tb.day, tb.hour, tb.minute, tzinfo=timezone.utc)

    rd = extract_historical_noaa_data('44007')
    transform_historical_station_data(time_before, rd)

    print()