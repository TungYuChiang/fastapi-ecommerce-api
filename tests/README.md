# API Testing Framework

This directory contains the testing framework and test cases for the E-Commerce Platform API. Tests use the `pytest` framework and integrate FastAPI testing tools to provide comprehensive API test coverage.

## Test Architecture

The test architecture is organized as follows:

```plaintex
tests/
├── __init__.py           # Test package definition
├── conftest.py           # Test fixtures
├── api/                  # API test directory
│   ├── __init__.py
│   ├── test_product_api.py  # Product API tests
│   ├── test_user_api.py     # User API tests
│   ├── test_order_api.py    # Order API tests
│   └── test_main.py         # Main application tests
└── README.md             # This documen
```

## Test Markers

We use the following pytest markers to organize tests:

- `api`: API endpoint tests
- `unit`: Unit tests
- `integration`: Integration tests
- `slow`: Tests that take longer to execute
- `e2e`: End-to-end tests

## Test Fixtures

The following common test fixtures are defined in `conftest.py`:

- `client`: Asynchronous HTTP client for testing API endpoints
- `db_session`: Test database session
- `product_data`: Test product data
- `user_data`: Test user data
- `order_data`: Test order data
- `payment_data`: Test payment data

## Running Tests

### Running Tests in Docker

Use the following command to run tests in an existing Docker environment:

```bash
./scripts/run_tests.sh
```

The test script includes:

- Markdown linting to ensure documentation quality
- Python code linting using Ruff to enforce code style
- Unit tests execution with coverage reporting

The script supports command-line options for more flexibility:

```bash
# Run tests with automatic linting fixes
./scripts/run_tests.sh --fix

# Display help information
./scripts/run_tests.sh --help
```

Options:

- `-f, --fix`: Automatically fix linting issues in both Markdown and Python code
- `-h, --help`: Show help message with available options

This will run all tests in the `ecommerce-api` container and display detailed test results and coverage reports.

## Error Handling Mechanism

Test cases utilize our unified error handling mechanism to ensure the API returns standardized error responses. All API errors inherit from the `BaseAPIError` class and return a unified format:

```json
{
  "success": false,
  "error": {
    "code": "ERR_XXX",
    "message": "Error message",
    "detail": "Optional detailed information"
  }
}
```

Test cases verify that the API returns the correct status codes and error formats in various error scenarios.

## Common Error Type Tests

The test suite includes validation for the following common error types:

- `NotFoundError` (404): Resource not found
- `ValidationError` (422): Input validation error
- `AuthenticationError` (401): Not authenticated
- `AuthorizationError` (403): Not authorized
- `ConflictError` (409): Resource conflic
- `ServerError` (500): Server internal error

## Adding Tests

When adding new tests, follow these steps:

1. Create a test file in the appropriate test directory (e.g., `tests/api/test_new_feature.py`)
2. Use `@pytest.mark.api` or other appropriate markers for each test case
3. Decorate all asynchronous test functions with `@pytest.mark.asyncio`
4. Use fixtures to provide test data and clients
5. Assert that the API response meets expectations

## Best Practices

- Each test case should be independent, not relying on the state of other tests
- Use mocks for isolation of external dependencies
- Test cases should cover normal scenarios and error scenarios
- Maintain high test coverage, especially for core business logic
- Run the test suite regularly to ensure system stability

## Using Docker Commands to Run Tests

In addition to using the `run_tests.sh` script, you can also use Docker commands directly to run tests. Below are detailed instructions for running tests using Docker:

### Start Services Using docker-compose

First, make sure your development environment is running:

```bash
# Start all services
docker-compose up -d
```

### Run Tests Using docker exec

#### Run All Tests

```bash
# Run all tests
docker exec ecommerce-api pytes

# Run all tests with verbose outpu
docker exec ecommerce-api pytest -v

# Run all tests and generate a coverage repor
docker exec ecommerce-api pytest --cov=app
```

#### Run Tests for Specific Directories or Files

```bash
# Run all API tests
docker exec ecommerce-api pytest tests/api/ -v

# Run a specific test file
docker exec ecommerce-api pytest tests/api/test_product_api.py -v

# Run multiple test files
docker exec ecommerce-api pytest tests/api/test_main.py tests/api/test_product_api.py -v
```

#### Run Tests with Specific Markers

```bash
# Run all tests marked as 'api'
docker exec ecommerce-api pytest -m api -v

# Run all non-slow tests (excluding tests marked as 'slow')
docker exec ecommerce-api pytest -m "not slow" -v
```

### File Synchronization and Test Updates

If you update test files locally, you can use the `docker cp` command to copy the updated files to the container:

```bash
# Copy a single test file to the container
docker cp tests/api/test_product_api.py ecommerce-api:/app/tests/api/

# Copy test utility functions
docker cp tests/utils.py ecommerce-api:/app/tests/

# Copy the entire test directory
docker cp tests/ ecommerce-api:/app/
```

Note: If you have correctly set up volume mounts in your `docker-compose.yml`, you usually don't need to manually copy files, as local file changes will automatically sync to the container. However, if you encounter synchronization issues, you can use the above commands for manual synchronization.

### Handling Test Databases

If tests require a clean database environment:

```bash
# Recreate database tables (use with caution, will clear existing data)
docker exec ecommerce-api python scripts/create_tables.py
```

### View Test Logs

```bash
# View container logs to check test outpu
docker logs ecommerce-api

# View logs in real-time
docker logs -f ecommerce-api
```

### Troubleshooting Common Issues

1. **Authentication Issues**: If you encounter authentication errors in tests, you may need to ensure the JWT key is set correctly.

2. **Port Conflicts**: If you get errors about ports being in use, you can modify the port settings in the `.env` file.

3. **Path Issues**: API tests may fail due to different path configurations, make sure to use the correct path format (some endpoints may require trailing slashes).

4. **Data Synchronization**: If volume mounts aren't working properly, use the `docker cp` command to manually synchronize files.

Implementing these testing strategies ensures your API can be reliably and consistently tested in Docker containers.
