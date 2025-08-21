from typing import List, Optional
from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    name: str
    director: str
    genres: List[str]
    shop: int
    rent: Optional[bool] = False
    
class MovieRequestCreate(BaseModel):
    name: str
    director: str
    genres: List[str]
    shop: int
    rent: Optional[bool] = False

class MovieRequestUpdate(BaseModel):
    name: str
    director: str
    genres: List[str]
    rent: Optional[bool] = False

class MovieShopRequestUpdate(BaseModel):
    shop: int

class Shop(BaseModel):
    id: int
    address: str
    manager: str
    movies: List[Movie] = []
    
class ShopRequestCreate(BaseModel):
    address: str
    manager: str

class ShopRequestUpdate(BaseModel):
    address: str
    manager: str
