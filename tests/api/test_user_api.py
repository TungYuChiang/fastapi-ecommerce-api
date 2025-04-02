"""
Tests for user API endpoints
"""
import pytest
import uuid
from httpx import AsyncClient

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.api
@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, user_data):
    """
    Test user registration
    """
    # Ensure each test uses a unique username
    
    user_data = {
        "username": f"testuser_{uuid.uuid4().hex[:8]}",
        "password": "TestPassword123"
    }
    
    response = await client.post("/users/register", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["username"] == user_data["username"]
    assert "password" not in created_user
    return created_user

@pytest.mark.api
@pytest.mark.asyncio
async def test_user_login(client: AsyncClient):
    """
    Test user login
    """
    # First register a user
    user_data = {
        "username": f"login_user_{uuid.uuid4().hex[:8]}",
        "password": "TestPassword123",
    }
    await client.post("/users/register", json=user_data)
    
    response = await client.post("/users/login", json= user_data)
    assert response.status_code == 200
    login_result = response.json()
    assert "access_token" in login_result
    assert login_result["token_type"] == "bearer"


@pytest.mark.api
@pytest.mark.asyncio
async def test_invalid_login(client: AsyncClient):
    """
    Test login with invalid credentials
    """
    login_data = {
        "username": f"nonexistent_user_{uuid.uuid4().hex[:8]}",
        "password": "WrongPassword123"
    }
    response = await client.post("/users/login", json=login_data)
    assert response.status_code == 401
    error_data = response.json()
    assert error_data["success"] is False
    assert error_data["error"]["code"] == "ERR_401"