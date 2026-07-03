from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Annotated


class EventBase(SQLModel):
    title: Annotated[str, Field(min_length=1, max_length=30)]
    description: Annotated[str, Field(min_length=1, max_length=200)]
    date: datetime
    location: Annotated[str, Field(min_length=1, max_length=50)]


class Event(EventBase, table=True):
    id : int = Field(default=None, primary_key=True)


class EventCreate(EventBase):
    pass


class EventPublic(EventBase):
    id: int