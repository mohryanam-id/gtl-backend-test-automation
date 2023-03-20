import configparser
from datetime import date
import io
import logging
import os
import requests
import csv
import pytest
from tests.util.configuration import Configuration

cwd = os.getcwd()

from tests.util.securitieslistcomparator import SecuritiesListComparer

@pytest.fixture(scope="session")
def config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


@pytest.mark.parametrize("params, expected_content_file_path", [
    ({"page": 1}, os.path.join(cwd,"tests","data","expected_securities_page_1.csv")),
    ({"page": 10},os.path.join(cwd,"tests","data","expected_securities_page_10.csv")),
    ({"page": 20},os.path.join(cwd,"tests","data","expected_securities_page_20.csv")),
])
def test_get_securities_list(params: tuple, expected_content_file_path: str, caplog):
    caplog = logging.getLogger(__name__)
    caplog.setLevel(logging.INFO)
    
    url = Configuration().items["example_api"]["url"]
    params["size"] = int(Configuration().items["example_api"]["page_size"])
    
    response = requests.get(url, params=params)
    
    assert response.status_code == 200
    assert response.content is not None

    # Assert that the content is equal
    actual_content = response.content.decode("utf-8")
    actual_csv = csv.DictReader(io.StringIO(actual_content))
    expected_csv = csv.DictReader(open(expected_content_file_path))
    securities_list_comparer = SecuritiesListComparer(actual_csv, expected_csv)

    
    added_securities_list, removed_securities_list, updated_security_list = securities_list_comparer.compare()

    caplog.info("Added securities:")
    for securities in added_securities_list:
        caplog.info(str(securities))

    caplog.info("Removed securities:")
    for securities in removed_securities_list:
        caplog.info(str(securities))

    caplog.info("Updated securities:")
    for securities in updated_security_list:
        caplog.info(str(securities))

    assert ((len(added_securities_list) == 0) and (len(removed_securities_list) == 0) and (len(updated_security_list) == 0))


