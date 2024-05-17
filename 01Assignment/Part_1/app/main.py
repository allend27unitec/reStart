import sys
sys.path.append("../../../")
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status
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
from orm.employee_model import Employee, Gender, Role, Department
from orm.base_model import OrmBase
from pydantic import BaseModel

"""
from classes.Commission import commission
from classes.Contract import contract
from classes.ContractCommission import contract_commission
from classes.SalariedContract import salaried_contract
from classes.HourlyContract import hourly_contract
from classes.FreelancerContract import freelancer_contract
"""

app = FastAPI()
# Set up database connection
def create_session():
    try:
        engine = settings.postgresql_engine()
        session_factory = sessionmaker(bind=engine)
        print(f"Postgresql Connection successful")
        return scoped_session(session_factory)
    except Exception as e:
         print(f"Postgresql Connection Exception {e}")

db: List[Employee] = [
    Employee(
    id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    first_name="John",
    last_name="Adams",
    middle_name="",
    emp_number="E7876",
    salary=50000,
    gender=Gender.male,
    department=Department.accounting,
    roles=[Role.admin, Role.user]
    ),
    Employee(
    id=UUID("b11b61d1-537f-469d-aa7a-11617e028506"),
    first_name="Alexa",
    last_name="Jones",
    middle_name='',
    emp_number="E7479",
    salary=45000,
    gender=Gender.female,
    department=Department.research,
    roles=[Role.student, Role.user]
    ),
    Employee(
    id=UUID("b19b51e1-437f-469d-ab7c-227282272806"),
    first_name="Martin",
    last_name="Smith",
    middle_name='',
    emp_number="E7900",
    salary=50000,
    gender=Gender.male,
    department=Department.operations,
    roles=[Role.student, Role.user]
    ),
    Employee(
    id=UUID("b90c04ce-16fc-4615-91d5-a39e3ebdd016"),
    first_name="Steven",
    last_name="King",
    middle_name="",
    emp_number="E7698",
    salary=55000,
    gender=Gender.male,
    department=Department.research,
    roles=[Role.admin]
    )]

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/api/v1/fetch")
async def fetch_users():
    emp: List[Employee] = []
    for user in db:
        commission = user.get_commission(user)
        payWeek = user.calculate_emp_salary(60)
        newUser = user
        newUser.commission = commission
        newUser.payWeek = payWeek
        emp.append(newUser)

    return emp
"""

@app.post("/api/v1/register")
async def register_user(user: Employee):
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
async def update_user(user_update: EmployeeUpdateRequest, user_id: UUID):
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
'''
    # Change the departments of employee1 and employee4
    employee1.assign_department("OPERATIONS")
    employee4.assign_department("SALES")

    # Now calculate the overtime of the employees who are eligible:
    employee2.calculate_salary(45000, 52)
    employee4.calculate_salary(45000, 60)

    print("Updated Employee Details:")
    employee1.print_employee_details()
    employee2.print_employee_details()
    employee3.print_employee_details()
    employee4.print_employee_details()
'''

if __name__ == "__main__":
#    Session = create_session()
    emp = Employee(
    id=UUID("b11b61d1-537f-469d-aa7a-11617e028506"),
    first_name="Alexa",
    last_name="Jones",
    middle_name='',
    emp_number="E7479",
    salary=45000,
    gender=Gender.female,
    department=Department.research,
    roles=[Role.student, Role.user]
    )
    print(emp.get_commission(emp))
    print("user: ", emp.id, emp.full_name, emp.salary, emp.roles,emp.emp_number)
