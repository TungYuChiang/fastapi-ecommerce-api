from fastapi import FastAPI
from app.routers import product
from app.routers import user
from app.routers import order
from app.routers import payment

# 導入所需模型和引擎
from app.models.base import Base
from app.database import engine

# 確保所有模型都被導入，以便 Base.metadata 能夠收集所有表格定義
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem

app = FastAPI()

# 創建所有表格
Base.metadata.create_all(bind=engine)

app.include_router(product.router)
app.include_router(user.router)
app.include_router(order.router)
app.include_router(payment.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
