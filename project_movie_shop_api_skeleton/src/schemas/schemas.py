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

class MovieRequestUpdate(BaseModel):
    name: str
    director: str
    gender: list[str]

class MovieShopRequestUpdate(BaseModel):
    shop: int

class Shop(BaseModel):
    id: int
    address: str
    manager: str
    movies: list[Movie] = []
    
class ShopRequestCreate(BaseModel):
    address: str
    manager: str

class ShopRequestUpdate(BaseModel):
    address: str
    manager: str
