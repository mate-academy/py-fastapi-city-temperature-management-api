import os

import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

URL = "https://api.weatherapi.com/v1/current.json"
FILTERING = "Paris"
API_KEY = os.environ.get("API_KEY")


def get_weather(
        filtering: str,
        url: str = URL,
        api_key: str = API_KEY
) -> None:
    """Get weather from API and print it."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    msg_api = f"You need to visit {domain} and get your API key."
    msg_doc = f"You may visit {domain}/docs/ for more information."

    params = {"key": api_key, "q": filtering}

    try:
        res = requests.get(url, params=params).json()
    except Exception as e:
        print(e, msg_doc)
        return

    if "error" not in res:
        temp = res["current"]["temp_c"]
        return temp

    else:
        print(msg_api, res["error"]["message"])
        return
