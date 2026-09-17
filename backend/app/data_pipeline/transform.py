# backend/app/data_pipeline/transform.py

from extract import extract_noaa_data
import pandas as pd


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


if __name__ == "__main__":
    rd = extract_noaa_data()
    transform_noaa_data(rd)