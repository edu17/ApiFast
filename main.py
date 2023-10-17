from fastapi import FastAPI, Body, Path, Query, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse,JSONResponse
from pydantic import BaseModel,Field
from typing import Optional, List
from jwt_manager import create_token,validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title ="Api Tarjeton con FastAPI"
app.version="0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth= await super().__call__(request)
        data= validate_token(auth.credentials)
        if data['email']!="admin@gmail.com":
            raise HTTPException(status_code=403,detail="Credenciales son invalidas")

class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id:Optional[int]=None
    title:str = Field(min_length=5,max_length=15)
    overview:str = Field(min_length=15,max_length=50)
    year:int = Field(le=2022)
    rating:float = Field(ge=1,le=10)
    category:str = Field(min_length=3,max_length=10)

    class Config:
        json_schema_extra={
            "example":{
                "id":3,
                "title":"Mi pelicula",
                "overview":"Descripción de la película",
                "year":2022,
                "rating":0.8,
                "category":"Accion"
            }
        }


movies=[
    {
        "id":1,
        "title":"Avatar",
        "overview":"En un exuberante planeta llamado Pandora viven los na'vi, sers que ....",
        "year":"2009",
        "rating":7.8,
        "category":"Accion1"
    },
    {
        "id":2,
        "title":"Avatar",
        "overview":"En un exuberante planeta llamado Pandora viven los na'vi, sers que ....",
        "year":"2009",
        "rating":7.8,
        "category":"Accion2"
    }
]

@app.get('/',tags=['home'])

def message():
    return HTMLResponse('<h1>Hola mundo</h1>')

@app.post('/login',tags=['auth'])
def login(user:User):
    if user.email=="admin@gmail.com" and user.password=="admin":
        token: str=create_token(user.dict())
    return JSONResponse(status_code=200, content=token)

@app.get('/movies',tags=['movies'],response_model=List[Movie], status_code=200,dependencies=[Depends(JWTBearer())])
def getmMovies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


@app.get('/movies/{id}',tags=['movies'],response_model=Movie)
def getMoviesId(id: int):

    for item in movies:
        if item["id"]==id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])


@app.get('/movies/',tags=['movies'], response_model=List[Movie])
def getMoviesCategory(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [ item for item in movies if item['category'] == category ]
    return JSONResponse(content=data)

@app.post('/movies',tags=['movies'],response_model=dict, status_code=201)
def createMovie(movie:Movie)->dict:
    movies.append(movie)    
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})


@app.put('/movies/{id}',tags=['movies'],response_model=dict, status_code=200)
def updateMovie(id:int,movie:Movie):
    for item in movies:
        if item["id"]==id:
            item['title']=movie.title
            item['overview']=movie.overview
            item['year']=movie.year
            item['rating']=movie.rating
            item['category']=movie.category
            return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

@app.delete('/movies',tags=['movies'], response_model=dict, status_code=200)
def deleteMovie(id:int):
    for item in movies:
        if item["id"]==id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})