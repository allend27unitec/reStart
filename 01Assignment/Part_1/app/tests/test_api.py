import pytest
import requests
import sys
sys.path.append("../../") # to pick up functions in parent folder
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from app.main import app, create_session, get_db
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from app.models.employee_model import Employee
from app.models.base_model import OrmBase
from app.schemas.employee_schema import (EmployeeBase, 
                                     EmployeeRead, 
                                     ContractModel, 
                                     EmployeePaymentsDTO, 
                                     EmployeeShort,
                                     EmployeeCreate, SalariedModel
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
   
def test_create_employee(test_client):

    payload = {
    "id": "0e7d1fdd-a860-41e6-b9b2-e06b57ccee97",
    "emp_number": "LBP3147",
    "username": "LBPopplewell",
    "first_name": "Lars",
    "last_name": "Popplewell",
    "middle_name": "Burrage",
    "salary": 12667700,
    "email": "lburraged5@loc.gov",
    "hashed_password": "",
    "contract_type": {"contract": {"ctype": "salaried", "salary": 253354, "hours": 60}},
    "updated_at": "2022-12-26 17:36:22",
    "created_at": "2018-12-10 19:06:34"
    }

    response = test_client.post("/api/v1/register/", json=payload)
    data = response.json()

    assert response.status_code == 201
    employee = EmployeeBase.model_validate(response.json())
    c:ContractModel = employee.contract_type 
    contract = c.model_dump(mode='json')
    pay = ContractModel(**contract).execute_contract().get_payment()
    ctype = ContractModel(**contract).execute_contract().contract_type()
    assert isinstance(c, ContractModel)
    assert pay == 304024
    assert ctype == "Salaried Contract"
    assert data['emp_number'] == 'LBP3147'


def test_get_employees(test_client):
    response = test_client.get("/api/v1/employees/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

'''
def test_get_specific_employee(test_client):
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
    
    response = test_client.get(f"/api/v1/employees/{emp_id}")
    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"

def test_update_employee(test_client):
    response = test_client.post("/api/v1/employees/", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "middle_name": "C",
        "emp_number": "E91011",
        "salary": 50000,
    })
    emp_id = response.json()["id"]
    
    response = test_client.patch(f"/api/v1/employees/{emp_id}", json={
        "salary": 55000,
    })
    assert response.status_code == 200
    assert response.json()["salary"] == 55000

def test_delete_employee(test_client):
    response = test_client.post("/api/v1/employees/", json={
        "first_name": "Bob",
        "last_name": "Brown",
        "middle_name": "D",
        "emp_number": "E121314",
        "salary": 45000,
    })
    emp_id = response.json()["id"]
    
    response = test_client.delete(f"/api/v1/employees/{emp_id}")
    assert response.status_code == 200
    assert response.json() == {"deleted user": emp_id}

'''
