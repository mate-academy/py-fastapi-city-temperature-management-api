import httpx
from typing import Optional
import logging
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

# Reusable HTTP client for better performance when making multiple parallel requests
# This avoids repeated TCP/TLS handshakes
_http_client: Optional[httpx.AsyncClient] = None


def get_http_client() -> httpx.AsyncClient:
    """
    Returns a singleton AsyncClient instance for HTTP requests.
    Creates the client on first call if it doesn't exist.
    """
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(timeout=10.0)
    return _http_client


async def close_http_client():
    """
    Closes the HTTP client. Should be called on application shutdown.
    """
    global _http_client
    if _http_client is not None:
        await _http_client.aclose()
        _http_client = None


async def get_temperature_for_city(city_name: str) -> Optional[float]:
    """
    Fetches current temperature for a city from wttr.in API.
    Args:
        city_name: City name
    Returns:
        Temperature in Celsius or None if data could not be fetched
    Raises:
        httpx.HTTPError: If HTTP request error occurred
    """
    try:
        # Use reusable HTTP client for better performance
        client = get_http_client()

        # URL for wttr.in API (free, no API key required)
        # URL-encode city name to handle spaces and special characters
        encoded_city_name = quote_plus(city_name)
        url = f"https://wttr.in/{encoded_city_name}?format=j1"

        response = await client.get(url)
        response.raise_for_status()  # Raises exception for HTTP errors

        data = response.json()
        # Extract temperature from response
        temperature = float(data["current_condition"][0]["temp_C"])

        logger.info(f"Fetched temperature for {city_name}: {temperature}°C")
        return temperature

    except httpx.HTTPError as e:
        logger.error(f"HTTP request error for {city_name}: {e}")
        return None
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"Data parsing error for {city_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error for {city_name}: {e}")
        return None
