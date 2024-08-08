import requests
from datetime import datetime
from jsonschema import validate, ValidationError
from config import ACCESS_KEY
import pytest

BASE_URL = "http://data.fixer.io/api"
LATEST_ENDPOINT = f"{BASE_URL}/latest"

def test_validate_empty_access_key_returns_error_response():
    response = requests.get(LATEST_ENDPOINT, params={"access_key": ""})
    response_json = response.json()
    expected_error_response = {
        "success": False,
        "error": {
            "code": 101,
            "type": "missing_access_key",
            "info": "You have not supplied an API Access Key. [Required format: access_key=YOUR_ACCESS_KEY]"
        }
    }
    assert response_json["error"]["code"] == expected_error_response["error"]["code"]
    assert response_json["error"]["type"] == expected_error_response["error"]["type"]
    assert response_json["error"]["info"] == expected_error_response["error"]["info"]

def test_validate_default_base_currency_is_eur():
    response = requests.get(LATEST_ENDPOINT, params={"access_key": "953a6948da5d998c7565867c5c5aef94"})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["base"] == "EUR"

def test_validate_response_types_is_valid():
    response = requests.get(LATEST_ENDPOINT, params={"access_key": "953a6948da5d998c7565867c5c5aef94"})
    assert response.status_code == 200
    response_json = response.json()
    schema = {
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "base": {"type": "string"},
            "date": {"type": "string"},
            "rates": {"type": "object"}
        },
        "required": ["success", "base", "date", "rates"]
    }
    try:
        validate(instance=response_json, schema=schema)
    except ValidationError as e:
        assert False, f"Response does not match schema: {e}"

def test_validate_response_date_is_today():
    response = requests.get(LATEST_ENDPOINT, params={"access_key": ACCESS_KEY})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["date"] == datetime.now().strftime("%Y-%m-%d")

def test_validate_invalid_access_key_returns_error_response():
    response = requests.get(LATEST_ENDPOINT, params={"access_key": "953a6948da5d998c7565867c5c5aef98"})
    response_json = response.json()
    expected_error_response = {
        "success": False,
        "error": {
            "code": 101,
            "type": "invalid_access_key",
            "info": "You have not supplied a valid API Access Key. [Technical Support: support@apilayer.com]"
        }
    }
    assert response_json["error"]["code"] == expected_error_response["error"]["code"]
    assert response_json["error"]["type"] == expected_error_response["error"]["type"]
    assert response_json["error"]["info"] == expected_error_response["error"]["info"]

def test_validate_response_headers():
    response = requests.get(LATEST_ENDPOINT, params={"access_key": ACCESS_KEY})
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
