from fastapi import APIRouter, HTTPException, Path, Query
from sqlmodel import select, delete

from typing import Annotated
from app.data.db import SessionDep

from app.models.registration import Registration
from app.models.user import User
from app.models.event import Event


router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.get("/")
def get_all_registrations(
    session: SessionDep) -> list[Registration]:
    """
    Returns the list of all registrations in the database.
    """
    registrations = session.exec(select(Registration)).all()
    return registrations


@router.delete("/")
def delete_registration(
    session: SessionDep,
    username: Annotated[str, Path(description="Username of the registered user")],
    event_id: Annotated[int, Path(description="ID of the event")],
):
    """
    Deletes a single registration identified by username and event_id.
    Returns 404 if the user, event, or registration does not exist.
    """
    user = session.get(User, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    event = session.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    registration = session.exec(
        select(Registration).where(
            Registration.username == username,
            Registration.event_id == event_id,
        )
    ).first()

    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")

    session.delete(registration)
    session.commit()

    return {"message": "Registration deleted successfully!"}
