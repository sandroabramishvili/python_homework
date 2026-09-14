from fastapi import FastAPI, Depends, HTTPException
from starlette import status
from database import SessionLocal, get_db
from models import Movie
from sqlalchemy.orm import Session
from schemas import MovieCreate, MovieUpdate, MovieResponse

app = FastAPI(
    title="Movie Catalog API",
    description="API for managing a movie catalog with FastAPI, PostgreSQL, SQLAlchemy, and Pydantic.",
    version="1.0.0",
)

@app.post("/movies", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    new_movie = Movie(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@app.get("/movies", response_model=list[MovieResponse])
def get_all_movies(
        genre: str | None = None, 
        min_rating: float | None = None, 
        max_rating: float | None = None, 
        year: int | None = None, 
        db: Session = Depends(get_db)
):
    movies = db.query(Movie)

    if genre:
        movies = movies.filter(Movie.genre == genre)
    if min_rating is not None:
        movies = movies.filter(Movie.rating >= min_rating)
    if max_rating is not None:
        movies = movies.filter(Movie.rating <= max_rating)
    if year is not None:
        movies = movies.filter(Movie.year == year)

    return movies.all()

@app.get("/movies/search", response_model=list[MovieResponse])
def search_movies(q: str, db: Session = Depends(get_db)):
    movies = db.query(Movie).filter(Movie.title.ilike(f"%{q}%")).all()
    return movies

@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.patch("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(
        movie_id: int,
        movie: MovieUpdate,
        db: Session = Depends(get_db)
):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    for key, value in movie.model_dump(exclude_unset=True).items():
        setattr(db_movie, key, value)

    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(db_movie)
    db.commit()
    return {"message": "Movie deleted successfully"}
