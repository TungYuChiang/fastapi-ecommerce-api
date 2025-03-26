"""
Pytest configuration file containing test fixtures
"""
import asyncio
import os
import pytest
from typing import AsyncGenerator, Generator
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from main import app as main_app
from app.database import get_db

# Test database URL (using SQLite in memory for tests)
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Create an instance of the default event loop for each test case.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_engine():
    """
    Create a test database engine.
    """
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_engine):
    """
    Create a fresh database session for a test.
    """
    Session = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="module")
def app() -> FastAPI:
    """
    Create a FastAPI app instance for testing.
    """
    return main_app


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    """
    Create an async client for testing API endpoints.
    Returns an AsyncClient instance rather than an async generator.
    """
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac


@pytest.fixture
def product_data():
    """
    Sample product data for tests.
    """
    return {
        "name": "Test Product",
        "description": "A product for testing",
        "price": 99.99,
        "stock": 100,
        "category": "Test Category"
    }


@pytest.fixture
def user_data():
    """
    Sample user data for tests.
    """
    return {
        "username": "testuser",
        "password": "TestPassword123",
    }


@pytest.fixture
def order_data():
    """
    Sample order data for tests.
    """
    return {
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 1},
        ],
        "payment_method": "credit_card"
    }


@pytest.fixture
def payment_data():
    """
    Sample payment data for tests.
    """
    return {
        "order_id": 1,
        "payment_method": "credit_card",
        "amount": 199.99
    } 