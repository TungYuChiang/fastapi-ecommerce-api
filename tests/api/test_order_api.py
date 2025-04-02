"""
Tests for order API endpoints
"""
import pytest
import uuid
from httpx import AsyncClient
from tests.utils import get_auth_headers


@pytest.mark.api
@pytest.mark.asyncio
async def test_create_order(client: AsyncClient, order_data, product_data, user_data):
    """
    Test creating a new order
    """
    # First register test user
    user_response = await client.post("/users/register", json=user_data)
    assert user_response.status_code == 200
    
    # Create products for order testing
    headers = await get_auth_headers(client)
    product1 = dict(product_data)
    product1["name"] = f"Test Product 1 {uuid.uuid4().hex[:8]}"
    product1_response = await client.post("/products/", json=product1, headers=headers)
    assert product1_response.status_code == 201
    product1_data = product1_response.json()
    
    product2 = dict(product_data)
    product2["name"] = f"Test Product 2 {uuid.uuid4().hex[:8]}"
    product2_response = await client.post("/products/", json=product2, headers=headers)
    assert product2_response.status_code == 201
    product2_data = product2_response.json()
    
    # Update order data with actual created product IDs
    test_order_data = dict(order_data)
    test_order_data["items"] = [
        {"product_id": product1_data["id"], "quantity": 2},
        {"product_id": product2_data["id"], "quantity": 1}
    ]
    
    response = await client.post("/orders/", json=test_order_data)
    assert response.status_code == 201
    created_order = response.json()
    assert "id" in created_order
    assert "order_number" in created_order
    assert created_order["payment_method"] == test_order_data["payment_method"]
    assert len(created_order["items"]) == len(test_order_data["items"])
    return created_order


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_order_by_id(client: AsyncClient, order_data, product_data, user_data):
    """
    Test getting an order by ID
    """
    # First register test user
    user_response = await client.post("/users/register", json=user_data)
    assert user_response.status_code == 200
    
    # Create products for order testing
    headers = await get_auth_headers(client)
    product1 = dict(product_data)
    product1["name"] = f"Test Product 1 {uuid.uuid4().hex[:8]}"
    product1_response = await client.post("/products/", json=product1, headers=headers)
    assert product1_response.status_code == 201
    product1_data = product1_response.json()
    
    product2 = dict(product_data)
    product2["name"] = f"Test Product 2 {uuid.uuid4().hex[:8]}"
    product2_response = await client.post("/products/", json=product2, headers=headers)
    assert product2_response.status_code == 201
    product2_data = product2_response.json()
    
    # Update order data with actual created product IDs
    test_order_data = dict(order_data)
    test_order_data["items"] = [
        {"product_id": product1_data["id"], "quantity": 2},
        {"product_id": product2_data["id"], "quantity": 1}
    ]
    
    # First create an order
    create_response = await client.post("/orders/", json=test_order_data)
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