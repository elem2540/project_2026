from sqlmodel import SQLModel, Field
from typing import Annotated


class UserBase(SQLModel):
    username: Annotated[str, Field(min_length=1, max_length=50)]
    name: Annotated[str, Field(min_length=1, max_length=30)]
    email: Annotated[str, Field(min_length=1, max_length=100)]


class User(UserBase, table=True):
    username: str = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    pass