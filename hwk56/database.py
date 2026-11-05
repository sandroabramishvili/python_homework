from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:madagascar@localhost:5432/hwk56"

engine = create_engine(DATABASE_URL)