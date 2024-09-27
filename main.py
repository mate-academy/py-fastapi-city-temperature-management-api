from datetime import datetime

import pytz
from fastapi import FastAPI
from City_app.router import city_router
from Temperature_app.router import temperature_router


app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
def main() -> dict:
    local_tz = pytz.timezone("Europe/Kiev")
    local_time = datetime.now(local_tz)
    return {"local_time": local_time.strftime("%Y-%m-%d %H:%M:%S")}
