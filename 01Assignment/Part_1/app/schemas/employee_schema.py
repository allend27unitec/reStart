from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, validator
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from models.employee_model import Gender, Role, Department

class EmployeeBase(BaseModel):
#    model_config = ConfigDict(from_attributes=True)
    id: Optional[UUID] = uuid4()
    emp_number: str = None
    username: str = None
    first_name: str = None
    last_name: str = None
    middle_name: str = None
    salary: int = None
    email: str = None
    hashed_password: str = None
    email_verified_at: datetime = None
    is_two_factor_auth_enabled: int = None
    active: int = None 
    has_verified_email: int = None
    gender: Gender  = None
    roles: List[Role] = None
    department: Department = None
    created_at: datetime = None

    @validator('salary')
    def min_salary(cls, s):
       if (s < 40000):
           raise ValueError('Salary must be more than 40000')
           return s

    @property
    def full_name(self):
      return f"{self.last_name}, {self.first_name}"

    @full_name.setter
    def full_name(self, value):
      parts = value.split(' ')
      self.first_name = parts[0]
      self.last_name = parts[-1]

    def calculate_emp_salary(self, hours:int | float) -> float:
      base = hours * (self.salary / 2000)
      overtime = 0
      if (hours >= 50):
         overtime = (hours - 50) * (self.salary / 2000)
      return ("{:.2f}".format(base+overtime))

    def get_commission(self, sales: int) -> float:
      return commission.calculate_commission(sales)

    def print_emp_details(self) -> None:
      pass

    def __repr__(self) -> str:
      return f"User(id={self.id!r}, name={self.last_name!r}, {self.first_name!r}"

class EmployeeCreate(BaseModel):
    password: str

class EmployeeUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class EmployeeRead(BaseModel):
    id: Optional[UUID] = None
    emp_number: str = None
    username: Optional[str] = None
    first_name: str = None
    last_name: str = None
    middle_name: Optional[str] = None
    salary: int = 40001
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    email_verified_at: Optional[datetime] = None
    is_two_factor_auth_enabled: Optional[int] = None
    active: Optional[int] = None 
    has_verified_email: Optional[int] = None
    gender: Gender  = None
    roles: List[Role] = None
    department: Department = None
    commission: Optional[str] = None
