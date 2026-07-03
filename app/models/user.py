from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    name: str
    email: str


class User(SQLModel, table=True):
    username: str = Field(default = None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    username: str