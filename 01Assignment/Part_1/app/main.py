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
from models.employee_model import Employee, Gender, Role, Department
from models.base_model import OrmBase
from schemas.employee_schema import EmployeeCreate, EmployeeRead, EmployeeUpdate
from dictionaries import convert

app = FastAPI(
    title="Assignment 1 Part 1 ",
    description="Demonstration of Object Orientated Programming and modular class structure"
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
    roles=[Role.admin, Role.user, Role.team_lead]
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
    roles=[Role.contracter, Role.user]
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
    roles=[Role.manager]
    )]

class FunctionParams(BaseModel):
    KeyList:Optional[List[str]] = ['a', 'b', 'c']
    ValueList: Optional[List[int]] = [1, 2, 3]
    p1: Optional[int]
    p2: Optional[str]

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/api/v1/fetch", response_model=List[EmployeeRead])
async def fetch_users() -> Any:
    emp: List[EmployeeRead] = []
    for user in db:
        sales: int = random.randrange(1000,10000)  # simulate sales
        workHours = random.randrange(20, 80)  # simulate weekly hours worked
        newUser = to_pydantic(user, EmployeeRead)
        """
        print("User dump")
        try:
           print(newUser.model_json_schema())
        except PyudanticUserError as e:
            print(e)
        print(newUser.model_dump())
        print(EmployeeRead.model_validate(newUser))
        print
        """
        commission = user.get_commission(sales)
   #     payWeek = newUser.calculate_emp_salary(workHours)
        newUser.commission = commission
  #      newUser.payWeek = payWeek
        emp.append(newUser)

    return emp

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
async def register_user(user: EmployeeCreate) -> Employee:
    db.append(user)
    return {"registered id": user.id}

@app.post("/api/v2/dictionaries", response_model=Dict)
async def convert_dict(params: FunctionParams) -> str:
    result: Dict[str, int] = convert(params.KeyList, params.ValueList)
    result = "Dictionary from associated key/value lists: "+ str(result)
    return {"result": result}
"""
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
