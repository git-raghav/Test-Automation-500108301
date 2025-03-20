import os
from typing import Dict

class Config:
    # Base configuration
    BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

    # Environment specific settings
    ENV = os.getenv("ENV", "development")

    # Test configuration
    TEST_TIMEOUT = int(os.getenv("TEST_TIMEOUT", "30"))
    PERFORMANCE_TEST_USERS = int(os.getenv("PERFORMANCE_TEST_USERS", "10"))
    PERFORMANCE_TEST_SPAWN_RATE = int(os.getenv("PERFORMANCE_TEST_SPAWN_RATE", "1"))

    # Environment specific configurations
    ENVIRONMENTS: Dict[str, Dict] = {
        "development": {
            "base_url": "http://localhost:8000",
            "timeout": 30,
            "debug": True
        },
        "staging": {
            "base_url": "http://staging-api.example.com",
            "timeout": 60,
            "debug": False
        },
        "production": {
            "base_url": "http://api.example.com",
            "timeout": 60,
            "debug": False
        }
    }

    @classmethod
    def get_config(cls) -> Dict:
        return cls.ENVIRONMENTS.get(cls.ENV, cls.ENVIRONMENTS["development"])
