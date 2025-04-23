from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_URL_DATABASE: str = "sqlite:///./smartStock.db"

engine = create_engine(url=SQLALCHEMY_URL_DATABASE, connect_args={
    "check_same_thread": False})

LocalSession = sessionmaker(engine, autoflush=False, autocommit=False)

Base = declarative_base()
