from fastapi import APIRouter, Path, Query, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from jwt_handler import validate_token
from fastapi.security import HTTPBearer
from db.database import Session, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

router_movie = APIRouter()

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials) # type: ignore
        if data["username"] != "stiven":
            raise HTTPException(status_code=403, detail="Credenciales son inválidas")

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Mi película", min_length=5, max_length=40)
    overview: str = Field(default="Descripción de la película", min_length=15, max_length=200)
    year: int = Field(default=2022, ge=1900, le=2025)
    rating: float = Field(ge=1, le=10)
    category: str = Field(default="Mi categoría", min_length=5, max_length=15)

@router_movie.get("/movies", tags=["movies"], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(data))

@router_movie.get("/movies/{id}", tags=["movies"], status_code=200)
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


@router_movie.get("/movies/", tags=["movies"])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not data:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@router_movie.post("/movies", tags=["movies"], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película", "movie": movie.model_dump()})

@router_movie.put("/movies/{id}", tags=["movies"], status_code=200)
def update_movie(id: int, movie: Movie):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    data.title = movie.title # type: ignore
    data.overview = movie.overview # type: ignore
    data.year = movie.year # type: ignore
    data.rating = movie.rating # type: ignore
    data.category = movie.category # type: ignore
    db.commit()
    return JSONResponse(content={"message": "Se ha modificado la película"})

@router_movie.delete("/movies/{id}", tags=["movies"], status_code=200)
def delete_movie(id: int):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    db.delete(data)
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminado la película", "movie": jsonable_encoder(data)})