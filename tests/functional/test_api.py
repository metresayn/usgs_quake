from api import fetch_and_transform_earthquake_property
from config import settings
import pytest
import json

START_DATE = "01-01-2017"
END_DATE = "01-01-2017"


@pytest.fixture
def earthquake_test_data():
    test_eq_data = fetch_and_transform_earthquake_property.EarthquakeJson(
        api_url=settings["api"].get("events_query"),
        retrieval_start_time=START_DATE,
        retrieval_end_time=END_DATE,
        api_limit=settings["api"].get("limit"),
        data_format=settings["api"].get("dataformat"),
        offset=1,
    )
    return test_eq_data


def test_dynaconf_settings():
    assert settings.database.database_name == "usgs"
    assert settings.database.username == "postgres"


def test_retrieve_data_from_api(earthquake_test_data):
    test_api_data = earthquake_test_data.retrieve_data_from_api()
    assert type(test_api_data) == dict
