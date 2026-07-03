from sqlmodel import SQLModel, Field
from datetime import datetime


class EventBase(SQLModel):
    title: str
    description: str
    date: datetime
    location: str


class Event(SQLModel, table=True):
    id : int = Field(default = None, primary_key=True)


class EventCreate(EventBase):
    pass


class EventiPublic(EventBase):
    id: int