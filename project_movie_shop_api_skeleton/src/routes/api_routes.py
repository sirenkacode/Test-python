from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Dict, Optional

from src.constants import MOVIE_NOT_FOUND_MESSAGE, SHOP_NOT_FOUND_MESSAGE, SHOP_INVALID_MESSAGE
from src.schemas.schemas import Movie, MovieRequestCreate, MovieRequestUpdate, MovieShopRequestUpdate, Shop, ShopRequestCreate, ShopRequestUpdate

# In-memory "DB"
movies: Dict[int, Movie] = {}
shops: Dict[int, Shop] = {}
_next_movie_id = 1
_next_shop_id = 1

router = APIRouter()

# Movies
@router.get("/movies", response_model=List[Movie])
def read_all_movies():
  return list(movies.values())

@router.get("/movies/{movie_id}", response_model=Movie)
def read_movie_by_id(movie_id : int):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  return movies[movie_id]

@router.post("/movies", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie : MovieRequestCreate):
  global _next_movie_id

  try:
    shop_id = int(movie.shop)
  except ValueError:
    raise HTTPException(status_code=422, detail=[SHOP_INVALID_MESSAGE])

  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])

  new_movie = Movie(id=_next_movie_id, **movie.model_dump())
  movies[_next_movie_id] = new_movie
  shops[shop_id].movies.append(new_movie)
  _next_movie_id += 1
  return new_movie

@router.put("/movies/{movie_id}", response_model=Movie)
def update_movie(movie_id : int, new_movie : MovieRequestUpdate):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  movies[movie_id].name = new_movie.name
  movies[movie_id].director = new_movie.director
  movies[movie_id].gender = new_movie.gender
  return movies[movie_id]

@router.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id : int):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  _ = movies.pop(movie_id)

# Shops
@router.get("/shops", response_model=List[Shop])
def read_all_shops():
  return list(shops.values())

@router.get("/shops/{shop_id}", response_model=Shop)
def read_shop_by_id(shop_id : int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  return shops[shop_id]

@router.post("/shops", response_model=Shop, status_code=status.HTTP_201_CREATED)
def create_shop(shop : ShopRequestCreate):
  global _next_shop_id
  new_shop = Shop(id=_next_shop_id, **shop.model_dump())
  shops[_next_shop_id] = new_shop
  _next_shop_id += 1
  return new_shop

@router.put("/shops/{shop_id}", response_model=Shop)
def update_shop(shop_id : int, new_shop : ShopRequestUpdate):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
  shops[shop_id].address = new_shop.address
  shops[shop_id].manager = new_shop.manager
  return shops[shop_id]

@router.delete("/shops/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(shop_id : int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
  _ = shops.pop(shop_id)

# Extra
@router.get("/shops/{shop_id}/movies", response_model=List[Movie])
def get_all_movies_by_shop(shop_id: int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
  return shops[shop_id].movies

@router.get("/shops/{shop_id}/movies/available", response_model=List[Movie])
def get_all_availables_movies_by_shop(shop_id: int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
  all_movies = shops[shop_id].movies
  available_movies = [movie for movie in all_movies if not movie.rent]
  return available_movies

@router.patch("/movies/{movie_id}/move", response_model=Movie)
def change_movie_shop(movie_id : int, new_movie_shop : MovieShopRequestUpdate):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  movies[movie_id].shop = str(new_movie_shop.shop)
  return movies[movie_id]

@router.get("/search/movies", response_model=List[Movie])
def get_movies_by_values(
    name: Optional[str] = None,
    director: Optional[str] = None,
    gender: Optional[List[str]] = Query(None)
):
    results = list(movies.values())

    if name:
        results = [m for m in results if name.lower() in m.name.lower()]

    if director:
        results = [m for m in results if director.lower() in m.director.lower()]

    if gender:
        results = [m for m in results if all(g in m.gender for g in gender if g != "")]

    return results