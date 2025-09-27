from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from app.config import POSTGRES_URL


engine = create_engine(url=POSTGRES_URL)


def create_database_tables():
    SQLModel.metadata.create_all(bind=engine)


session = Session(bind=engine)


def get_session():
    with Session(bind=engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
