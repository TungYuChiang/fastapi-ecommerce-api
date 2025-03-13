#!/usr/bin/env python
"""
數據庫表格創建腳本
"""
import logging
import sys
import os

# 將項目根目錄添加到 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import engine
from app.models.base import Base

# 確保所有模型都被導入，以便 Base.metadata 能夠收集所有表格定義
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables():
    try:
        # 由於現在所有模型都使用同一個 Base，我們可以一次性創建所有表格
        logger.info("正在創建所有資料庫表格...")
        Base.metadata.create_all(bind=engine)
        logger.info("所有表格創建成功!")
    except Exception as e:
        logger.error(f"創建表格時發生錯誤: {str(e)}")
        raise


if __name__ == "__main__":
    create_tables()

# 要創建表格，運行:
# python scripts/create_tables.py