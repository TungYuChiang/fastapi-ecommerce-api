#!/usr/bin/env python
"""
Database Table Creation Script
"""
import logging
import sys
import os

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import engine
from app.models.base import Base

# Ensure all models are imported so Base.metadata can collect all table definitions
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables():
    try:
        # Since all models now use the same Base, we can create all tables at once
        logger.info("Creating all database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        raise


if __name__ == "__main__":
    create_tables()

# To create tables, run:
# python scripts/create_tables.py