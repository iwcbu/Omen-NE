# backend/app/data_pipeline/models.py


class IrlObs(object):
    def __init__(self, wave_height: float, wind_speed: WindSpeed, wind_direction: WindDirection, comments: str):
        self.obs_wave_height = wave_height
        self.obs_wind_speed = wind_speed
        self.obs_wind_direction = wind_direction
        self.comments = comments


class Source(object):
    def __init__(self, company: str, device: str, year: int):
        self.company = company
        self.device = device

        now = datetime.now()
        if year < 1990 or year > now.year:
            raise ValueError("Invalid year")
        
        self.year = year

    def __str__(self):
        return f"{self.company} {self.device} ~ {self.year}"

    def __repr__(self):
        return f"Source({self.company!r}, {self.device!r}, {self.year!r})"
