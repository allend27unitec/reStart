from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional, List
from uuid import UUID, uuid4
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Boolean, Integer, ForeignKey
# from sqlalchemy.sql.sqltypes import String as SqlString
from enum import Enum
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
    sessionmaker,
    declared_attr,
)
from sqlalchemy.ext.declarative import AbstractConcreteBase
from .base_model import OrmBase
from datetime import datetime
from classes.contract import Contract
from classes.commission_contract import CommissionContract

# Set up ORM

Base = declarative_base()

class Employee(OrmBase): 
    __tablename__ = "employee"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    emp_number: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    last_name: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[str] = mapped_column(String(255), nullable=True)
    salary: Mapped[int] = mapped_column(BigInteger, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=True)
    email_verified_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_two_factor_auth_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    has_verified_email: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    gender: Mapped[int] = mapped_column(Integer, nullable=True)
    roles: Mapped[str] = mapped_column(String(255), nullable=True)
    department: Mapped[int] = mapped_column(Integer, nullable=True)
    # contract_id = Column(Integer, ForeignKey('emp_contract.id'), nullable=True)
    # contract: Mapped[Contract] = relationship('EmploymentContract')
    contract_type: Mapped[str] = mapped_column(String, nullable=True) # the type of contract
    contract_data: Mapped[str] = mapped_column(String, nullable=True) # JSON or some other serialized format of the contract
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

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
'''
    def compute_pay(self) -> int:
        payout = self.contract.get_payment()
        if self.commission is not None:
            payout += self.commission.get_payment()
        return payout
'''

class EmploymentContract(OrmBase):
    __tablename__ = "emp_contract"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)


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
