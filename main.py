from fastapi import FastAPI
from app.routers import product

app = FastAPI()

app.include_router(product.router) 

@app.get("/")
async def read_root():
    return {"Hello": "World"}
