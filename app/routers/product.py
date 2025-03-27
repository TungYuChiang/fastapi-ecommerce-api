from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductSchema
from app.database import get_db
from app.services.product import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
)
from app.services.user import get_current_user
from app.models.user import User
from app.errors import NotFoundError

router = APIRouter()


@router.post("/products/", response_model=ProductSchema, status_code=201)
async def create_product_endpoint(
    product: ProductSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_product(db, product)


@router.get("/products/", response_model=List[ProductSchema])
async def read_products_endpoint(db: Session = Depends(get_db)):
    return get_products(db)


@router.get("/products/{product_id}", response_model=ProductSchema)
async def read_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if product is None:
        raise NotFoundError(message="Product not found")
    return product


@router.put("/products/{product_id}", response_model=ProductSchema)
async def update_product_endpoint(
    product_id: int,
    product: ProductSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_product = update_product(db, product_id, product)
    if updated_product is None:
        raise NotFoundError(message="Product not found")
    return updated_product


@router.delete("/products/{product_id}", status_code=204)
async def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = delete_product(db, product_id)
    if not success:
        raise NotFoundError(message="Product not found")
    return {"detail": "Product deleted"}
