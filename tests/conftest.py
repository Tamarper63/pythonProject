# tests/conftest.py
import pytest
import yaml
from pathlib import Path


@pytest.fixture
def access_key_error_responses():
    """
    Fixture that loads access key error responses from a YAML file.
    """
    file_path = Path(__file__).parent / "data" / "access_key_error_responses.yaml"
    try:
        with file_path.open() as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        pytest.fail(f"The file {file_path} was not found.")
    except yaml.YAMLError as exc:
        pytest.fail(f"Error parsing YAML file {file_path}: {exc}")

# You can add more fixtures below as needed
