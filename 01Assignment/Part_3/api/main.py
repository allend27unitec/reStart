import sys

from pydantic import PydanticUserError
from sqlalchemy.orm.scoping import ScopedSession
sys.path.append("../../../")
from typing import Optional, List, Any, Dict
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import Column, Integer, String, create_engine, null
from sqlalchemy.orm import (
    Session,
    sessionmaker,
    scoped_session
)
from models.owner_model import Owner, OwnsCar, Car
from schemas.owner_schema import OwnerBase, OwnerCreateDTO, OwnsCar, OwnerWithCarsDTO, OwnerRead, OwnerUpdate
from schemas.car_schema import CarBase, CarCreate, CarUpdate, CarRead

app = FastAPI(
    title="Assignment 1 Part 3 ",
    description="Demonstration of Object Orientated Programming (OOP), modular class structure, and Data Transfer Object (DTO) using an API"
    )
# Set up database connection
def create_session() -> ScopedSession:
    try:
        engine = create_engine("sqlite:///part3.db")
        session_factory = sessionmaker(bind=engine)
        print(f"Sqlite Connection successful")
        return scoped_session(session_factory)
    except Exception as e:
         print(f"Sqlite Connection Exception {e}")

def get_db():
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


@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/api/v1/owners", response_model=List[OwnerRead])
async def get_all_owners(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)) -> Any:
    oList = db.query(Owner).offset(skip).limit(limit).all()
    owners: List[OwnerRead] = []
    for owner in oList:
        new = to_pydantic(owner, OwnerRead)
        owners.append(new)
    return owners
    
@app.post("/owners/", response_model=OwnerRead)
async def create_owner(*, db: Session = Depends(get_db), owner: OwnerCreateDTO):   
    owner_dict = OwnerCreateDTO.model_dump(owner)
    new = from_pydantic(OwnerCreateDTO, owner_dict)
    print("DTO dump")
    print(owner_dict)
    try:
       print(owner_dict.model_json_schema())
    except PydanticUserError as e:
       print(e)
    print()
    print(OwnerCreateDTO.model_validate(new))
    # db.add(new)
    #db.commit()
    #db.refresh(new)
    return new

@app.get("/api/v1/owners-full-details{owner_id}", response_model=List[OwnerRead])
async def get_owner_car(owner_id: int, db: Session = Depends(get_db)) -> Any:
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    owners: List[OwnerRead] = []
    if owner is None:
        raise HTTPException(status_code=404,
                            detail="Owner not found")
    new = to_pydantic(owner, OwnerRead)
    owners.append(new)
    '''
    cars = db.query(OwnsCar).filter(OwnsCar.owner_id == owner_id).all()
    if cars is None:
        print("no cars")
    else:
        for car in cars:
            new = to_pydantic(car, CarRead)
            print(new)

    '''
    
    return owners

@app.get("/api/v1/cars", response_model=List[CarBase])
async def fetch_cars(skip: int=0, limit: int=20, db: Session=Depends(get_db)) -> Any:
    cList = db.query(Car).offset(skip).limit(limit).all()
    cars: List[CarBase] = []
    for car in cList:
        new = to_pydantic(car, CarBase)
        cars.append(new)
    return cars

'''
@app.get("/api/v1/owner{owner_id}/cars", response_model=List[CarRead])
async def get_owner_cars(owner_id:int) -> Any:
    car_ids = [oc.car_id for oc in ownsCar_db if (oc.owner_id == owner_id)]
    cars = [car for car in car_db if (car.id in car_ids)]
    return cars

@app.get("/api/test", response_model=None)
async def get_dict_items(owner_id:int) -> Any:
    ditems:List
    for o in owner_db: 
        if (owner_id == o.id): owner=o
    data = owner.dict()
    print(dir(data))
    return ditems
    for key, value in data.items():
        ditems.append("{} {}".format(key, value))


@app.get("/api/v1/show/{user_id}")
async def show_user(user_id: int):
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
async def delete_user(user_id: int):
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
async def update_user(user_update: OwnerUpdateRequest, user_id: int):
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
'''
