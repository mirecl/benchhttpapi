from locust import HttpUser, task, between
import warnings

warnings.filterwarnings("ignore")

test_case = [
    {
        "date": "12.10.2021",
        "amount": 450000,
        "rate": 3.7,
        "periods": 12,
    },
    {
        "date": "12.01.2021",
        "amount": 450000,
        "rate": 3.7,
        "periods": 12,
    },
    {
        "date": "12.01.2021",
        "amount": 500000,
        "rate": 6,
        "periods": 12,
    },
    {
        "date": "12.01.2021",
        "amount": 500000,
        "rate": 4,
        "periods": 8,
    },
    {
        "date": "12.01.2021",
        "amount": 500000,
        "rate": 4,
        "periods": 34,
    },
    {
        "date": "31.12.2021",
        "amount": 10000,
        "rate": 3.5,
        "periods": 60,
    },
    {
        "date": "31.12.2020",
        "amount": 300000,
        "rate": 6,
        "periods": 20,
    },
    {
        "date": "31.12.2021",
        "amount": 450000,
        "rate": 3.7,
        "periods": 1,
    },
]


class Nt(HttpUser):
    wait_time = between(0.01, 0.01)

    @task(5)
    def mdeposit1(self):
        r = self.client.post(
            "/deposit",
            json=test_case[0],
            name="not valid date",
            catch_response=True,
        )
        if r.status_code == 400:
            r.success()

    @task(4)
    def mdeposit2(self):
        r = self.client.post(
            "/deposit",
            json=test_case[1],
            name="not valid amount",
            catch_response=True,
        )
        if r.status_code == 400:
            r.success()

    @task(1)
    def mdeposit3(self):
        r = self.client.post(
            "/deposit",
            json=test_case[2],
            name="not valid rate",
            catch_response=True,
        )
        if r.status_code == 400:
            r.success()

    @task(1)
    def mdeposit4(self):
        r = self.client.post(
            "/deposit",
            json=test_case[3],
            name="not valid period#1",
            catch_response=True,
        )
        if r.status_code == 400:
            r.success()

    @task(1)
    def mdeposit5(self):
        r = self.client.post(
            "/deposit",
            json=test_case[4],
            name="not valid period#2",
            catch_response=True,
        )
        if r.status_code == 400:
            r.success()

    @task(100)
    def mdeposit6(self):
        self.client.post(
            "/deposit",
            json=test_case[5],
            name="valid 60 periods",
        )

    @task(50)
    def mdeposit7(self):
        self.client.post(
            "/deposit",
            json=test_case[6],
            name="valid 20 periods",
        )

    @task(10)
    def mdeposit8(self):
        self.client.post(
            "/deposit",
            json=test_case[7],
            name="valid 1 periods",
        )
