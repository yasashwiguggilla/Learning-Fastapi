from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL Database URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:yashu%402005@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()

