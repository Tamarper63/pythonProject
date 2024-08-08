# tests/test_exchange_rates.py
import pytest
from datetime import datetime
import requests
from jsonschema import validate, ValidationError
from tests.api_requests import get_latest_exchange_rates, LATEST_ENDPOINT
from tests.config import ACCESS_KEY


@pytest.mark.parametrize("access_key, expected_error_response", [
    ("", {
        "success": False,
        "error": {
            "code": 101,
            "type": "missing_access_key",
            "info": "You have not supplied an API Access Key. [Required format: access_key=YOUR_ACCESS_KEY]"
        }
    }),
    ("invalid_key", {
        "success": False,
        "error": {
            "code": 101,
            "type": "invalid_access_key",
            "info": "You have not supplied a valid API Access Key. [Technical Support: support@apilayer.com]"
        }
    })
])
def test_validate_access_key_errors(access_key, expected_error_response):
    response_json = get_latest_exchange_rates(access_key)
    assert response_json["error"]["code"] == expected_error_response["error"]["code"]
    assert response_json["error"]["type"] == expected_error_response["error"]["type"]
    assert response_json["error"]["info"] == expected_error_response["error"]["info"]


def test_validate_default_base_currency_is_eur():
    response_json = get_latest_exchange_rates(ACCESS_KEY)
    assert response_json["base"] == "EUR"


def test_validate_response_types_is_valid(valid_response_schema):
    response_json = get_latest_exchange_rates(ACCESS_KEY)

    try:
        validate(instance=response_json, schema=valid_response_schema)
    except ValidationError as e:
        pytest.fail(f"Response does not match schema: {e}")


def test_validate_response_date_is_today():
    response_json = get_latest_exchange_rates(ACCESS_KEY)

    date_from_response = response_json.get("date")
    assert date_from_response is not None, "Date field is missing in the response JSON"

    expected_date = datetime.now().strftime("%Y-%m-%d")
    assert date_from_response == expected_date, f"Expected date {expected_date}, but got {date_from_response}"


def test_validate_response_headers():
    response = requests.get(LATEST_ENDPOINT, params={"access_key": ACCESS_KEY})
    response.raise_for_status()

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
