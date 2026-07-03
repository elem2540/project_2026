from typing_extensions import Annotated

from app.models.user import User, UserCreate, UserPublic
from fastapi import APIRouter, Query
from data.db import SessionDep
from sqlmodel import select

router = APIRouter(prefix="/users") # all router endpoints will start from /users

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

@router.post("/")
def add_user(
    user: UserCreate,
    session: SessionDep
) -> JSONResponse:
    """ 
    Adds a new user to the database.
    """
    if user.username in session.exec(select(User.username)).all():
        raise HTTPException(status_code=422, detail="Username already exists")
    new_user = User(username=user.username, password=user.password)
    session.add(new_user)
    session.commit()
    return JSONResponse(
        status_code=201,
        content={"msg": "User created successfully!", "username": new_user.username}
        )

@router.delete("/")
def delete_all_users(
    session: SessionDep
) -> JSONResponse:
    """
    Deletes all users from the database.
    """
    session.exec(delete(User))
    session.exec(delete(Registration))
    session.commit()
    return JSONResponse(
        status_code=200,
        content={"msg": "All users deleted successfully!"}
    )

@router.delete("/{username}")
def delete_user_by_username(
    session: SessionDep,
    username: Annotated[str, Query(description="Username of the user to delete", examples="jackey57")]
):
    """
    Deletes a user from the database based on their username
    """
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.exec(delete(Registration).where(Registration.username == username))
    session.delete(user)
    session.commit()
    return JSONResponse(
        status_code=200,
        content={"msg": f"User '{username}' deleted successfully!"}
    )
