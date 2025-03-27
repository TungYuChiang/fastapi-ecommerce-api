"""
Tests for order API endpoints
"""
import pytest
from httpx import AsyncClient
from app.errors import NotFoundError, ValidationError


@pytest.mark.api
@pytest.mark.asyncio
async def test_create_order(client: AsyncClient, order_data):
    """
    Test creating a new order
    """
    response = await client.post("/orders/", json=order_data)
    assert response.status_code == 201
    created_order = response.json()
    assert "id" in created_order
    assert "order_number" in created_order
    assert created_order["payment_method"] == order_data["payment_method"]
    assert len(created_order["items"]) == len(order_data["items"])
    return created_order


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_order_by_id(client: AsyncClient, order_data):
    """
    Test getting an order by ID
    """
    # First create an order
    create_response = await client.post("/orders/", json=order_data)
    created_order = create_response.json()
    
    # Now get the order by ID
    order_id = created_order["id"]
    response = await client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    fetched_order = response.json()
    assert fetched_order["id"] == order_id
    assert fetched_order["order_number"] == created_order["order_number"]


@pytest.mark.api
@pytest.mark.asyncio
async def test_order_not_found(client: AsyncClient):
    """
    Test getting a non-existent order returns 404
    """
    response = await client.get("/orders/9999")  # Assuming ID 9999 doesn't exist
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["success"] is False
    assert error_data["error"]["code"] == "ERR_NOT_FOUND"


@pytest.mark.api
@pytest.mark.asyncio
async def test_invalid_order_data(client: AsyncClient):
    """
    Test creating an order with invalid data returns 422
    """
    # Missing required fields
    invalid_order = {
        "payment_method": "credit_card"
        # Missing items
    }
    
    response = await client.post("/orders/", json=invalid_order)
    assert response.status_code == 422
    error_data = response.json()
    assert error_data["success"] is False
    assert error_data["error"]["code"] == "ERR_VALIDATION" 