from typing_extensions import Annotated

from app.models.user import User, UserCreate, UserPublic
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from app.data.db import SessionDep
from sqlmodel import select

router = APIRouter(prefix="/users")  # tutti gli endpoint del router partiranno da /users


@router.get("/")
def get_all_users(
        session: SessionDep,
        sort: Annotated[
            bool,
            Query(description="Sort users by username", examples=[True])
        ] = False
) -> list[UserPublic]:
    """ Returns the list of all users. """

    users = session.exec(select(User)).all()

    if sort:
        users.sort(key=lambda user: user.username)

    return list(users)


@router.get("/{username}")
def get_user_by_username(
        username: Annotated[str, Query(description="The username of the user to retrieve", examples=["igor_miti"])],
        session: SessionDep
) -> JSONResponse:
    """ Returns the user with the given ID. """

    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content={
        "msg": "User found",
        "username": user.username,
        "name": user.name,
        "email": user.email
    }, status_code=200)