from locust import HttpUser, task, between
from config import Config
import json

class ArithmeticAPIUser(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        """Register and login before starting tests"""
        # Register user
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
        response = self.client.post("/register", json=register_data)
        if response.status_code == 200:
            self.token = response.json()["access_token"]
        else:
            # If registration fails, try to login
            login_data = {
                "username": "testuser",
                "password": "testpassword"
            }
            response = self.client.post("/token", data=login_data)
            if response.status_code == 200:
                self.token = response.json()["access_token"]
            else:
                raise Exception("Failed to authenticate")

    @task(1)
    def test_add(self):
        if self.token:
            self.client.get("/add/2/3", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def test_subtract(self):
        if self.token:
            self.client.get("/subtract/5/3", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def test_multiply(self):
        if self.token:
            self.client.get("/multiply/2/3", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def test_root(self):
        if self.token:
            self.client.get("/", headers={"Authorization": f"Bearer {self.token}"})

if __name__ == "__main__":
    import os
    os.system(f"locust -f performance_test.py --host={Config.BASE_URL}")
