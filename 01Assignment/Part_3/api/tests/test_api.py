import pytest
import requests
import sys
sys.path.append("../") 
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from main import app, create_session, get_db
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.owner_model import Owner
from models.base_model import OrmBase
from schemas.owner_schema import (OwnerBase, 
                                     OwnerRead, 
                                     OwnerWithCarsDTO, 
                                     UpdateCar
                                     )
from schemas.car_schema import (CarBase, 
                                CarRead, 
                                CarWithOwnersDTO, 
                                CarCreate
                                )
API_URL = "http://localhost:8000"
client = TestClient(app)

def create_session() -> Session:
    try:
        engine = create_engine("sqlite:///test.db",
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool,
                       )
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        OrmBase.metadata.create_all(bind=engine)
        print(f"Sqlite Connection successful")
        return TestingSessionLocal()
    except Exception as e:
         print(f"Sqlite Connection Exception {e}")
# Dependency override for testing
def override_get_db():
  #  db = TestingSessionLocal()
    db = create_session()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client

def test_url():
    response = requests.get(API_URL)
    assert response.status_code == 200

def test_create_car(test_client):
    payload = {
    "id": 1,
    "make": "Volkswagen",
    "model": "Type 2",
    "style": "convertible",
    "year": "1989",
    "updated_at": None,
    "created_at": None
    }
    payload1 = {
    "id": 2,
    "make": "MINI",
    "model": "Cooper",
    "style": "EV",
    "year": "2012",
    "updated_at": None,
    "created_at": None 
    }
    payload2 = {
    "id": 3,
    "make": "Dodge",
    "model": "Caliber",
    "style": "EV",
    "year": "2009",
    "updated_at": "2022-12-08 01:45:15",
    "created_at": "2015-12-26 16:32:53"
  }
    response = test_client.post("/api/v1/carregister/", json=payload)
    assert response.status_code == 201
    car = CarBase.model_validate(response.json())
    assert car.make == "Volkswagen"
    response = test_client.post("/api/v1/carregister/", json=payload1)
    assert response.status_code == 201
    car = CarBase.model_validate(response.json())
    assert car.make == "MINI"
    response = test_client.post("/api/v1/carregister/", json=payload2)
    assert response.status_code == 201
    car = CarBase.model_validate(response.json())
    assert car.make == "Dodge"

def test_create_owner(test_client):
    payload = {
    "id": 6,
    "first_name": "Ynes",
    "last_name": "Gannaway",
    "middle_name": "Copcutt",
    "email": "ycopcuttn1@ebay.com",
    "updated_at": None,
    "created_at": None,
    "cars": []
    }
    payload1 = {
    "id": 9,
    "first_name": "Antonio",
    "last_name": "McVeigh",
    "middle_name": "Calverd",
    "email": "acalverd36@homestead.com",
    "updated_at": None,
    "created_at": None,
    "cars": [ 
        {
        "id": 1,
        "owner_id": 9,
        "car_id": 2,
        "colour": "Turquoise",
        "vin": "NL28 PWRY 1286 7416 98",
        "plate_number": "KFD67463",
        "purchased_dt": "1991-02-05",
        "updated_at": None,
        "created_at": None,
        }
	  ]
    } 
    payload2 = {
    "id": 12,
    "first_name": "Burgess",
    "last_name": "Huckster",
    "middle_name": "Bussons",
    "email": "bbossons@ocn.com",
    "updated_at": None,
    "created_at": None,
    "cars": [ 
        {
        "id": 2,
        "owner_id": 12,
        "car_id": 3,
        "colour": "Red",
        "vin": "NL28 PWRY 1286 7416 98",
        "plate_number": "KJFE7438",
        "purchased_dt": "2021-02-05",
        "updated_at": None,
        "created_at": None,
        },
        {
        "id": 3,
        "owner_id": 12,
        "car_id": 1,
        "colour": "Violet",
        "vin": "NL28 PWRY 9847 9834 44",
        "plate_number": "KJFE7438",
        "purchased_dt": "2000-12-12",
        "updated_at": None,
        "created_at": None,
        }
	  ]
   } 

    response = test_client.post("/api/v1/register/", json=payload)
    assert response.status_code == 201
    ownerDTO = OwnerWithCarsDTO.model_validate(response.json())
    owner: OwnerRead = ownerDTO.owner
    cars = ownerDTO.cars
    assert owner.last_name == "Gannaway"
    assert isinstance(owner, OwnerRead)
    assert isinstance(cars, list)

    response = test_client.post("/api/v1/register/", json=payload1)
    assert response.status_code == 201
    ownerDTO = OwnerWithCarsDTO.model_validate(response.json())
    owner: OwnerRead = ownerDTO.owner
    cars = ownerDTO.cars
    assert owner.last_name == "McVeigh"
    assert isinstance(owner, OwnerRead)
    assert isinstance(cars, list)

    response = test_client.post("/api/v1/register/", json=payload2)
    assert response.status_code == 201
    ownerDTO = OwnerWithCarsDTO.model_validate(response.json())
    owner: OwnerRead = ownerDTO.owner
    cars = ownerDTO.cars
    assert owner.last_name == "Huckster"
    assert isinstance(owner, OwnerRead)
    assert isinstance(cars, list)

def test_get_owners(test_client):
    response = test_client.get("/api/v1/owners/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_specific_owner(test_client):
    payload = 6    
    response = test_client.get(f"/api/v1/owners-full-details{payload}")
    assert response.status_code == 200
    payload = 9    
    response = test_client.get(f"/api/v1/owners-full-details{payload}")
    assert response.status_code == 200

def test_update_car(test_client):
    payload = {"plate_number": "new plate"}
    response = test_client.patch(f"/api/v1/ownscar/3", json=payload)
    assert response.status_code == 206
    ownscar = UpdateCar.model_validate(response.json())
    assert ownscar.plate_number ==  "new plate"

def test_delete_owner(test_client):
    payload = 6
    response = test_client.delete(f"{API_URL}/api/v1/deleteowner/{payload}")
    assert response.status_code == 204

