from datetime import datetime as dt


def test_service(data_request, data_response, client):
    resp = client(json=data_request)
    assert resp.status_code == data_response["code"]

    if resp.status_code == 400:
        res = resp.json()
        assert res["error"] != None

    if resp.status_code == 200:
        current_response = {
            "date": None,
            "sum": None,
            "sum_s": None,
            "sum_e": None,
        }
        res = resp.json()
        current_response["sum"] = round(sum(res.values()))
        current_response["date"] = [
            dt.strftime(d, "%d.%m.%Y")
            for d in sorted(dt.strptime(row, "%d.%m.%Y") for row in res.keys())
        ]
        current_response["sum_s"] = round(res[current_response["date"][0]])
        current_response["sum_e"] = round(res[current_response["date"][-1]])

        assert current_response["date"] == data_response["date"]
        assert 0 <= abs(current_response["sum"] - data_response["sum"]) <= 20
        assert 0 <= abs(current_response["sum_s"] - data_response["sum_s"]) <= 2
        assert 0 <= abs(current_response["sum_e"] - data_response["sum_e"]) <= 2
