from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class OwnerBase(SQLModel):
    first_name: str
    last_name: str
    national_id: str = Field(index=True)


class Owner(OwnerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    cars: List["Car"] = Relationship(back_populates="owner")


class OwnerCreate(OwnerBase):
    pass


class OwnerRead(OwnerBase):
    id: int


class CarBase(SQLModel):
    plate_number: str = Field(index=True)
    brand: str
    model: str
    year: int

    owner_id: Optional[int] = Field(default=None, foreign_key="owner.id")


class Car(CarBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    owner: Optional[Owner] = Relationship(back_populates="cars")


class CarRead(CarBase):
    id: int


class CarCreate(CarBase):
    pass


class CarReadWithOwner(CarRead):
    owner: Optional[OwnerRead] = None


class OwnerReadWithCars(OwnerRead):
    cars: List[CarRead] = []


class CarUpdate(SQLModel):
    plate_number: Optional[str] = None
    owner_id: Optional[int] = None


sqlite_file_name = "vtnz.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# POST http://127.0.0.1:8000/owners/
# Sample request body
# {
#     "first_name": "Mickey",
#     "last_name": "Mouse",
#     "national_id": "SHJDK432432"
# }
@app.post("/owners/", response_model=OwnerRead)
def create_owner(*, session: Session = Depends(get_session), owner: OwnerCreate):
    # ========================================================================
    #                 _                                _
    #                | |                              | |
    #    ___ ___   __| | ___    __ _  ___   ___  ___  | |__   ___ _ __ ___
    #   / __/ _ \ / _` |/ _ \  / _` |/ _ \ / _ \/ __| | '_ \ / _ \ '__/ _ \
    #  | (_| (_) | (_| |  __/ | (_| | (_) |  __/\__ \ | | | |  __/ | |  __/
    #   \___\___/ \__,_|\___|  \__, |\___/ \___||___/ |_| |_|\___|_|  \___|
    #                           __/ |
    #                          |___/
    # ========================================================================
    pass


# GET http://127.0.0.1:8000/owners-full-details/1
# Sample response body
# {
#     "first_name": "Mickey",
#     "last_name": "Mouse",
#     "national_id": "SHJDK432432",
#     "id": 1,
#     "cars": [
#         {
#             "plate_number": "HAS531",
#             "brand": "Toyota",
#             "model": "Vitz",
#             "year": 2012,
#             "owner_id": 1,
#             "id": 1,
#         }
#     ],
# }
@app.get("/owners-full-details/{owner_id}", response_model=OwnerReadWithCars)
def read_owner_full_details(*, session: Session = Depends(get_session), owner_id: int):
    # ========================================================================
    #                 _                                _
    #                | |                              | |
    #    ___ ___   __| | ___    __ _  ___   ___  ___  | |__   ___ _ __ ___
    #   / __/ _ \ / _` |/ _ \  / _` |/ _ \ / _ \/ __| | '_ \ / _ \ '__/ _ \
    #  | (_| (_) | (_| |  __/ | (_| | (_) |  __/\__ \ | | | |  __/ | |  __/
    #   \___\___/ \__,_|\___|  \__, |\___/ \___||___/ |_| |_|\___|_|  \___|
    #                           __/ |
    #                          |___/
    # ========================================================================
    pass


# POST http://127.0.0.1:8000/cars/
# Sample request body
# {
#     "plate_number": "HAS-531",
#     "brand": "Toyota",
#     "model": "Vitz",
#     "year": 2012,
#     "owner_id": 1,
# }
@app.post("/cars/", response_model=CarRead)
def create_car(*, session: Session = Depends(get_session), car: CarCreate):
    # ========================================================================
    #                 _                                _
    #                | |                              | |
    #    ___ ___   __| | ___    __ _  ___   ___  ___  | |__   ___ _ __ ___
    #   / __/ _ \ / _` |/ _ \  / _` |/ _ \ / _ \/ __| | '_ \ / _ \ '__/ _ \
    #  | (_| (_) | (_| |  __/ | (_| | (_) |  __/\__ \ | | | |  __/ | |  __/
    #   \___\___/ \__,_|\___|  \__, |\___/ \___||___/ |_| |_|\___|_|  \___|
    #                           __/ |
    #                          |___/
    # ========================================================================
    pass


# GET http://127.0.0.1:8000/cars-full-details/1
# Sample response body
# {
#     "plate_number": "HAS-531",
#     "brand": "Toyota",
#     "model": "Vitz",
#     "year": 2012,
#     "owner_id": 1,
#     "id": 1,
#     "owner": {
#         "first_name": "Mickey",
#         "last_name": "Mouse",
#         "national_id": "SHJDK432432",
#         "id": 1,
#     },
# }
@app.get("/cars-full-details/{car_id}", response_model=CarReadWithOwner)
def read_car_full_details(*, session: Session = Depends(get_session), car_id: int):
    # ========================================================================
    #                 _                                _
    #                | |                              | |
    #    ___ ___   __| | ___    __ _  ___   ___  ___  | |__   ___ _ __ ___
    #   / __/ _ \ / _` |/ _ \  / _` |/ _ \ / _ \/ __| | '_ \ / _ \ '__/ _ \
    #  | (_| (_) | (_| |  __/ | (_| | (_) |  __/\__ \ | | | |  __/ | |  __/
    #   \___\___/ \__,_|\___|  \__, |\___/ \___||___/ |_| |_|\___|_|  \___|
    #                           __/ |
    #                          |___/
    # ========================================================================
    pass


# PATCH http://127.0.0.1:8000/cars/1
# Sample request body
# {
#     "plate_number": "UWB-920"
# }
@app.patch("/cars/{car_id}", response_model=CarRead)
def update_car(
    *, session: Session = Depends(get_session), car_id: int, car: CarUpdate
):
    # ========================================================================
    #                 _                                _
    #                | |                              | |
    #    ___ ___   __| | ___    __ _  ___   ___  ___  | |__   ___ _ __ ___
    #   / __/ _ \ / _` |/ _ \  / _` |/ _ \ / _ \/ __| | '_ \ / _ \ '__/ _ \
    #  | (_| (_) | (_| |  __/ | (_| | (_) |  __/\__ \ | | | |  __/ | |  __/
    #   \___\___/ \__,_|\___|  \__, |\___/ \___||___/ |_| |_|\___|_|  \___|
    #                           __/ |
    #                          |___/
    # ========================================================================
    pass
