from locust import HttpUser, task, between
from config import Config

class ArithmeticAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def test_add(self):
        self.client.get("/add/2/3")

    @task(1)
    def test_subtract(self):
        self.client.get("/subtract/5/3")

    @task(1)
    def test_multiply(self):
        self.client.get("/multiply/2/3")

    @task(1)
    def test_root(self):
        self.client.get("/")

if __name__ == "__main__":
    import os
    os.system(f"locust -f performance_test.py --host={Config.BASE_URL}")
