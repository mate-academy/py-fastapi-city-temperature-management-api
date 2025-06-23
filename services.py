import aiohttp


async def fetch_temperature(city_name: str) -> float:
    # Заглушка: используем фиктивную температуру
    async with aiohttp.ClientSession() as session:
        # Здесь может быть реальный API, например OpenWeather или Open-Meteo
        # Здесь просто мок-значение
        return 25.0 + hash(city_name) % 10  # Псевдо-реализация
