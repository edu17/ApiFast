from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import movieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200,
                  dependencies=[Depends(JWTBearer())])
def getMovies() -> JSONResponse:
    db = Session()
    result = movieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def getMoviesId(id: int = Path(ge=1, le=2000)) -> JSONResponse:
    db = Session()
    result = movieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def getMoviesCategory(category: str = Query(min_length=5, max_length=15)) -> JSONResponse:
    db = Session()
    result = movieService(db).get_movie_categories(category)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def createMovie(movie: Movie) -> JSONResponse:
    db = Session()
    movieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def updateMovie(id: int, movie: Movie) -> JSONResponse:
    db = Session()
    result = movieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    movieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})


@movie_router.delete('/movies', tags=['movies'], response_model=dict, status_code=200)
def deleteMovie(id: int) -> JSONResponse:
    db = Session()
    result = movieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    movieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})
