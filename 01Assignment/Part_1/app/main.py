import sys
import random
from datetime import datetime
import json
import bcrypt
import difflib    
import aiofiles
import asyncio

from pydantic.errors import PydanticUserError
sys.path.append("../../../") # to pick up project settings
sys.path.append("../") # to pick up functions in parent folder
from typing import Optional, List, Any, Dict
from fastapi import FastAPI, Response, Depends, HTTPException, status, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Json
from sqlalchemy import Column, Integer, String
from threading import get_ident
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)
from uuid import UUID, uuid4
#from project.settings import settings
from models.employee_model import Employee
from schemas.employee_schema import (EmployeeBase, 
                                     EmployeeRead, 
                                     ContractModel, 
                                     EmployeePaymentsDTO, 
                                     EmployeeShort,
                                     EmployeeCreate
                                     )
from dictionaries import convert
from flow_control import print_pattern
from file_handling import format_text_file
from this_list import transform_list
from classes.commission_contract import CommissionContract
from classes.freelancer_contract import FreelancerContract
from classes.hourly_contract import HourlyContract
from classes.no_contract import NoContract
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy import create_engine


app = FastAPI(
    title="Assignment 1 Part 1 ",
    description="Demonstration of Object Orientated Programming with abstract classes, 
    database models and schemas, testing with pytest"
)

def create_session() -> ScopedSession:
    try:
        engine = create_engine("sqlite:///part1.db")
        session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
        print(f"Sqlite Connection successful")
        return scoped_session(session_factory, scopefunc=get_ident)
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
    model_dict = pydantic_model.model_dump()
    return model_class(**model_dict)

class FunctionParams(BaseModel):
    keyList:List[str] = ['a', 'b', 'c']
    valueList: List[int] = [1, 2, 3]
    inputFile: str = '../input.txt'
    outputFile: str = '../output.txt'
    startList: List[str] = ['a','b','c','d','e']

class FlatFileUpload:
    def __init__(self, filename: str):
        self.filename = filename
        self.file: Optional[aiofiles.threadpool.binary.AsyncBufferedIOBase] = None

    async def __aenter__(self):
        self.file = await aiofiles.open(self.filename, mode='rb')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.file.close()

    async def read(self, size: int = -1):
        return await self.file.read(size)

    async def write(self, data):
        await self.file.write(data)

    async def seek(self, offset: int, whence: int = 0):
        await self.file.seek(offset, whence)

    async def close(self):
        await self.file.close()

@app.get("/")
async def root():
    return {"Hello": "Part 1"}

@app.get("/api/v1/employees", response_model=List[EmployeeRead])
async def get_all_employee(skip: int = 0, limit: int = 20, db: ScopedSession = Depends(get_db)) -> Any:
    sa_employees = db.query(Employee).offset(skip).limit(limit).all()
    employees: List[EmployeeRead] = []
    for emp in sa_employees:
        employees.append(to_pydantic(emp, EmployeeRead))
    return employees 

@app.post("/api/v1/register", status_code=status.HTTP_201_CREATED, response_model=EmployeeBase)
async def register_employee(employee: EmployeeBase, db: ScopedSession = Depends(get_db)) -> Any:
#async def register_employee(employee: EmployeeBase):
    sa_employee = from_pydantic(employee, Employee)
    contract = employee.contract_type 
    new_employee = to_pydantic(sa_employee, EmployeeBase)
    password = b'password'
    salt = bcrypt.gensalt()
    hpass = bcrypt.hashpw(password, salt)
    new_employee.hashed_password = str(hpass)
    sa_employee.hashed_password = str(hpass)
    db.add(sa_employee)
    db.commit()
    #contract_type = json.dumps(contract)
    return new_employee

