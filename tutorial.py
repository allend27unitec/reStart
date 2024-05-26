from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID
from tutorial_models import UserAccount, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[UserAccount] = [
    UserAccount(
        id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
        first_name="Jamila",
        last_name="Ahmed",
        middle_name="",
        gender=Gender.female,
        roles=[Role.admin, Role.user]
    ),
    UserAccount(
        id=UUID("b11b61d1-537f-469d-aa7a-11617e028506"),
        first_name="Alexa",
        last_name="Jones",
        middle_name='',
        gender=Gender.male,
        roles=[Role.student, Role.user]
    ),
    UserAccount(
        id=UUID("b90c04ce-16fc-4615-91d5-a39e3ebdd016"),
        first_name="Alex",
        middle_name="Beth",
        last_name="Mohammed",
        gender=Gender.male,
        roles=[Role.admin]
    )]

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/api/v1/fetch")
async def fetch_users():
    return db

@app.post("/api/v1/register")
async def register_user(user: UserAccount):
    db.append(user)
    return {"registered id": user.id}

@app.delete("/api/v1/delete/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if (user.id == user_id):
            db.remove(user)
            return {"deleted user": user_id} 
    #      return {"404 not found": user_id}
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )

@app.put("/api/v1/update/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if (user.id == user_id):
            if (user_update.first_name is not None):
                user.first_name = user_update.first_name
            if (user_update.last_name is not None):
                user.last_name = user_update.last_name
            user.middle_name = user_update.middle_name
            if (user_update.roles is not None):
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )
