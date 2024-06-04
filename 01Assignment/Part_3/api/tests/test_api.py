import pytest
import requests
import sys
sys.path.append("../") 
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from main import app, create_session, get_db
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from models.owner_model import Owner
from models.base_model import OrmBase
from schemas.owner_schema import (OwnerBase, 
                                     OwnerRead, 
                                     OwnerWithCarsDTO, 
                                     OwnerCreateDTO
                                     )
from schemas.car_schema import (CarBase, 
                                CarRead, 
                                CarWithOwnersDTO, 
                                CarCreate
                                )
API_URL = "http://localhost:8000"
client = TestClient(app)
engine = create_engine("sqlite:///test.db",
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool,
                       )
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
OrmBase.metadata.create_all(bind=engine)

# Dependency override for testing
def override_get_db():
    db = TestingSessionLocal()
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
    response = test_client.post("/api/v1/carregister/", json=payload)
    print(response)
    assert response.status_code == 422
    car = CarRead.model_validate(response.json())
    #assert car.make == "Volkswagen"
'''
    response = test_client.post("/api/v1/carregister/", json=payload1)
    #assert response.status_code == 201
    car = CarRead.model_validate(response.json())
    #assert car.make == "MINI"


def test_create_owner(test_client):
    payload = {
    "id": 18,
    "first_name": "Ynes",
    "last_name": "Gannaway",
    "middle_name": "Copcutt",
    "email": "ycopcuttn1@ebay.com",
    "updated_at": None,
    "created_at": None
    "cars": []
    }
    payload1 = {
    "id": 9,
    "first_name": "Antonio",
    "last_name": "McVeigh",
    "middle_name": "Calverd",
    "email": "acalverd36@homestead.com",
    "updated_at": None,
    "created_at": None
    "cars": [ 
        {
        "id": 1,
        "owner_id": 9,
        "car_id": 1,
        "colour": "Turquoise",
        "vin": "NL28 PWRY 1286 7416 98",
        "plate_number": "KFD67463",
        "purchased_dt": "1991-02-05",
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

def test_get_owners(test_client):
    response = test_client.get("/api/v1/owners/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_specific_owner(test_client):
    response = test_client.post("/api/v1/register/", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "middle_name": "B",
        "emp_number": "E5678",
        "salary": 7000000,
        "contract_type": "{'ctype':'freelancer':, 'rate': 8000, 'hours':60}"
    })
    emp_id = response.json()["id"]
    print(response.json())
    
    response = test_client.get(f"/api/v1/owners/{emp_id}")
    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"

def test_update_owner(test_client):
    response = test_client.post("/api/v1/owners/", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "middle_name": "C",
        "emp_number": "E91011",
        "salary": 50000,
    })
    emp_id = response.json()["id"]
    
    response = test_client.patch(f"/api/v1/owners/{emp_id}", json={
        "salary": 55000,
    })
    assert response.status_code == 200
    assert response.json()["salary"] == 55000

def test_delete_owner(test_client):
    response = test_client.post("/api/v1/owners/", json={
        "first_name": "Bob",
        "last_name": "Brown",
        "middle_name": "D",
        "emp_number": "E121314",
        "salary": 45000,
    })
    emp_id = response.json()["id"]
    
    response = test_client.delete(f"/api/v1/owners/{emp_id}")
    assert response.status_code == 200
    assert response.json() == {"deleted user": emp_id}

'''
