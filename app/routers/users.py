from typing_extensions import Annotated

from app.models.user import User, UserCreate, UserPublic
from fastapi import APIRouter, Query
from data.db import SessionDep
from sqlmodel import select

router = APIRouter(prefix="/users") # tutti gli endpoint del router partiranno da /users
@router.get("/", response_model=list[UserPublic])
def get_all_users(    
    session: SessionDep,
    sort: Annotated[
        bool,
        Query(description="Sort users by username", examples=[True])
    ] = False
): 
    users = session.exec(select(User)).all()

    if sort:
        users.sort(key=lambda user: user.username)

    return users
    