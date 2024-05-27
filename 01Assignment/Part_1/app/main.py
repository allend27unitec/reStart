import sys
import random
from datetime import datetime
import json
import difflib    
import aiofiles
import asyncio
sys.path.append("../../../") # to pick up project settings
sys.path.append("../") # to pick up functions in parent folder
from typing import Optional, List, Any, Dict
from fastapi import FastAPI, Response, Depends, HTTPException, status, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import (
    Session,
    sessionmaker,
    scoped_session,
)
from uuid import UUID, uuid4
#from project.settings import settings
from models.employee_model import Employee, Gender, Role, Department
from schemas.employee_schema import EmployeeRead, ContractModel
from dictionaries import convert
from flow_control import print_pattern
from file_handling import format_text_file
from this_list import transform_list
from classes.commission_contract import CommissionContract
from classes.freelancer_contract import FreelancerContract
from classes.hourly_contract import HourlyContract
from classes.no_contract import NoContract


app = FastAPI(
    title="Assignment 1 Part 1 ",
    description="Demonstration of Object Orientated Programming and modular class structure"
)
"""
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
"""

def to_pydantic(model_instance, pydantic_model):
    model_dict = {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}
    return pydantic_model(**model_dict)

def from_pydantic(pydantic_model, model_class):
    model_dict = pydantic_model.dict(exclude_unset=True)
    return model_class(**model_dict)

db: List[Employee] = [
    Employee(
        id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
        username="ja",
        first_name="John",
        last_name="Adams",
        middle_name="",
        emp_number="E7876",
        salary=5000000,
        email="ja@gmail.com",
        gender=Gender.male,
        department=Department.accounting,
        roles=[Role.admin, Role.user, Role.team_lead],
        contract_type=ContractModel,   # CommissionContract(num_contracts=12, commission=17),
        contract_data=json.dumps({'type':'freelancer','rate':5000, 'hours':100}),
        created_at = datetime.now
    )]
'''
    Employee(
        id=UUID("b11b61d1-537f-469d-aa7a-11617e028506"),
        username="aj",
        first_name="Alexa",
        last_name="Jones",
        middle_name='',
        emp_number="E7479",
        salary=4500000,
        email="aj@gmail.com",
        gender=Gender.female,
        department=Department.research,
        roles=[Role.contracter, Role.user],
        # contract=FreelancerContract(rate=8000, hours=40)
    ),
    Employee(
        id=UUID("b19b51e1-437f-469d-ab7c-227282272806"),
        username="ms",
        first_name="Martin",
        last_name="Smith",
        middle_name='',
        emp_number="E7900",
        salary=6500000,
        email="ma@gmail.com",
        gender=Gender.male,
        department=Department.operations,
        roles=[Role.student, Role.user],
        # contract=HourlyContract(rate=4500, hours=76, overhead=7650)
    ),
    Employee(
        id=UUID("b90c04ce-16fc-4615-91d5-a39e3ebdd016"),
        username="sk",
        first_name="Steven",
        last_name="King",
        middle_name="",
        emp_number="E7698",
        salary=4900000,
        email="sk@gmail.com",
        gender=Gender.male,
        department=Department.research,
        roles=[Role.manager],
        # contract=NoContract()
    )]
  '''

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
    return {"Hello": "World"}

@app.get("/api/v1/fetch", response_model=EmployeeRead)
async def fetch_users() -> Any:
    emp: List[EmployeeRead] = []
    for user in db:
        contracts: int = random.randrange(105,1500)  # simulate contracts
        rate: int = random.randrange(15,35)  # simulate contracts

        workHours = random.randrange(20, 80)  # simulate weekly hours worked
        newUser = to_pydantic(user, EmployeeRead)
        """
        print("User dump")
        try:
           print(newUser.model_json_schema())
        except PyudanticUserError as e:
            print(e)
        print(EmployeeRead.model_validate(newUser))
        print
        """
        # print(newUser.model_dump())
        # contract = user.contract
        # print(contract)
        # payment = user.contract.get_payment()
        #     payWeek = newUser.calculate_emp_salary(workHours)
        # newUser.payment=[]
        # newUser.payment.extend((str(contract), f"{payment/100:.2f}"))
        #      newUser.payWeek = payWeek
        # newUser.payment = f"{payment/100:.2f}"
        emp.append(newUser)

    return emp
'''
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
async def register_user(user: Employee) -> Dict:
    db.append(user)
    return {"registered id": user.id}
'''
@app.post("/api/v2/dictionaries", response_class=Response)
async def convert_dict(params: FunctionParams) -> str:
    result: Dict[str, int] = convert(params.keyList, params.valueList)
    result =  lists: "+ str(result)
    return Response(content=result, media_type="text/html")

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
    print("user: ", emp.id, emp.full_name, emp.salary, emp.roles,emp.emp_number)
