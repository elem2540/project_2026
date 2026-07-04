from sqlmodel import create_engine, SQLModel, Session, select
from typing import Annotated
from fastapi import Depends
import os
from faker import Faker
from app.config import config
# TODO: remember to import all the DB models here
from app.models.user import User
from app.models.event import Event
from app.models.registration import Registration  # NOQA


sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def init_database() -> None:
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:
            # TODO: (optional) initialize the database with fake data
            events = []
            for i in range(10):
                event = Event(
                    title=f.sentence(nb_words=5)[:30],
                    description=f.sentence(nb_words=30)[:200],
                    date=f.date_time_between(start_date="now", end_date="+1y"),
                    location=f.city()[:50]
                )
                session.add(event)
                events.append(event)

            users = []
            for i in range(10):
                user = User(
                    username=f.user_name()[:50],
                    name=f.name()[:30],
                    email=f.email()[:100],
                )
                session.add(user)
                users.append(user)
            session.flush()

            for i in range(3):
                registration = Registration(
                    event_id=events[i].id,
                    username=users[i].username
                )
                session.add(registration)

            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
