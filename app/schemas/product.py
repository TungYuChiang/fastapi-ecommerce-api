from pydantic import BaseModel
from typing import Optional


class ProductSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
