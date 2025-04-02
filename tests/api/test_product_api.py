"""
Tests for product API endpoints
"""
import pytest
from httpx import AsyncClient
from app.errors import NotFoundError
from main import app
from tests.utils import get_auth_headers


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_all_products(client: AsyncClient):
    """
    Test getting all products
    """
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get("/products/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.api
@pytest.mark.asyncio
async def test_create_product(client: AsyncClient, product_data):
    """
    Test creating a new product
    """
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Get auth headers
        headers = await get_auth_headers(client)
        
        # Create product with auth
        response = await client.post("/products/", json=product_data, headers=headers)
        assert response.status_code == 201
        created_product = response.json()
        assert created_product["name"] == product_data["name"]
        assert created_product["price"] == product_data["price"]
        assert "id" in created_product
        return created_product


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient, product_data):
    """
    Test getting a product by ID
    """
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Get auth headers
        headers = await get_auth_headers(client)
        
        create_response = await client.post("/products/", json=product_data, headers=headers)
        created_product = create_response.json()
        
        # Now get the product by ID
        product_id = created_product["id"]
        response = await client.get(f"/products/{product_id}")
        assert response.status_code == 200
        fetched_product = response.json()
        assert fetched_product["id"] == product_id
        assert fetched_product["name"] == product_data["name"]


@pytest.mark.api
@pytest.mark.asyncio
async def test_update_product(client: AsyncClient, product_data):
    """
    Test updating a product
    """
    # Get auth headers
    headers = await get_auth_headers(client)
    
    # First create a product
    create_response = await client.post("/products/", json=product_data, headers=headers)
    assert create_response.status_code == 201
    created_product = create_response.json()
    product_id = created_product["id"]
    
    # Update the product - use PUT instead of PATCH to match route definition
    update_data = {
        "name": "Updated Product Name",
        "price": 89.99,
        "description": product_data["description"]  # Must include all required fields
    }
    response = await client.put(f"/products/{product_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["id"] == product_id
    assert updated_product["name"] == update_data["name"]
    assert updated_product["price"] == update_data["price"]
    assert updated_product["description"] == product_data["description"]


@pytest.mark.api
@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient):
    """
    Test deleting a product
    """
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Get auth headers
        headers = await get_auth_headers(client)
        
        # First create a product
        product_data = {
            "name": "Test Delete Product",
            "description": "A product for testing delete endpoint",
            "price": 29.99
        }
        create_response = await client.post("/products/", json=product_data, headers=headers)
        created_product = create_response.json()
        product_id = created_product["id"]
        
        # Delete the product
        response = await client.delete(f"/products/{product_id}", headers=headers)
        assert response.status_code == 204
        
        # Verify the product is deleted
        get_response = await client.get(f"/products/{product_id}")
        assert get_response.status_code == 404


@pytest.mark.api
@pytest.mark.asyncio
async def test_product_not_found(client: AsyncClient):
    """
    Test getting a non-existent product returns 404
    """
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get("/products/9999")  # Assuming ID 9999 doesn't exist
        assert response.status_code == 404
        error_data = response.json()
        assert error_data["success"] is False
        assert error_data["error"]["code"] == "ERR_NOT_FOUND"
        assert error_data["error"]["message"] == "Product not found" 