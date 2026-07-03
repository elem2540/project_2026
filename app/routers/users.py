@router.post("/")
def add_user(
    user: str = UserCreate,
    session: Any = SessionDep
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
        content={"msg": "User created successfully", "username": new_user.username}
        )