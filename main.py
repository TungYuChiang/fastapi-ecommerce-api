#!/usr/bin/env python
"""
E-Commerce Platform API Service Entry Point
"""
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.routers import product
from app.routers import user
from app.routers import order
from app.routers import payment
from app.errors import (
    BaseAPIError, 
    api_exception_handler, 
    http_exception_handler, 
    validation_exception_handler,
    default_exception_handler
)

# Import required models and engine
from app.models.base import Base
from app.database import engine

# Ensure all models are imported so Base.metadata can collect all table definitions
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem

# Create FastAPI application instance
app = FastAPI(
    title="E-Commerce Platform API",
    description="API providing product management, user management, order processing and payment features",
    version="1.0.0",
)

# Register error handlers
app.add_exception_handler(BaseAPIError, api_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, default_exception_handler)

# Create all tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(product.router, tags=["Products"])
app.include_router(user.router, tags=["Users"])
app.include_router(order.router, tags=["Orders"])
app.include_router(payment.router, tags=["Payments"])


@app.get("/", tags=["Root"])
async def read_root():
    """
    API root path, returns welcome message
    """
    return {"message": "Welcome to the E-Commerce Platform API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    from app.config.settings import APP_HOST, APP_PORT

    # Start API server
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)

# To start the API server, run:
# python api.py
# or use uvicorn:
# uvicorn api:app --reload