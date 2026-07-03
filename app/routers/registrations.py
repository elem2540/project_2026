from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.data.db import SessionDep
from app.models.registration import Registration
from app.models.user import User
from app.models.event import Event


router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.get("/")
def get_all_registrations(
    session: SessionDep) -> list[Registration]:
    """Restituisce la lista di tutte le registrazioni presenti nel database."""
    registrations = session.exec(select(Registration)).all()
    return registrations


@router.delete("/")
def delete_registration(
    session: SessionDep,
    username: Annotated[str, Query(description="Username dell'utente registrato")],
    event_id: Annotated[int, Query(description="ID dell'evento")],
):
    """
    Elimina una singola registrazione identificata tramite username ed event_id.
    Restituisce 404 se l'utente, l'evento o la registrazione non esistono.
    """
    user = session.get(User, username)
    if user is None:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    event = session.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    registration = session.exec(
        select(Registration).where(
            Registration.username == username,
            Registration.event_id == event_id,
        )
    ).first()

    if registration is None:
        raise HTTPException(status_code=404, detail="Registrazione non trovata")

    session.delete(registration)
    session.commit()

    return {"message": "Registrazione cancellata con successo"}