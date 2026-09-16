from fastapi import FastAPI

from api.routes import health, forecast, spots

app = FastAPI()

app.include_router(health.router)
app.include_router(forecast.router)
app.include_router(spots.router)