@app.get("/api/v1/payments", response_model=List[EmployeePaymentsDTO])
async def get_employee_payments(skip: int = 0, limit: int = 20, db: ScopedSession = Depends(get_db)) -> Any:
    sa_employees = db.query(Employee).offset(skip).limit(limit).all()
    employees: List[EmployeePaymentsDTO] = []
    for emp in sa_employees:
        employee = to_pydantic(emp, EmployeeShort)
        c:ContractModel = employee.contract_type 
        contract = c.model_dump(mode='json')
        '''
        refactored from the original str to model
        #contract = json.loads(contract)
        #contract = {"contract": contract}
        #print(f"json loaded contract {contract}")
        #print(f"attribute value {employee.contract_type}")
        #    employee = employee.model_dump(exclude={'contract_type'})
        '''
        temp = ContractModel(**contract).execute_contract().get_payment()
        payment = f"${temp/100:,.2f}"
        ctype = ContractModel(**contract).execute_contract().contract_type()
        employees.append(EmployeePaymentsDTO(employee=employee, payment=payment, contract_type=ctype))
        
    return employees

@app.get("/api/v1/employee/{employee_id}", response_model=EmployeePaymentsDTO)
async def get_employee(employee_id:UUID, db: ScopedSession = Depends(get_db)) -> Any:
    sa_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if sa_employee is None:
        print(f"couldn't find {employee_id} - will try sequential search")
        #raise HTTPException(status_code=404,
        #                    detail="Employee not found")
        sa_employees = db.query(Employee).offset(0).limit(25).all()
        found=None
        for sa_employee in sa_employees:
            print(f"comparing {sa_employee.id} to {employee_id}")
            if (sa_employee.id == employee_id):
                print(f"found it")
                found = sa_employee
                break
        if (found == None):
                raise HTTPException(status_code=404,
                                    detail="Employee not found")
    employee = to_pydantic(sa_employee, EmployeeShort)
    c:ContractModel = employee.contract_type 
    contract = c.model_dump(mode='json')
    temp = ContractModel(**contract).execute_contract().get_payment()
    payment = f"${temp/100:,.2f}"
    ctype = ContractModel(**contract).execute_contract().contract_type()
    emp_dto = EmployeePaymentsDTO(employee=employee, payment=payment, contract_type=ctype)
    #print(emp_dto.model_dump())
    #return emp_dto.model_dump()
    return emp_dto 

@app.post("/api/v2/dictionaries", response_class=Response)
async def convert_dict(params: FunctionParams) -> Any:
    result = json.dumps(convert(params.keyList, params.valueList))
    return Response(content=result, media_type="application/json")

@app.post("/api/v2/flowcontrol", response_class=Response)
async def flowcontrol() -> Any:
    pp1 = print_pattern(4)
    pp2 = print_pattern(1)
    result = pp1 + pp2
    return Response(content=result, media_type="text/html")

@app.post("/api/v2/uploadfile")
async def createfile(file: UploadFile):
    return {"filename": file.filename}

@app.post("/api/v2/thislist")
async def transformlist(params: FunctionParams) -> Any:
    result = json.dumps(transform_list(params.startList))
    #  return {"result": result}
    return Response(content=result, media_type="application/json")

@app.post("/api/v2/filehandling", response_class=Response)
async def filehandle(params: FunctionParams) -> Any:
    asyncio.create_task(format_text_file(params.inputFile, params.outputFile))
    """
    tried the following but does not support async context manager protocol:
    async with open(params.inputFile, 'r') as f:
        c1 = f.readlines()
    async with open(params.outputFile, 'r') as f:
        c2 = f.readlines()
    """
    async with FlatFileUpload(params.inputFile) as file1, FlatFileUpload(params.outputFile) as file2:
        c1 = await file1.read()
        c2 = await file2.read()
    t1 = c1.decode('utf-8')
    t2 = c2.decode('utf-8')
    diff = difflib.unified_diff(t1.splitlines(), t2.splitlines(), lineterm='')
    result = '\n'.join(diff)
    return Response(content=result, media_type="text/html")

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
    #    ScopedSession = create_session()
    emp = Employee(
        id=UUID("b11b61d1-537f-469d-aa7a-11617e028506"),
        first_name="Alexa",
        last_name="Jones",
        middle_name='',
        emp_number="E7479",
        salary=45000,
    )
    print("user: ", emp.id, emp.full_name, emp.salary, emp.roles,emp.emp_number)
