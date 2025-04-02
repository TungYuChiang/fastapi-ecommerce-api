#!/bin/bash

# Define variables
FIX_MODE=false

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -f|--fix) FIX_MODE=true ;;
        -h|--help)
            echo "Usage: ./run_tests.sh [options]"
            echo "Options:"
            echo "  -f, --fix    Auto-fix linting issues when possible"
            echo "  -h, --help   Show this help message"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Run tests in existing Docker environment
echo "Starting E-commerce API tests in existing Docker environment..."
if [ "$FIX_MODE" = true ]; then
    echo "Auto-fix mode enabled: will attempt to fix linting issues"
fi

# Make sure containers are running
if ! docker ps | grep -q "ecommerce-api"; then
    echo "❌ API container is not running. Please start Docker environment first with: docker-compose up -d"
    exit 1
fi

# Run Markdown linting in the container
echo "Running Markdown linting..."
if [ "$FIX_MODE" = true ]; then
    # Run with auto-fix
    docker exec ecommerce-api bash -c '
        # Check if markdownlint is installed
        if command -v markdownlint &> /dev/null; then
            echo "Checking and fixing Markdown files..."
            markdownlint --fix "**/*.md" --ignore node_modules || {
                echo "❌ Markdown linting failed (some issues may require manual fixes)"
                exit 1
            }
            echo "✅ Markdown linting and fixing passed"
        else
            echo "⚠️ markdownlint not installed, skipping Markdown checks"
            echo "To install, run in container: npm install -g markdownlint-cli"
        fi
    '
else
    # Run without auto-fix (normal lint check)
    docker exec ecommerce-api bash -c '
        # Check if markdownlint is installed
        if command -v markdownlint &> /dev/null; then
            echo "Checking Markdown files..."
            markdownlint "**/*.md" --ignore node_modules || {
                echo "❌ Markdown linting failed"
                echo "Run with --fix option to attempt automatic fixes"
                exit 1
            }
            echo "✅ Markdown linting passed"
        else
            echo "⚠️ markdownlint not installed, skipping Markdown checks"
            echo "To install, run in container: npm install -g markdownlint-cli"
        fi
    '
fi

# Store the markdown lint exit code
MARKDOWN_EXIT_CODE=$?

# If markdown linting failed, exit early
if [ $MARKDOWN_EXIT_CODE -ne 0 ]; then
    echo "❌ Markdown linting failed, tests aborted"
    exit $MARKDOWN_EXIT_CODE
fi

# Run Python code linting with Ruff in the container
echo "Running Python code linting..."
if [ "$FIX_MODE" = true ]; then
    # Run with auto-fix
    docker exec ecommerce-api bash -c '
        # Check if ruff is installed
        if command -v ruff &> /dev/null; then
            echo "Checking and fixing Python code..."
            ruff check --fix . || {
                echo "❌ Python code linting failed (some issues may require manual fixes)"
                exit 1
            }
            echo "✅ Python code linting and fixing passed"
        else
            echo "⚠️ Ruff not installed, skipping Python code linting"
            echo "To install, run in container: pip install ruff"
        fi
    '
else
    # Run without auto-fix (normal lint check)
    docker exec ecommerce-api bash -c '
        # Check if ruff is installed
        if command -v ruff &> /dev/null; then
            echo "Checking Python code..."
            ruff check . || {
                echo "❌ Python code linting failed"
                echo "Run with --fix option to attempt automatic fixes"
                exit 1
            }
            echo "✅ Python code linting passed"
        else
            echo "⚠️ Ruff not installed, skipping Python code linting"
            echo "To install, run in container: pip install ruff"
        fi
    '
fi

# Store the ruff lint exit code
RUFF_EXIT_CODE=$?

# If ruff linting failed, exit early
if [ $RUFF_EXIT_CODE -ne 0 ]; then
    echo "❌ Python code linting failed, tests aborted"
    exit $RUFF_EXIT_CODE
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