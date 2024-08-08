import requests
from tests.config import ACCESS_KEY

BASE_URL = "http://data.fixer.io/api"
LATEST_ENDPOINT = f"{BASE_URL}/latest"


def get_latest_exchange_rates(access_key):
    response = requests.get(LATEST_ENDPOINT, params={"access_key": access_key})
    return response.json()  # Return JSON response from the API
