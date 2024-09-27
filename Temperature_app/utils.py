from City_app.models import DBCity
from City_app.schemas import City
from Temperature_app import crud
from Temperature_app.api_parser.parcer import get_temperature
from project_settings.dependecies import get_db


async def update_city_temperature(city: DBCity) -> City:
    async for db in get_db():
        city_schema = City(
            id=city.id,
            name=city.name,
            additional_info=city.additional_info
        )
        temperature = await get_temperature(city_schema.name)
        if temperature:
            temperature_data = {
                "city_id": city_schema.id,
                "temperature": temperature.get(city_schema.name)
            }
            temperature_model = await crud.create_temperature(
                db=db,
                temperature_data=temperature_data
            )
            city_schema.temperatures = [temperature_model]
        else:
            city_schema.temperatures = []
        return city_schema
