from sqlmodel import SQLModel, Field
from typing import Annotated


class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    name: str
    email: str