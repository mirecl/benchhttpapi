import pytest
import requests
from functools import partial
import zlib
import pickle
import json
import inquirer
import os

URL = "http://127.0.0.1:8000/deposit"


@pytest.fixture(scope="session")
def client():
    return partial(requests.post, URL)


def pytest_generate_tests(metafunc):
    questions = [
        inquirer.List(
            "case",
            message="Укажите набор тест-кейсов:",
            choices=sorted(
                [
                    row.split(".")[0]
                    for row in filter(
                        lambda x: x.endswith(".pkl"), os.listdir("test/cases")
                    )
                ],
                reverse=True,
            ),
        ),
    ]
    answers = inquirer.prompt(questions)
    print(f"Подождите, идет загрузка {answers['case']}...\n")

    if "data_request" not in metafunc.fixturenames:
        return

    with open(f"test/cases/{answers['case']}.pkl", "rb") as f:
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
