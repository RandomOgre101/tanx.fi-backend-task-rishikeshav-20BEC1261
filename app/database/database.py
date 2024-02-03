from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
# from contextlib import contextmanager

load_dotenv()

DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOSTNAME = os.environ.get("DATABASE_HOSTNAME")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_PORT = os.environ.get("DATABASE_PORT")


SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:password@localhost:5432/tanx-task'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()