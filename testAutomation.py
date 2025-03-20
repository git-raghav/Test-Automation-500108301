import requests


# Define test cases for the API endpoints


testcases = [
    {
        "url": "http://localhost:8000/add/2/2",
        "expected": 4,
        "description": "Test addition of 2 and 2"
    },
    {
        "url": "http://localhost:8000/subtract/2/2",
        "expected": 0,
        "description": "Test subtraction of 2 from 2"
    },
    {
        "url": "http://localhost:8000/multiply/2/2",
        "expected": 4,
        "description": "Test multiplication of 2 and 2"
    }
]
def test():
    """
    Runs automated tests on the API endpoints.
    Asserts that the API response matches the expected result.
    """
    for case in testcases:
        # Make a GET request to the API endpoint
        response = requests.get(case["url"])
        
        # Parse the JSON response
        result = response.json()["result"]
        
        # Assert that the result matches the expected value
        assert result == case["expected"], f"Test failed: {case['description']}. Expected {case['expected']}, got {result}"
        
        # Print success message if the test passes
        print(f"Test passed: {case['description']}")
    
    print("All tests passed!")
    
# Run the test function


test()

