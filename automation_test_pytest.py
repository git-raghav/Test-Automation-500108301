import pytest

import requests

# Define test cases as a list of tuples for parameterized testing


testcases = [
    ("http://localhost:8000/add/2/2", 4, "Test addition of 2 and 2"),
    ("http://localhost:8000/subtract/2/2", 0, "Test subtraction of 2 from 2"),
    ("http://localhost:8000/multiply/2/2", 4, "Test multiplication of 2 and 2"),
    ("http://localhost:8000/add/-1/1", 0, "Test addition of -1 and 1"),
    ("http://localhost:8000/multiply/0/5", 0, "Test multiplication by zero"),
]
@pytest.mark.parametrize("url, expected, description", testcases)
def test_api(url, expected, description):
    """
    Parameterized test for API endpoints.
    """
    response = requests.get(url)
    result = response.json()["result"]
    assert result == expected, f"{description}. Expected {expected}, got {result}"
    
    
# Run tests using pytest


if __name__ == "__main__":
    pytest.main()
