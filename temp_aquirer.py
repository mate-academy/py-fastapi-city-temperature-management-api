import random


async def get_temperature_for_city(city_name: str) -> float:
    """
    Заглушка для отримання температури міста.
    В реальному проекті тут має бути інтеграція з API погоди.
    """
    # Симулюємо температуру від -30 до +40 градусів
    return round(random.uniform(-30.0, 40.0), 1)
