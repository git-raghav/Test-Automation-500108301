from locust import HttpUser, task, between

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
    def test_history(self):
        self.client.get("/history")
