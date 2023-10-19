from pydantic import BaseModel, Field
from typing import Optional


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=10)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 3,
                "title": "Mi pelicula",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 0.8,
                "category": "Accion"
            }
        }
