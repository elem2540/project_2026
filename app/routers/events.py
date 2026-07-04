from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse

from app.models.event import EventCreate, EventPublic, Event
from app.models.user import UserCreate, User
from app.models.registration import Registration
from app.data.db import SessionDep

from typing import Annotated
from sqlmodel import select, delete


router = APIRouter(prefix="/events", tags=["events"])


@router.get("/")
def get_all_events(
        session: SessionDep,
        sort: Annotated[bool, Query(description="Sort events by their date")] = False
) -> list[EventPublic]:
    """ 
    Returns the list of available events.
    """
    events = session.exec(select(Event)).all()
    if sort:
         return sorted(events, key=lambda event: event.date)
    else:
        return list(events)


@router.post("/")
def add_event(session: SessionDep, event: EventCreate):
    """ 
    Adds a new event. 
    """
    event_entry = Event.model_validate(event)
    session.add(event_entry)
    session.commit()
    
    return JSONResponse(
        status_code=201,
        content={
            "msg": "Event added successfully!",
            "event_id": event_entry.id
        }
    )


@router.get("/{id}")
def get_event_by_id(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the event to retrieve", examples=[1])]
) -> JSONResponse:
    """ 
    Returns the event with the given ID. 
    """
    event = session.get(Event, id)
    if event:
        return JSONResponse(
            status_code=200,
            content={
                "msg": "Event retrieved successfully!",
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date.isoformat(),
                "location": event.location
            }
        )
    else:
        raise HTTPException(status_code=404, detail="Event not found")


@router.put("/{id}")
def replace_event(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the event to replace")],
    new_event: EventCreate
) -> str:
    """ 
    Replaces the event with the given ID. 
    """
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.title = new_event.title
    event.description = new_event.description
    event.date = new_event.date
    event.location = new_event.location
    session.add(event)
    session.commit()

    return "Event replaced successfully!"


@router.post("/{id}/register")
def add_registration(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the event to register for")],
    user: UserCreate
):
    """ 
    Registers a user for the event with the given ID.
    If the user isn't in the database, it creates it. 
    """
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    username = session.get(User, user.username)
    if not username:
        new_user = User.model_validate(user)
        session.add(new_user)
        session.commit()
        username = new_user

    registration = session.exec(
        select(Registration).where(
            Registration.username == username.username,
            Registration.event_id == event.id
        )
    ).first()
    if registration:
        raise HTTPException(status_code=400, detail="User already registered")

    new_registration = Registration( username=username.username, event_id=event.id)
    session.add(new_registration)
    session.commit()

    return JSONResponse(
        status_code=201,
        content={
            "msg": "User registered successfully!",
            "event_id": event.id
        }
    )


@router.delete("/")
def delete_all_events(
        session: SessionDep,
):
    """
    Deletes all events. 
    """
    session.exec(delete(Registration))
    session.exec(delete(Event))
    session.commit()

    return JSONResponse(
        status_code=200,
        content={
            "msg": "All events deleted successfully!"
        }
    )


@router.delete("/{id}")
def delete_event_by_id(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the event to delete")],
) -> JSONResponse:
    """ 
    Deletes the event with the given ID. 
    """
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    session.exec(delete(Registration).where(Registration.event_id == id))
    session.delete(event)
    session.commit()

    return JSONResponse(
        status_code=200,
        content={
            "msg": "Event deleted successfully!"
        }
    )