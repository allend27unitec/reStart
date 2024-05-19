from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional, List
from uuid import UUID, uuid4
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, Integer
# from sqlalchemy.sql.sqltypes import String as SqlString
from enum import Enum
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
    declared_attr,
)
from .base_model import OrmBase
from datetime import datetime
from classes.Commission import commission
"""
from classes.Contract import contract
from classes.ContractCommission import contract_commission
from classes.SalariedContract import salaried_contract
from classes.HourlyContract import hourly_contract
from classes.FreelancerContract import freelancer_contract
"""

# Set up ORM

class Employee(OrmBase): 
   __tablename__ = "employee"
   
   id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
   emp_number: Mapped[str] = mapped_column(String(30))
   username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
   last_name: Mapped[str] = mapped_column(String(30))
   first_name: Mapped[str] = mapped_column(String(30))
   middle_name: Mapped[str] = mapped_column(String(30))
   salary: Mapped[int] = mapped_column(BigInteger)
   email: Mapped[str] = mapped_column(String(30), unique=True, index=True)
   hashed_password: Mapped[str] = mapped_column(String(250))
   email_verified_at: Mapped[datetime] = mapped_column(DateTime)
   is_two_factor_auth_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
   active: Mapped[bool] = mapped_column(Boolean, default=False)
   has_verified_email: Mapped[bool] = mapped_column(Boolean, default=False)
   gender: Mapped[int] = mapped_column(Integer)
   roles: Mapped[str] = mapped_column(String(20))
   department: Mapped[int] = mapped_column(Integer)
   created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

   """
   def __init__(self, id, first_name, last_name, middle_name, emp_number, salary, gender, department, roles):
      self.id = id
      self.first_name = first_name
      self.last_name = last_name
      self.middle_name = middle_name
      self.emp_number = emp_number
      self.salary = salary
      self.gender = gender
      self.department = department
      self.roles = roles
   """

   def get_commission(self, sales: int) -> float:
      return commission.calculate_commission(sales)

class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"
    contracter = "contracter"
    manager = "manager"
    team_lead = "team leader"

class Department(str, Enum):
    accounting = "ACCOUNTING"
    research = "RESEARCH"
    sales = "SALES"
    operations = "OPERATIONS"
    development = "DEVELOPMENT"
"""
class EmployeeUpdateRequest(OrmBase):
   __tablename__ = 'employee'
   __table_args__ = {'extend_existing':True}

   id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
   emp_number: Mapped[int] = None
   username: Mapped[Optional[str]] = None
   last_name: Mapped[Optional[str]] = None
   first_name: Mapped[Optional[str]] = None
   middle_name: Mapped[Optional[str]] = None
   salary: Mapped[Optional[int]] = None
   email: Mapped[Optional[str]] =  None
"""
