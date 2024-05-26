import sys
import random
sys.path.append("../../../")
from typing import Optional, List, Any, Dict
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
    scoped_session
)
from passlib.context import CryptContext
from jose import JWTError, jwt
from uuid import UUID, uuid4
from project.settings import settings
from models.owner_model import Owner, OwnsCar
from schemas.owner_schema import OwnerBase, OwnerCreate, OwnsCar, OwnerWithCarsDTO, OwnerRead, OwnerUpdate
from schemas.car_schema import CarBase, CarCreate, CarUpdate, CarRead

app = FastAPI(
    title="Assignment 1 Part 3 ",
    description="Demonstration of Object Orientated Programming (OOP), modular class structure, and Data Transfer Object (DTO) using an API"
    )
# Set up database connection
def create_session():
    try:
        engine = settings.postgresql_engine()
        session_factory = sessionmaker(bind=engine)
        print(f"Postgresql Connection successful")
        return scoped_session(session_factory)
    except Exception as e:
         print(f"Postgresql Connection Exception {e}")

def get_db() -> Session:
    db = create_session()
    try:
        yield db # pause and inject db
    finally:
        db.close() # close when done

def to_pydantic(model_instance, pydantic_model):
    model_dict = {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}
    return pydantic_model(**model_dict)

def from_pydantic(pydantic_model, model_class):
    model_dict = pydantic_model.dict(exclude_unset=True)
    return model_class(**model_dict)

owner_db: List[OwnerBase] = [
    OwnerBase(
    id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    first_name="John",
    last_name="Adams",
    middle_name=""
    ),
    OwnerBase(
    id=UUID("b11b61d1-537f-469d-aa7a-11617e028506"),
    first_name="Alexa",
    last_name="Jones",
    middle_name=''
    ),
    OwnerBase(
    id=UUID("b19b51e1-437f-469d-ab7c-227282272806"),
    first_name="Martin",
    last_name="Smith",
    middle_name=''
    ),
    OwnerBase(
    id=UUID("b90c04ce-16fc-4615-91d5-a39e3ebdd016"),
    first_name="Steven",
    last_name="King",
    middle_name=""
    )]
car_db: List[CarBase] = [
    CarBase(
    id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    make="Ford",
    model="Ranger",
    style="4x4",
    colour="Red",
    year="2024"
    ),
    CarBase(
    id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    make="Ford",
    model="Mustang",
    style="convertible",
    colour="red",
    year="2024"
    ),
    CarBase(
    id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    make="Tesla",
    model="CyberTruck",
    style="4x4",
    colour="Silver",
    year="2024"
    )]
ownsCar_db: List[OwnsCar] = [
    OwnsCar(
    id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    owner_id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    car_id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    colour="",
    registration="",
    purchased_dt=1679616000.0
    ),
    OwnsCar(
    id=UUID("45002df7-5c5e-5cc5-977c-2253cd69a2b0"),
    owner_id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    car_id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    colour="",
    registration="",
    purchased_dt=1679616000.0
    ),
    OwnsCar(
    id=UUID("23880be6-4a3c-4bb4-977c-2253cd69a2b0"),
    owner_id=UUID("b19b51e1-437f-469d-ab7c-227282272806"),
    car_id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    colour="",
    registration="",
    purchased_dt=1679616000.0
    )]

ownerWithCarsDTO_db: List[OwnerWithCarsDTO] = []

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/api/v1/owners", response_model=List[OwnerRead])
async def fetch_users() -> Any:
    return owner_db

@app.get("/api/v1/cars", response_model=List[CarRead])
async def fetch_cars() -> Any:
    return car_db

@app.get("/api/v1/owner{owner_id}/cars", response_model=List[CarRead])
async def get_owner_cars(owner_id:UUID) -> Any:
    car_ids = [oc.car_id for oc in ownsCar_db if (oc.owner_id == owner_id)]
    cars = [car for car in car_db if (car.id in car_ids)]
    return cars

@app.get("/api/test", response_model=None)
async def get_dict_items(owner_id:UUID) -> Any:
    ditems:List
    for o in owner_db: 
        if (owner_id == o.id): owner=o
    data = owner.dict()
    print(dir(data))
    return ditems
"""
    for key, value in data.items():
        ditems.append("{} {}".format(key, value))
"""


"""
@app.get("/api/v1/show/{user_id}")
async def show_user(user_id: UUID):
    for user in db:
        if (user.id == user_id):
            return user 
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
        )

@app.post("/api/v1/register", response_model=None)
async def register_user(user: OwnerCreate) -> Owner:
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
async def update_user(user_update: OwnerUpdateRequest, user_id: UUID):
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
    return
"""

if __name__ == "__main__":
#    Session = create_session()
    emp = Owner(
    id=UUID("b11b61d1-537f-469d-aa7a-11617e028506"),
    first_name="Alexa",
    last_name="Jones",
    middle_name='',
    )
    print("user: ", emp.id, emp.full_name)
