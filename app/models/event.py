from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Annotated


class Event(SQLModel, table=True):
    id : int = Field(default = None, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str