import sys
sys.path.append("../../01Assignment/Part_1/app")
#sys.path.append("../../01Assignment/Part_1/app/models")
sys.path.append("../../01Assignment/Part_1")
from fastapi.testclient import TestClient
from uuid import UUID
#from employee_model import Employee, Gender, Role, Department
from main import app
import json
import pytest

client: TestClient = TestClient(app)

@pytest.fixture
def test_client():
    yield client
'''
def test_show_main(test_client):
    emp = Employee(
    id=UUID("b11b61d1-537f-469d-aa7a-11617e028506"),
    first_name="Alexa",
    last_name="Jones",
    middle_name='',
    emp_number="E7479",
    salary=4500000,
    gender=Gender.female,
    department=Department.research,
    roles=[Role.student, Role.user]
    )

    request_body = json.dumps(emp.__dict__)
    response = test_client.get("/api/v1/show/{user_id}/", json= request_body)
    assert response.status_code == 200
'''

def test_index_main(test_client):
    response = test_client.get("/api/v1/fetch")
    assert response.status_code == 200
