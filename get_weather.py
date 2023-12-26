import requests
import os


API_KEY = os.environ["weatherapi_key"]
URL = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}"


def get_weather(city: str = "Tokyo") -> int:
    data = requests.get(URL, params={"q": city}).json()
    temperature = data["current"]["temp_c"]

    return int(temperature)


if __name__ == "__main__":
    print(get_weather())
