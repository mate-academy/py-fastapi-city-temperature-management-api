from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int | None = None

    class Config:

        orm_mode = True


class get_temperature(BaseModel):
    city_name: str


# schemas for json response
class CoordInfo(BaseModel):
    lon: float | None = None
    lat: float | None = None

class WeatherInfo(BaseModel):
    id: int | None = None
    main: str | None = None
    description: str | None = None
    icon: str | None = None
    
    class Config:

        orm_mode = True

class MainInfo(BaseModel):
    temp: float | None = None
    feels_like: float | None = None
    temp_min: float | None = None
    temp_max: float | None = None
    pressure: int | None = None
    humidity: int | None = None
    sea_level: int | None = None
    grnd_level: int | None = None

class WindInfo(BaseModel):
    speed: float | None = None
    deg: float | None = None
    gust: float | None = None

class CloudsInfo(BaseModel):
    all: int | None = None

class SysInfo(BaseModel):
    type: int | None = None
    id: int | None = None
    country: str | None = None
    sunrise: int | None = None
    sunset: int | None = None

class FullWeatherInfo(BaseModel):
    coord: CoordInfo
    weather: list[WeatherInfo]
    base: str
    main: MainInfo
    visibility: int
    wind: WindInfo
    clouds: CloudsInfo
    dt: int
    sys: SysInfo
    timezone: int
    id: int
    name: str
    cod: int
