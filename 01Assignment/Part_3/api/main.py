from re import A
import sys
import json
from pydantic import PydanticUserError
from sqlalchemy.orm.scoping import ScopedSession
sys.path.append("../../../")
from typing import Optional, List, Any, Dict
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
)
import models.owner_model as saOwner
from models.car_model import Car
from schemas.owner_schema import OwnerCreateDTO, OwnsCar, OwnerRead, OwnerWithCarsDTO, OwnsCarUpdate
from schemas.car_schema import CarWithOwnersDTO, CarRead

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
    model_dict = pydantic_model.model_dump(exclude_unset=True)
    return model_class(**model_dict)

def serialize(item: List[str]) -> str:
    return json.dumps(item)


@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/api/v1/owners", response_model=List[OwnerRead])
async def get_all_owners(skip: int = 0, limit: int = 20, db: ScopedSession = Depends(get_db)) -> Any:
    sa_owners = db.query(saOwner.Owner).offset(skip).limit(limit).all()
    owners: List[OwnerRead] = []
    for owner in sa_owners:
        owners.append(to_pydantic(owner, OwnerRead))
    return owners
    
@app.get("/api/v1/cars", response_model=List[CarRead])
async def get_all_cars(skip: int = 0, limit: int = 20, db: ScopedSession = Depends(get_db)) -> Any:
    sa_cars = db.query(Car).offset(skip).limit(limit).all()
    cars: List[CarRead] = []
    for car in sa_cars:
        cars.append(to_pydantic(car, CarRead))
    return cars

@app.post("/api/v1/owners/", response_model=Any)
async def create_owner(*, db: ScopedSession = Depends(get_db), owner: OwnerCreateDTO):   
    owner_data = owner.model_dump(exclude={'cars'})
    sa_owner = saOwner.Owner(**owner_data)
    sa_cars = []
    for car in owner.cars:
        car_data = car.model_dump()
        sa_car = saOwner.OwnsCar(**car_data) 
        sa_cars.append(sa_car)
    db.add(sa_owner)
    db.add_all(sa_cars)
    db.commit()
    '''
    db.refresh(sa_owner)
    db.refresh(sa_cars)
    '''
    return {"new owner id": owner.id}

@app.get("/api/v1/owners-full-details{owner_id}", response_model=OwnerWithCarsDTO)
async def get_owner_car(owner_id: int, db: ScopedSession = Depends(get_db)) -> Any:
    sa_owner = db.query(saOwner.Owner).filter(saOwner.Owner.id == owner_id).first()
    if sa_owner is None:
        raise HTTPException(status_code=404,
                            detail="Owner not found")
    owner:OwnerRead = to_pydantic(sa_owner, OwnerRead)
    sa_cars = db.query(saOwner.OwnsCar).filter(saOwner.OwnsCar.owner_id == owner_id).all()
    cars:List[OwnsCar] = []
    if sa_cars is None:
        print("no cars")
    else:
        for car in sa_cars:
            cars.append(to_pydantic(car, OwnsCar))

    return OwnerWithCarsDTO(owner=owner, cars=cars)

@app.get("/api/v1/cars-full-details{car_id}", response_model=CarWithOwnersDTO)
async def get_car_owner(car_id: int, db: ScopedSession = Depends(get_db)) -> Any:
    # get the sa car
    sa_car = db.query(saOwner.Car).filter(saOwner.Car.id == car_id).first()
    if sa_car is None:
        raise HTTPException(status_code=404,
                            detail="Car not found")
    car:CarRead = to_pydantic(sa_car, CarRead)
    # find all owners of the car
    sa_owns_car = db.query(saOwner.OwnsCar).filter(saOwner.OwnsCar.car_id == car_id).all()
    car_owners:List[OwnerWithCarsDTO] = []
    if sa_owns_car is None:
        print("no owner for this car")
    else:
        # build the OwnerWithCarsDTO
        for sa_own_car in sa_owns_car:
            sa_owner = db.query(saOwner.Owner).filter(saOwner.Owner.id == sa_own_car.owner_id).first()
            owner = to_pydantic(sa_owner, saOwner.Owner)
            car_owners.append(await get_owner_car(owner_id=owner.id, db=db))

    return CarWithOwnersDTO(car=car, owners=car_owners)

@app.patch("/api/v1/owner/{owner_id}", response_model=OwnsCarUpdate)
async def update_car(*, owner_id: int, db: ScopedSession=Depends(get_db), cars: OwnsCarUpdate) -> Any:
    owner_cars: OwnerWithCarsDTO = await get_owner_car(owner_id=owner_id, db=db)
    owner_data = owner_cars.model_dump(exclude={'cars'})
    car_data = owner_cars.model_dump(exclude={'owner'})

    return car_data


'''
    
@app.get("/api/v1/cars", response_model=List[CarBase])
async def fetch_cars(skip: int=0, limit: int=20, db: ScopedSession=Depends(get_db)) -> Any:
    cList = db.query(Car).offset(skip).limit(limit).all()
    cars: List[CarBase] = []
    for car in cList:
        new = to_pydantic(car, CarBase)
        cars.append(new)
    return cars

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
