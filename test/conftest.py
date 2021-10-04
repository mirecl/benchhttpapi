import pytest
import requests
from functools import partial
import zlib
import pickle
import json

URL = "http://localhost:8081/deposit"


@pytest.fixture(scope="session")
def client():
    return partial(requests.post, URL)


def pytest_generate_tests(metafunc):
    if "data_request" not in metafunc.fixturenames:
        return

    with open("test/cases.pkl", "rb") as f:
        tmp = pickle.load(f)

    test_cases = json.loads(zlib.decompress(tmp))

    # Предусматриваем неправильную загрузку и пустой файл
    if not test_cases:
        raise ValueError("Test cases not loaded")

    return metafunc.parametrize(
        "data_request, data_response",
        [(row["request"], row["response"]) for row in test_cases],
        ids=[row["id"] for row in test_cases],
    )
