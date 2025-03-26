from locust import HttpUser, task, between
from config import Config
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArithmeticAPIUser(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        """Register and login before starting tests"""
        try:
            # Register user
            register_data = {
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpassword"
            }
            response = self.client.post("/register", json=register_data)
            logger.info(f"Register response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                self.token = response.json()["access_token"]
                logger.info("Successfully registered and got token")
            else:
                # If registration fails, try to login
                login_data = {
                    "username": "testuser",
                    "password": "testpassword"
                }
                response = self.client.post("/token", data=login_data)
                logger.info(f"Login response: {response.status_code} - {response.text}")

                if response.status_code == 200:
                    self.token = response.json()["access_token"]
                    logger.info("Successfully logged in and got token")
                else:
                    logger.error(f"Failed to authenticate. Status: {response.status_code}, Response: {response.text}")
                    raise Exception(f"Failed to authenticate: {response.text}")
        except Exception as e:
            logger.error(f"Error in on_start: {str(e)}")
            raise

    @task(1)
    def test_add(self):
        if self.token:
            try:
                response = self.client.get("/add/2/3", headers={"Authorization": f"Bearer {self.token}"})
                if response.status_code != 200:
                    logger.error(f"Add operation failed: {response.status_code} - {response.text}")
            except Exception as e:
                logger.error(f"Error in test_add: {str(e)}")

    @task(1)
    def test_subtract(self):
        if self.token:
            try:
                response = self.client.get("/subtract/5/3", headers={"Authorization": f"Bearer {self.token}"})
                if response.status_code != 200:
                    logger.error(f"Subtract operation failed: {response.status_code} - {response.text}")
            except Exception as e:
                logger.error(f"Error in test_subtract: {str(e)}")

    @task(1)
    def test_multiply(self):
        if self.token:
            try:
                response = self.client.get("/multiply/2/3", headers={"Authorization": f"Bearer {self.token}"})
                if response.status_code != 200:
                    logger.error(f"Multiply operation failed: {response.status_code} - {response.text}")
            except Exception as e:
                logger.error(f"Error in test_multiply: {str(e)}")

    @task(1)
    def test_root(self):
        if self.token:
            try:
                response = self.client.get("/", headers={"Authorization": f"Bearer {self.token}"})
                if response.status_code != 200:
                    logger.error(f"Root operation failed: {response.status_code} - {response.text}")
            except Exception as e:
                logger.error(f"Error in test_root: {str(e)}")

if __name__ == "__main__":
    import os
    os.system(f"locust -f performance_test.py --host={Config.BASE_URL}")
