from typing import List, Optional
from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    name: str
    director: str
    gender: list[str]
    shop: str
    rent: bool = False
class MovieRequestCreate(BaseModel):
    name: str
    director: str
    gender: list[str]
    shop: str
    rent: bool
class MovieRequestUpdate(BaseModel):
    name: str
    director: str
    gender: list[str]


class Shop(BaseModel):
    id: int
class ShopRequestCreate(BaseModel):
    id: int
class ShopUpdate(BaseModel):
    id: int