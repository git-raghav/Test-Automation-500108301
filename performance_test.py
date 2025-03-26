from locust import HttpUser, task, between
import time
import uuid
from typing import Optional
import logging
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArithmeticAPIUser(HttpUser):
    wait_time = between(1, 3)
    max_retries = 3
    timeout = 10
    _token: Optional[str] = None

    def on_start(self):
        """Initialize user session with registration and login."""
        # Generate unique username and email
        unique_id = str(uuid.uuid4())[:8]
        self.username = f"testuser_{unique_id}"
        self.email = f"test_{unique_id}@example.com"
        self.password = "testpassword123"

        # Try to register and login with retries
        for attempt in range(self.max_retries):
            try:
                # Register new user
                register_response = self.client.post(
                    "/register",
                    json={
                        "username": self.username,
                        "email": self.email,
                        "password": self.password
                    },
                    timeout=self.timeout
                )

                if register_response.status_code == 200:
                    logger.info(f"Successfully registered user {self.username}")
                    break
                elif register_response.status_code == 400 and "already registered" in register_response.text.lower():
                    logger.info(f"User {self.username} already exists, proceeding to login")
                    break
                else:
                    logger.error(f"Registration failed: {register_response.text}")
                    if attempt == self.max_retries - 1:
                        raise Exception("Failed to register user after maximum retries")

                # Login
                login_response = self.client.post(
                    "/token",
                    data={
                        "username": self.username,
                        "password": self.password
                    },
                    timeout=self.timeout
                )

                if login_response.status_code == 200:
                    self._token = login_response.json()["access_token"]
                    logger.info(f"Successfully logged in user {self.username}")
                    break
                else:
                    logger.error(f"Login failed: {login_response.text}")
                    if attempt == self.max_retries - 1:
                        raise Exception("Failed to login after maximum retries")

            except Exception as e:
                logger.error(f"Error during user initialization: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2)  # Wait before retry

        if not self._token:
            raise Exception("Failed to initialize user session")

    @task(1)
    def test_add(self):
        """Test addition operation."""
        try:
            response = self.client.post(
                "/add",
                json={"num1": 5, "num2": 3},
                headers={"Authorization": f"Bearer {self._token}"},
                timeout=self.timeout
            )

            if response.status_code != 200:
                logger.error(f"Add operation failed: {response.text}")
                self.environment.events.request_failure.fire(
                    request_type="POST",
                    name="/add",
                    response_time=0,
                    response_length=0,
                    exception=Exception(f"Add operation failed: {response.text}")
                )
        except Exception as e:
            logger.error(f"Error in add operation: {str(e)}")
            self.environment.events.request_failure.fire(
                request_type="POST",
                name="/add",
                response_time=0,
                response_length=0,
                exception=e
            )

    @task(1)
    def test_subtract(self):
        """Test subtraction operation."""
        try:
            response = self.client.post(
                "/subtract",
                json={"num1": 10, "num2": 4},
                headers={"Authorization": f"Bearer {self._token}"},
                timeout=self.timeout
            )

            if response.status_code != 200:
                logger.error(f"Subtract operation failed: {response.text}")
                self.environment.events.request_failure.fire(
                    request_type="POST",
                    name="/subtract",
                    response_time=0,
                    response_length=0,
                    exception=Exception(f"Subtract operation failed: {response.text}")
                )
        except Exception as e:
            logger.error(f"Error in subtract operation: {str(e)}")
            self.environment.events.request_failure.fire(
                request_type="POST",
                name="/subtract",
                response_time=0,
                response_length=0,
                exception=e
            )

    @task(1)
    def test_multiply(self):
        """Test multiplication operation."""
        try:
            response = self.client.post(
                "/multiply",
                json={"num1": 6, "num2": 7},
                headers={"Authorization": f"Bearer {self._token}"},
                timeout=self.timeout
            )

            if response.status_code != 200:
                logger.error(f"Multiply operation failed: {response.text}")
                self.environment.events.request_failure.fire(
                    request_type="POST",
                    name="/multiply",
                    response_time=0,
                    response_length=0,
                    exception=Exception(f"Multiply operation failed: {response.text}")
                )
        except Exception as e:
            logger.error(f"Error in multiply operation: {str(e)}")
            self.environment.events.request_failure.fire(
                request_type="POST",
                name="/multiply",
                response_time=0,
                response_length=0,
                exception=e
            )

    @task(1)
    def test_root(self):
        """Test square root operation."""
        try:
            response = self.client.post(
                "/root",
                json={"number": 16},
                headers={"Authorization": f"Bearer {self._token}"},
                timeout=self.timeout
            )

            if response.status_code != 200:
                logger.error(f"Root operation failed: {response.text}")
                self.environment.events.request_failure.fire(
                    request_type="POST",
                    name="/root",
                    response_time=0,
                    response_length=0,
                    exception=Exception(f"Root operation failed: {response.text}")
                )
        except Exception as e:
            logger.error(f"Error in root operation: {str(e)}")
            self.environment.events.request_failure.fire(
                request_type="POST",
                name="/root",
                response_time=0,
                response_length=0,
                exception=e
            )

if __name__ == "__main__":
    import os
    os.system(f"locust -f performance_test.py --host={Config.BASE_URL}")
