# Assignment — Movie Catalog API

Create a **Movie Catalog FastAPI** using FastAPI, PostgreSQL, SQLAlchemy, and Pydantic.

The API must support adding, retrieving, updating, deleting, filtering, and searching movies.

## 1. Database

Create a SQLAlchemy model for the `movies` table with the following fields:

| Field         | Type    | Notes     |
|---------------|---------|-----------|
| `id`          | Integer | Primary Key |
| `title`       | String  | required  |
| `genre`       | String  | required  |
| `year`        | Integer | required  |
| `rating`      | Float   | required  |
| `description` | Text    | optional  |

`rating` must be between 0 and 10, and `year` must be a positive and realistic value.

## 2. Pydantic Schemas

Create at least three Pydantic schemas:

- **`MovieCreate`** — for creating a new movie
- **`MovieUpdate`** — for updating an existing movie
- **`MovieResponse`** — for the API's response

In `MovieUpdate`, all fields must be optional, so that it's possible to update only a specific field.

For example, the following request should change only the rating:

```json
{
    "rating": 9.2
}
```

`MovieResponse` must also return the `id` created by the database.

## 3. CRUD Endpoints

Create the following endpoints:

### `POST /movies`

Add a new movie to the database.

Example:

```json
{
    "title": "Inception",
    "genre": "Sci-Fi",
    "year": 2010,
    "rating": 8.8,
    "description": "A thief who steals corporate secrets..."
}
```

When creating a new record, use SQLAlchemy's `add()`, `commit()`, and `refresh()`.

### `GET /movies`

Return all movies in the database.

Add the following query parameters to the endpoint, all optional:

- `genre`
- `min_rating`
- `max_rating`
- `year`

| Request | Result |
|---|---|
| `GET /movies?genre=Action` | only movies of the Action genre |
| `GET /movies?min_rating=8&max_rating=10` | only movies with a rating between 8 and 10 |
| `GET /movies?genre=Drama&year=2020` | only Drama movies from 2020 |

It should also be possible to combine filters with each other.

### `GET /movies/{movie_id}`

Return a specific movie by ID.

If the movie doesn't exist, return `404 Not Found` using FastAPI's `HTTPException`.

### `PATCH /movies/{movie_id}`

Update an existing movie. All fields in the `MovieUpdate` schema must be optional, so it should be possible to change one or several fields.

For example:

```json
{
    "rating": 9.5
}
```

### `DELETE /movies/{movie_id}`

Delete a movie by ID.

If the movie doesn't exist, return `404 Not Found`.

## 4. Database Dependency

Separate the database connection and session configuration into their own file.

Create a dependency:

```python
def get_db():
    ...
```

and in the endpoints, obtain the database session via FastAPI's Dependency Injection:

```python
db: Session = Depends(get_db)
```

The database session must not be created manually in each endpoint.

## 5. Project Structure

Organize the project with at least the following structure:

```text
movie_api/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
└── requirements.txt
```

## 6. Bonus Part ⭐

Create:

### `GET /movies/search`

Accept a query parameter:

```text
GET /movies/search?q=matrix
```

and return all movies whose `title` contains the searched text.

For example, `q=matrix` should find:

- The Matrix
- The Matrix Reloaded
- The Matrix Revolutions

The search must be case-insensitive. For this, use an appropriate SQLAlchemy filtering mechanism, such as `ilike()`.

## Main Requirement

While completing the assignment, pay attention not only to the endpoints working, but also to **correct integration of FastAPI and SQLAlchemy**.

Your project must use:

- SQLAlchemy Models for working with the database
- Pydantic Schemas for request/response data validation
- SQLAlchemy Session for database operations
- FastAPI Dependency Injection via `Depends()`
- CRUD operations
- Query and Path Parameters
- appropriate HTTP status codes
- `HTTPException` for handling errors
