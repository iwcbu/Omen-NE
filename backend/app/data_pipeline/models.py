# backend/app/data_pipeline/models.py


class RawStationRow(object):
    def __init__(self, params):

        self.STN = params.STN # station id

        # global location: latidude and longitude
        self.LAT = params.LAT 
        self.LON = params.LON

        # timestamp: year, month, day (24h), hour, minute
        self.YYYY = params.YYYY
        self.MM = params.MM
        self.DD = params.DD
        self.hh = params.hh
        self.mm = params.mm

        # wind measurements
        self.WDIR = params.WDIR if params.WDIR != "MM" else None    # wind direction in degrees from true north
        self.WSPD = params.WSPD if params.WDIR != "MM" else None    # wind speed in knots
        self.GST = params.GST if params.WDIR != "MM" else None      # maximum recorded wind speed since last record in knots

        # wave measurements
        self.WVHT = params.WVHT if params.WDIR != "MM" else None    # average wave height every 20 minutes in meters
        self.DPD = params.DPD if params.DPD != "MM" else None       # primary wave period, time interval in seconds between consecutive wave crests exhibiting max amount of energy
        self.APD = params.APD if params.APD != "MM" else None       # average wave period, time interval in seconds of all waves tracked during 20 minute sampling period
        self.MWD = params.MWD if params.MWD != "MM" else None       # average wave direction during 20 minute sampling period in degress from true north

        self.PRES = params.PRES if params.PRES != "MM" else None    # atmospheric pressure at sea level, measured in hectopascals (hPa) or millibars (mb)
        self.PTDY = params.PTDY if params.PTDY != "MM" else None    # pressure Tendency, direction (plus or minus) and total amount of atmospheric pressure change over the last 3 hours (hPa).
        self.ATMP = params.ATMP if params.ATMP != "MM" else None    # temperature of air in Celsius
        self.WTMP = params.WTMP if params.WTMP != "MM" else None    # temperature of the water close to surface in Celsius
        self.DEWP = params.DEWP if params.DEWP != "MM" else None    # min temp for water to become a gas in Celsius 
        self.VIS = params.VIS if params.VIS != "MM" else None       # visibility in natical miles (nmi)
        self.TIDE = params.TIDE if params.TIDE != "MM" else None    #height of local tide in feet above or below the average lower low water (MLLW) datum


class WaveStation(object):
    def __init__(self, station: RawStationRow):
        self.id = station.STN

        # location
        self.lat = station.LAT | None
        self.lon = station.LON | None

        # timestamp
        self.year = station.YYYY
        self.month = station.MM
        self.day = station.DD
        self.hour = station.hh
        self.minute = station.mm

        # wave measurements
        self.waveHeight = station.WVHT
        self.primaryPeriod = station.DPD
        self.avgPeriod = station.APD
        self.avgDirection = station.MWD



class WindStation(object):
    def __init__(self, station: RawStationRow):
        self.id = station.STN

        # location
        self.lat = station.LAT | None
        self.lon = station.LON | None

        # timestamp
        self.year = station.YYYY
        self.month = station.MM
        self.day = station.DD
        self.hour = station.hh
        self.minute = station.mm

        # wind measurements
        self.direction = station.WDIR
        self.speed = station.WSPD
        self.maxSpeed= station.g