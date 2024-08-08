# tests/test_exchange_rates.py
import pytest
import requests
from datetime import datetime
from jsonschema import validate, ValidationError

from tests.api_requests import LATEST_ENDPOINT, get_latest_exchange_rates
from tests.config import ACCESS_KEY
from tests.conftest import access_key_error_responses


@pytest.mark.parametrize("access_key, expected_error_response", access_key_error_responses())
def test_validate_access_key_errors(access_key, expected_error_response):
    """
    Test to validate error responses for different access keys.
    """
    response_json = get_latest_exchange_rates(access_key)
    assert response_json["error"]["code"] == expected_error_response["error"]["code"], \
        f"Expected error code {expected_error_response['error']['code']}, but got {response_json['error']['code']}"
    assert response_json["error"]["type"] == expected_error_response["error"]["type"], \
        f"Expected error type {expected_error_response['error']['type']}, but got {response_json['error']['type']}"
    assert response_json["error"]["info"] == expected_error_response["error"]["info"], \
        f"Expected error info {expected_error_response['error']['info']}, but got {response_json['error']['info']}"


def test_validate_default_base_currency_is_eur():
    """
    Test to validate that the default base currency is EUR.
    """
    response_json = get_latest_exchange_rates(ACCESS_KEY)
    assert response_json["base"] == "EUR", \
        f"Expected base currency 'EUR', but got {response_json['base']}"


def test_validate_response_types_is_valid(valid_response_schema):
    """
    Test to validate the response against the JSON schema.
    """
    response_json = get_latest_exchange_rates(ACCESS_KEY)

    try:
        validate(instance=response_json, schema=valid_response_schema)
    except ValidationError as e:
        pytest.fail(f"Response does not match schema: {e}")


def test_validate_response_date_is_today():
    """
    Test to validate that the response date is today's date.
    """
    response_json = get_latest_exchange_rates(ACCESS_KEY)

    date_from_response = response_json.get("date")
    assert date_from_response is not None, "Date field is missing in the response JSON"

    expected_date = datetime.now().strftime("%Y-%m-%d")
    assert date_from_response == expected_date, \
        f"Expected date {expected_date}, but got {date_from_response}"


def test_validate_response_headers():
    """
    Test to validate the response headers.
    """
    response = requests.get(LATEST_ENDPOINT, params={"access_key": ACCESS_KEY})
    response.raise_for_status()

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"].startswith("application/json"), \
        f"Expected Content-Type to start with 'application/json', but got {response.headers['Content-Type']}"
