# backend/app/data_pipeline/models.py

from enum import StrEnum


class StationRow(object):
    def __init__(self, STN, LAT, LON, TS, WDIR, WSPD, GST, WVHT, DPD, APD, MWD, PRES, PTDY, ATMP, WTMP, DEWP, VIS, TIDE):

        self.STN = STN # station id

        # global location: latidude and longitude
        self.LAT = LAT 
        self.LON = LON

        # timestamp: 
        self.timestamp = TS

        # wind measurements
        self.WDIR = WDIR if WDIR != "MM" else None    # wind direction in degrees from true north
        self.WSPD = WSPD if WSPD != "MM" else None    # wind speed in knots
        self.GST = GST if GST != "MM" else None      # maximum recorded wind speed since last record in knots

        # wave measurements
        self.WVHT = WVHT if WVHT != "MM" else None    # average wave height every 20 minutes in meters
        self.DPD = DPD if DPD != "MM" else None       # primary wave period, time interval in seconds between consecutive wave crests exhibiting max amount of energy
        self.APD = APD if APD != "MM" else None       # average wave period, time interval in seconds of all waves tracked during 20 minute sampling period
        self.MWD = MWD if MWD != "MM" else None       # average wave direction during 20 minute sampling period in degress from true north

        self.PRES = PRES if PRES != "MM" else None    # atmospheric pressure at sea level, measured in hectopascals (hPa) or millibars (mb)
        self.PTDY = PTDY if PTDY != "MM" else None    # pressure Tendency, direction (plus or minus) and total amount of atmospheric pressure change over the last 3 hours (hPa).
        self.ATMP = ATMP if ATMP != "MM" else None    # temperature of air in Celsius
        self.WTMP = WTMP if WTMP != "MM" else None    # temperature of the water close to surface in Celsius
        self.DEWP = DEWP if DEWP != "MM" else None    # min temp for water to become a gas in Celsius 
        self.VIS = VIS if VIS != "MM" else None       # visibility in natical miles (nmi)
        self.TIDE = TIDE if TIDE != "MM" else None    #height of local tide in feet above or below the average lower low water (MLLW) datum




class WindSpeed(StrEnum):
    ABSENT = "absent"
    SLOW = "slow"
    FAST = "fast"
    VERY_FAST = "very_fast"
    HURRICANE = "hurricane"

class WindDirection(StrEnum):
    OFFSHORE = "offshore"
    ONSHORE = "onshore"
    NEITHER = "neither"

class IrlObs(object):
    def __init__(self, wave_height: float, wind_speed: WindSpeed, wind_direction: WindDirection, comments: str):
        self.obs_wave_height = wave_height
        self.obs_wind_speed = wind_speed
        self.obs_wind_direction = wind_direction
        self.comments = comments