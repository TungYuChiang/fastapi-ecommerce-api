# E-Commerce Platform API

[![CI](https://github.com/TungYuChiang/ecommerce/actions/workflows/ci.yml/badge.svg)](https://github.com/TungYuChiang/ecommerce/actions/workflows/ci.yml)
[![Security Scan](https://github.com/TungYuChiang/ecommerce/actions/workflows/security.yml/badge.svg)](https://github.com/TungYuChiang/ecommerce/actions/workflows/security.yml)
[![Documentation Checks](https://github.com/TungYuChiang/ecommerce/actions/workflows/docs.yml/badge.svg)](https://github.com/TungYuChiang/ecommerce/actions/workflows/docs.yml)

This is an E-Commerce Platform API developed with FastAPI, providing product management, user management, order processing, and payment functionality.

## System Architecture

- **Web API**: FastAPI providing RESTful API
- **Database**: PostgreSQL for application data storage
- **Message Queue**: RabbitMQ for order event processing
- **Task Processing**: Celery + Redis for asynchronous tasks
- **Testing Framework**: Pytest for API test coverage
- **Error Handling**: Unified error handling mechanism

## Technology Stack

- **FastAPI**: High-performance API framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and serialization
- **Celery**: Distributed task queue
- **Redis**: Caching and Celery backend
- **RabbitMQ**: Message queue
- **Pytest**: Testing framework
- **Docker & Docker Compose**: Containerized deploymen

## Running with Docker (Recommended)

### Prerequisites

- Docker
- Docker Compose

### Start All Services

```bash
docker-compose up -d
```

This will start the following services:

- PostgreSQL database
- Redis server
- RabbitMQ message queue
- FastAPI application
- Celery Worker
- RabbitMQ consumer

### View Logs

```bash
# View logs for all services
docker-compose logs -f

# View logs for specific services
docker-compose logs -f api
docker-compose logs -f celery_worker
docker-compose logs -f rabbitmq_consumer
```

### Stop Services

```bash
docker-compose down
```

### Rebuild Services

If you've modified code or configuration and need to rebuild services:

```bash
docker-compose build
docker-compose up -d
```

## Testing

### Run Tests in Docker Environment

Ensure Docker containers are running, then execute:

```bash
./scripts/run_tests.sh
```

The test script supports the following options:

```bash
# Run tests with automatic linting fixes
./scripts/run_tests.sh --fix

# Show available options
./scripts/run_tests.sh --help
```

Available options:

- `-f, --fix`: Automatically fix linting issues when possible
- `-h, --help`: Show the help message with available options

The testing process includes:

1. Markdown linting (with automatic fixes if `--fix` option is used)
2. Python code linting using Ruff (with automatic fixes if `--fix` option is used)
3. Running unit tests and generating coverage reports

### Run Tests Locally

```bash
# Run all tests
pytes

# Run specific test file
pytest tests/api/test_product_api.py

# Run specific type of tests
pytest -m api

# Generate test coverage repor
pytest --cov=app
```

For detailed testing instructions, refer to the [Testing Documentation](tests/README.md).

## Error Handling Mechanism

This project implements a unified error handling mechanism, processing various API error scenarios through custom exception classes. All error responses follow a standard format:

```json
{
  "success": false,
  "error": {
    "code": "ERR_XXX",
    "message": "Error message",
    "detail": "Detailed information"
  }
}
```

Main error types:

- `NotFoundError` (404): Requested resource not found
- `ValidationError` (422): Request data validation failed
- `AuthenticationError` (401): Not authenticated or authentication failed
- `AuthorizationError` (403): Authentication successful but no access permission
- `ConflictError` (409): Resource conflic
- `ServerError` (500): Server internal error

## API Endpoints

### Product Managemen

- `GET /products`: Get all products
- `GET /products/{product_id}`: Get specific produc
- `POST /products`: Create new produc
- `PUT /products/{product_id}`: Update produc
- `DELETE /products/{product_id}`: Delete produc

### User Managemen

- `POST /users`: Create user
- `GET /users/{user_id}`: Get user profile

### Order Managemen

- `POST /orders`: Create order
- `GET /orders/{order_id}`: Get specific order
- `GET /orders`: Get all orders

### Payment Processing

- `POST /payments/process`: Process paymen
- `GET /payments/status/{order_id}`: Check payment status

## Order Processing Flow

1. Customer creates order (`POST /orders`)
2. System publishes order creation event to RabbitMQ
3. Customer submits payment (`POST /payments/process`)
4. System processes payment and publishes payment processing event to RabbitMQ
5. Celery Worker verifies payment status
6. Customer can query order status (`GET /orders/{order_id}`)

## Project Structure

```plaintex
ecommerce/
├── app/
│   ├── config/          # Configuration module
│   ├── models/          # Database models
│   ├── routers/         # API routes
│   ├── schemas/         # Pydantic models
│   ├── services/        # Business logic
│   ├── tasks/           # Celery tasks
│   ├── messaging/       # Message handling
│   ├── __init__.py      # Application package initialization
│   ├── celery_app.py    # Celery configuration
│   ├── errors.py        # Error handling mechanism
│   └── database.py      # Database connection
├── scripts/             # Scripts and tools
│   ├── worker.py        # Celery Worker startup
│   └── run_tests.sh     # Test execution scrip
├── tests/               # Test directory
│   ├── api/             # API tests
│   ├── conftest.py      # Test fixtures
│   └── README.md        # Testing documentation
├── api.py               # API service entry poin
├── run.py               # Unified command line interface
├── requirements.txt     # Dependency managemen
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
└── .env                 # Environment variables
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and code quality control:

- **CI Workflow**: Runs linting, tests, and builds the Docker image
- **Security Scan**: Checks dependencies for vulnerabilities and scans code for security issues
- **Documentation Checks**: Verifies the quality of documentation files

### CI/CD Process

1. **Code Quality**: All pull requests are automatically checked for code style with Ruff
2. **Testing**: Automated tests are run against a temporary test environmen
3. **Security**: Dependencies are scanned for known vulnerabilities
4. **Docker Build**: Tests that the Docker image builds successfully

To view the CI/CD workflows, check the `.github/workflows` directory.
