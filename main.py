#!/usr/bin/env python
"""
電子商務平台 API 服務入口點
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

# 導入所需模型和引擎
from app.models.base import Base
from app.database import engine

# 確保所有模型都被導入，以便 Base.metadata 能夠收集所有表格定義
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem

# 創建 FastAPI 應用程式實例
app = FastAPI(
    title="電子商務平台 API",
    description="提供商品管理、用戶管理、訂單處理和支付功能的 API",
    version="1.0.0",
)

# 註冊錯誤處理器
app.add_exception_handler(BaseAPIError, api_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, default_exception_handler)

# 創建所有表格
Base.metadata.create_all(bind=engine)

# 註冊路由
app.include_router(product.router, tags=["商品"])
app.include_router(user.router, tags=["用戶"])
app.include_router(order.router, tags=["訂單"])
app.include_router(payment.router, tags=["支付"])


@app.get("/", tags=["根"])
async def read_root():
    """
    API 根路徑，返回歡迎信息
    """
    return {"message": "歡迎使用電子商務平台 API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    from app.config.settings import APP_HOST, APP_PORT

    # 啟動 API 服務器
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)

# 要啟動 API 服務器，運行:
# python api.py
# 或者使用 uvicorn:
# uvicorn api:app --reload