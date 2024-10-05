import requests
import os
from dotenv import load_dotenv

load_dotenv()

appid = os.getenv("OPENWEATHER_API_KEY")


def fetch_temperature(city):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        if data['list']:
            city_id = data['list'][0]['id']
            weather_res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                        params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            weather_data = weather_res.json()
            city_temperature = weather_data['main']['temp']
            return city_temperature
        else:
            print("City not found.")
            return None
    except Exception as e:
        print("Error fetching temperature:", e)
        return None


if __name__ == "__main__":
    city_name = "Kiev"
    temperature = fetch_temperature(city_name)
    print(f"Temperature in {city_name}: {temperature}°C" if temperature is not None else "Failed to get temperature.")
