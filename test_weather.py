import asyncio

from app.services.weather import get_current_temperature


async def main() -> None:
    temperature, date_time = await get_current_temperature(
        latitude=50.9848,
        longitude=11.0299,
    )

    print(f'Temperature: {temperature} °C')
    print(f'Date time: {date_time}')


asyncio.run(main())
