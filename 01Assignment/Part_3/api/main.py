import sys
import json
import logging
from pydantic import PydanticUserError
sys.path.append("../../")
from typing import List, Any
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import (
        sessionmaker,
        Session
        )
import models.owner_model as saOwner
from models.car_model import Car
from schemas.owner_schema import (
        OwnerCreateDTO, 
        OwnsCar, 
        OwnerRead, 
        OwnerWithCarsDTO, 
        UpdateCar 
        )
from schemas.car_schema import (
        CarWithOwnersDTO, 
        CarRead, 
        CarBase, 
        CarCreate
        )

app = FastAPI(
    title="Assignment 1 Part 3 ",
    description="Demonstration of Object Orientated Programming (OOP), modular class structure, and Data Transfer Object (DTO) using an API"
    )

logger=logging.getLogger('uvicorn')

# Set up database connection
def create_session() -> Session:
    try:
        engine = create_engine("sqlite:///part3.db")
        session = sessionmaker(bind=engine)
        print(f"Sqlite Connection successful")
        return session()
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

# the db needs to be passed in.  Depends can only be used in FastAPI endpoints
def check_car_exits(car_id: int, db: Session) -> bool:
    sa_car = db.get(Car, car_id)
    if (sa_car): return True
    return False

def check_owner_exits(owner_id: int, db: Session) -> bool:
    sa_owner = db.get(saOwner.Owner, owner_id)
    if (sa_owner): return True
    return False

def check_ownscar_exits(ownscar_id: int, db: Session) -> bool:
    sa_ownscar = db.get(saOwner.OwnsCar, ownscar_id)
    if (sa_ownscar): return True
    return False

@app.get("/")
async def root():
    return {"Hello": "Part 3"}

@app.get("/api/v1/owners", status_code=status.HTTP_200_OK, response_model=List[OwnerRead])
async def get_all_owners(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)) -> Any:
    sa_owners = db.query(saOwner.Owner).offset(skip).limit(limit).all()
    owners: List[OwnerRead] = []
    for owner in sa_owners:
        owners.append(to_pydantic(owner, OwnerRead))
    return owners
   
@app.get("/api/v1/cars", response_model=List[CarRead])
async def get_all_cars(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)) -> Any:
    sa_cars = db.query(Car).offset(skip).limit(limit).all()
    cars: List[CarRead] = []
    for car in sa_cars:
        cars.append(to_pydantic(car, CarRead))
    return cars

@app.post("/api/v1/register/", status_code=status.HTTP_201_CREATED, response_model=OwnerWithCarsDTO)
async def create_owner(*, db: Session = Depends(get_db), owner: OwnerCreateDTO):   
    owner_data = owner.model_dump(exclude={'cars'})
    sa_owner = saOwner.Owner(**owner_data)
    or_owner = to_pydantic(sa_owner, OwnerRead)
    sa_cars = []
    for car in owner.cars:
        car_data = car.model_dump()
        sa_car = saOwner.OwnsCar(**car_data) 
        sa_cars.append(sa_car)
    db.add(sa_owner)
    db.commit()
    db.refresh(sa_owner)
    if (sa_cars is not None):
        db.add_all(sa_cars)
        db.commit()
       # db.refresh(sa_cars)
    return OwnerWithCarsDTO(owner=or_owner, cars=owner.cars)
    
@app.post("/api/v1/carregister/", status_code=status.HTTP_201_CREATED, response_model=CarBase)
async def create_car(*, car: CarCreate, db: Session = Depends(get_db)):   
    sa_car = from_pydantic(car, Car) 
    if (check_car_exits(sa_car.id, db)):
        logger.error(f"attempt to create car with id {sa_car.id} - already exists.")
        cnt = db.query(Car).count() + 1
        sa_car.id = cnt
        car.id = cnt
        logger.error(f"Auto-incrementing - new id is {cnt}")
    
    db.add(sa_car)
    db.commit()
    db.refresh(sa_car)
    new_car = to_pydantic(sa_car, CarBase)  # adds the create and update
    logger.info(f"new car {new_car}")
    return CarBase(id=new_car.id,
                   make=new_car.make, 
                   model=new_car.model,
                   style=new_car.style,
                   year=new_car.year,
                   updated_at=new_car.updated_at,
                   created_at=new_car.created_at)


@app.get("/api/v1/owners-full-details{owner_id}", response_model=OwnerWithCarsDTO)
async def get_owner_car(owner_id: int, db: Session = Depends(get_db)) -> Any:
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
async def get_car_owner(car_id: int, db: Session = Depends(get_db)) -> Any:
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


@app.delete("/api/v1/deleteowner/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_owner(*, owner_id: int, db: Session=Depends(get_db)):
    sa_owner = db.query(saOwner.Owner).filter(saOwner.Owner.id == owner_id).one_or_none()
    #sa_owner = db.query(saOwner.Owner).get(owner_id)
    if sa_owner is not None:
        logger.info(f"successful attempt to delete owner {owner_id}")
        db.delete(sa_owner)
        db.commit()
        owner:OwnerRead = to_pydantic(sa_owner, OwnerRead)
        sa_cars = db.query(saOwner.OwnsCar).filter(saOwner.OwnsCar.owner_id == owner_id).all()
        cars:List[OwnsCar] = []
        if sa_cars is None:
            logger.info(f"no cars for owner with id {owner_id}")
        else:
            for car in sa_cars:
                db.delete(car)
                db.commit()
                logger.info(f"delete car {car.id} for owner with id {owner_id}")
        return {f"deleted owner: {owner_id}"} 
    logger.error(f"attempt to delete owner {owner_id} - not found")
    raise HTTPException(
        status_code=404,
        detail=f"owner with id: {owner_id} does not exist"
        )

'''
    patching any attribute within the context of the child entity (of a one to many
    relationship) requires the identification of the child record. This is would be the
    role of the client. The assignment question assumes a database structure that has
    not been normalised, and only one car (based on the provided endpoint).  Therefore,
    the endpoint has been altered to accomodate the structure employed. There are a 
    few ways of doing this:
    1. "/api/v1/owner/{owner_id}/car{car_id}" (assuming to own only one of such car)
    2. "/api/v1/ownscar/{ownscar_id}"
    3. "/api/v1/owner{owner_id}/ownscar{ownscar_id}"
    I chose the easiest way.
'''
@app.patch("/api/v1/ownscar/{ownscar_id}", status_code=status.HTTP_206_PARTIAL_CONTENT, response_model=UpdateCar)
async def update_car(*, ownscar_id: int, ownscar_update: UpdateCar, db: Session=Depends(get_db)):
    sa_ownscar = db.get(saOwner.OwnsCar, ownscar_id)
    if (sa_ownscar is None):
        logger.info(f"owner car record not found for id {ownscar_id}")
        raise HTTPException(
            status_code=404,
            detail=f"ownscar with id: {ownscar_id} does not exist"
            )
        
    update_data = ownscar_update.model_dump(exclude_unset=True)
    print(update_data)
    for key, value in update_data.items():
        setattr(sa_ownscar, key, value)
    db.commit()
    db.refresh(sa_ownscar)

    return update_data
