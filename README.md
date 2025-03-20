# Backend API Test Automation

This project demonstrates backend API testing using FastAPI for the server and Requests for testing. It includes automated tests and GitHub Actions integration.

## Features

-   FastAPI server with basic arithmetic endpoints
-   Automated tests using pytest
-   GitHub Actions integration for CI/CD
-   Parameterized test cases
-   Test coverage reporting

## API Endpoints

-   `GET /`: Root endpoint returning a hello message
-   `GET /add/{num1}/{num2}`: Adds two numbers
-   `GET /subtract/{num1}/{num2}`: Subtracts two numbers
-   `GET /multiply/{num1}/{num2}`: Multiplies two numbers

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python apiserver.py
```

The server will start at `http://localhost:8000`

## Running Tests

```bash
# Run tests with coverage report
pytest automation_test_pytest.py -v --cov=apiserver

# Run tests without coverage
pytest automation_test_pytest.py -v
```

## API Documentation

Once the server is running, you can access:

-   Swagger UI: `http://localhost:8000/docs`
-   ReDoc: `http://localhost:8000/redoc`

## GitHub Actions

The project includes GitHub Actions workflow that:

1. Sets up Python environment
2. Installs dependencies
3. Starts the FastAPI server
4. Runs automated tests

The workflow runs on push and pull requests.

## Test Cases

The test suite includes:

-   Basic arithmetic operations
-   Edge cases (negative numbers, zero)
-   Parameterized testing for multiple scenarios

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
6.
