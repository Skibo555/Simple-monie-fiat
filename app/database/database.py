from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import settings


SQLALCHEMY_DATABASE_URI = (f"{settings.DATABASE_TYPE}://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@"
                           f"{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}")

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
