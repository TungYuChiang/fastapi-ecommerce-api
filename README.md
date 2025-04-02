# E-Commerce Platform API

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
- **Docker & Docker Compose**: Containerized deployment

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

### Run Tests Locally

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/api/test_product_api.py

# Run specific type of tests
pytest -m api

# Generate test coverage report
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
- `ConflictError` (409): Resource conflict
- `ServerError` (500): Server internal error

## API Endpoints

### Product Management

- `GET /products`: Get all products
- `GET /products/{product_id}`: Get specific product
- `POST /products`: Create new product
- `PUT /products/{product_id}`: Update product
- `DELETE /products/{product_id}`: Delete product

### User Management

- `POST /users`: Create user
- `GET /users/{user_id}`: Get user profile

### Order Management

- `POST /orders`: Create order
- `GET /orders/{order_id}`: Get specific order
- `GET /orders`: Get all orders

### Payment Processing

- `POST /payments/process`: Process payment
- `GET /payments/status/{order_id}`: Check payment status

## Order Processing Flow

1. Customer creates order (`POST /orders`)
2. System publishes order creation event to RabbitMQ
3. Customer submits payment (`POST /payments/process`)
4. System processes payment and publishes payment processing event to RabbitMQ
5. Celery Worker verifies payment status
6. Customer can query order status (`GET /orders/{order_id}`)

## Project Structure

```
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
│   └── run_tests.sh     # Test execution script
├── tests/               # Test directory
│   ├── api/             # API tests
│   ├── conftest.py      # Test fixtures
│   └── README.md        # Testing documentation
├── api.py               # API service entry point
├── run.py               # Unified command line interface
├── requirements.txt     # Dependency management
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
└── .env                 # Environment variables
```