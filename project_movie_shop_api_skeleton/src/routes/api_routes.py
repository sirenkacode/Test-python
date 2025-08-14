from fastapi import APIRouter, HTTPException, status
from typing import List, Dict

from src.constants import MOVIE_NOT_FOUND_MESSAGE, SHOP_NOT_FOUND_MESSAGE
from src.schemas.schemas import Movie, MovieRequestCreate, MovieRequestUpdate, Shop, ShopRequestCreate

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
  new_movie = Movie(id=_next_movie_id, **movie.model_dump())
  movies[_next_movie_id] = new_movie
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
