import requests

testcases = [
    {
        "url": "http://localhost:8000/add/2/2",
        "expected": 4
    },
    {
        "url": "http://localhost:8000/subtract/2/2",
        "expected": 0
    },
    {
        "url": "http://localhost:8000/multiply/2/2",
        "expected": 4
    }
]


def test():
    for case in testcases:
        response = requests.get(case["url"])
        assert response.json()["result"] == case["expected"]
    print("All tests pass")
    
    
test()