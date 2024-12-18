import httpx
import os
from dotenv import load_dotenv
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Завантаження API ключа з файлу .env
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise EnvironmentError("API key not found. Please check your .env file or environment variables.")

async def fetch_temperature(city_name: str) -> float:
    """
    Функція для отримання температури міста з API WeatherAPI.

    :param city_name: Назва міста
    :return: Температура у градусах Цельсія
    :raises: HTTPStatusError, RequestError, ValueError
    """
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city_name}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()  # Перевірка на код HTTP 4xx/5xx
            data = response.json()

            # Перевірка структури відповіді
            if "current" in data and "temp_c" in data["current"]:
                return data["current"]["temp_c"]
            elif "error" in data:  # Обробка можливої помилки з API
                raise ValueError(f"API error: {data['error'].get('message', 'Unknown error')}")
            else:
                raise ValueError(f"Unexpected response structure: {data}")

    except httpx.HTTPStatusError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")  # Можливий код помилки 401, 404 тощо
        raise
    except httpx.RequestError as req_err:
        logger.error(f"Request error occurred: {req_err}")  # Проблеми з мережею
        raise
    except KeyError:
        logger.error("Unexpected response structure from the weather API")  # Неочікувана структура
        raise
