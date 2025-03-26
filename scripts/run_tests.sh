#!/bin/bash

# Run tests in existing Docker environment
echo "Starting E-commerce API tests in existing Docker environment..."

# Make sure containers are running
if ! docker ps | grep -q "ecommerce-api"; then
    echo "❌ API container is not running. Please start Docker environment first with: docker-compose up -d"
    exit 1
fi

# Run tests in the existing API container
echo "Running tests in API container..."
docker exec ecommerce-api pytest -v -s --cov=app --cov-report=term tests/

# Check if tests passed
TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed successfully!"
else
    echo "❌ Tests failed with exit code $TEST_EXIT_CODE"
fi

exit $TEST_EXIT_CODE 