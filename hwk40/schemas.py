from datetime import date
from pydantic import BaseModel, Field

CURRENT_YEAR = date.today().year

class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=100)
    year: int = Field(gt=0, le=CURRENT_YEAR)
    rating: float = Field(ge=0, le=10)
    description: str | None = Field(default=None)

class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    genre: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, gt=0, le=CURRENT_YEAR)
    rating: float | None = Field(default=None, ge=0, le=10)
    description: str | None = Field(default=None)

class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    year: int
    rating: float
    description: str | None

    class Config:
        from_attributes = True