# FastAPI Test Automation Project

A comprehensive FastAPI backend with automated testing and CI/CD integration using GitHub Actions. This project demonstrates best practices in API development, testing, and continuous integration.

## Features

### API Features

-   Basic arithmetic operations (add, subtract, multiply, square root)
-   User authentication with JWT tokens
-   Operation history tracking
-   Input validation
-   Error handling
-   Logging system

### Testing Features

-   Unit tests with pytest
-   Integration tests
-   Performance testing with Locust
-   Test coverage reporting
-   Allure test reports
-   HTML test reports

### CI/CD Features

-   Automated testing with GitHub Actions
-   PostgreSQL service container
-   Environment configuration
-   Test report generation
-   Artifact storage

## Troubleshooting

### Initial GitHub Actions Issues and Solutions

The workflow initially failed due to several issues that were resolved:

1. **Invalid Workflow File**

    - Error: "Invalid workflow file: .github/workflows/TestAutomation.yml#L18"
    - Cause: Multiple 'run' commands in the same step
    - Solution: Separated commands into different steps and fixed YAML syntax

2. **Missing Action Version**

    - Error: "Missing download info for actions/upload-artifact@v2"
    - Cause: Outdated action version
    - Solution: Updated to actions/upload-artifact@v4

3. **Test Execution Failure**

    - Error: "Process completed with exit code 2"
    - Cause: Missing dependencies and import issues
    - Solution: Added httpx and starlette to requirements.txt, fixed test imports

4. **Missing Artifacts**
    - Error: "No files were found with the provided path: ./allure-results"
    - Cause: Directory not created before running tests
    - Solution: Added step to create allure-results directory

These issues were resolved by:

-   Fixing YAML syntax in workflow file
-   Updating GitHub Actions versions
-   Adding missing dependencies
-   Creating necessary directories
-   Improving test structure

## Prerequisites

-   Python 3.8+
-   PostgreSQL (for production)
-   Git

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd Test-Automation-500108301
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

## Configuration

1. Set up environment variables:

```bash
# Create a .env file with the following variables
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/arithmetic_db
ENV=development
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

2. Initialize the database:

```bash
python -c "from database import init_db; import asyncio; asyncio.run(init_db())"
```

## Running the Application

1. Start the FastAPI server:

```bash
python apiserver.py
```

The server will be available at `http://localhost:8000`

2. Access the API documentation:

-   Swagger UI: `http://localhost:8000/docs`
-   ReDoc: `http://localhost:8000/redoc`

## Running Tests

1. Run all tests with coverage:

```bash
pytest automation_test_pytest.py -v \
  --cov=apiserver \
  --html=report.html \
  --self-contained-html \
  --alluredir=./allure-results
```

2. Run performance tests:

```bash
locust -f performance_test.py --host=http://localhost:8000
```

## API Endpoints

### Authentication

-   `POST /register` - Register a new user
-   `POST /token` - Login and get access token

### Arithmetic Operations

-   `POST /add` - Add two numbers
-   `POST /subtract` - Subtract two numbers
-   `POST /multiply` - Multiply two numbers
-   `POST /root` - Calculate square root

### User Operations

-   `GET /history` - Get user's operation history

## Project Structure

```
Test-Automation-500108301/
├── .github/
│   └── workflows/
│       └── TestAutomation.yml
├── apiserver.py
├── automation_test_pytest.py
├── performance_test.py
├── config.py
├── auth.py
├── database.py
├── logger.py
├── models.py
├── base.py
├── requirements.txt
└── README.md
```

## Testing Features

### Unit Tests

-   Authentication tests
-   Arithmetic operation tests
-   Database operation tests
-   Error handling tests

### Integration Tests

-   API endpoint integration tests
-   Database integration tests
-   Authentication flow tests

### Performance Tests

-   Response time tests
-   Load testing with Locust
-   Concurrent user simulation

## Test Reports and Artifacts

### Test Report

![Test Report 1](docs/test-report1.png)
![Test Report 2](docs/test-report2.png)


### GitHub Actions Artifacts

![GitHub Actions Artifacts](docs/artifacts.png)

The GitHub Actions workflow generates and stores:

-   Test execution reports
-   Allure test results
-   Application logs
-   Server logs

## CI/CD Pipeline

The GitHub Actions workflow includes:

1. Code checkout
2. Python environment setup
3. PostgreSQL service container
4. Dependency installation
5. Server startup
6. Test execution
7. Report generation
8. Artifact upload

## Logging

The application uses structured logging with:

-   Rotating file handlers
-   Environment-based log levels
-   JSON formatting in production
-   Console output in development

## Security Features

-   JWT token authentication
-   Password hashing with bcrypt
-   Input validation with Pydantic
-   Environment variable configuration
-   Secure password storage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
