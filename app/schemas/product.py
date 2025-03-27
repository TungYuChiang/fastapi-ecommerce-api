from pydantic import BaseModel
from typing import Optional


class ProductSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
