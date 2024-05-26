from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional, List
from uuid import UUID, uuid4
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.sql.sqltypes import String as SqlString
from enum import Enum
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, Integer, ForeignKey, Date
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
from .car_model import Car
from datetime import datetime, date

# Set up ORM

class Owner(OrmBase): 
   __tablename__ = "owner"
   
   id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
   last_name: Mapped[str] = mapped_column(String(30))
   first_name: Mapped[str] = mapped_column(String(30))
   middle_name: Mapped[str] = mapped_column(String(30))
   email: Mapped[str] = mapped_column(String(30), unique=True, index=True)
   active: Mapped[bool] = mapped_column(Boolean, default=False)
   created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

   """
   def __init__(self, id, first_name, last_name, middle_name, emp_number, salary, gender, department, roles):
      self.id = id
      self.first_name = first_name
      self.last_name = last_name
      self.middle_name = middle_name
   """

class OwnsCar(OrmBase): 
   __tablename__ = "ownscar"
   
   id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
   owner_id = Column(Integer, ForeignKey('owner.id'))
   car: Mapped[Car] = relationship('Owner')
   car_id = Column(Integer, ForeignKey('car.id'))
   car: Mapped[Car] = relationship('Car')
   colour: Mapped[str] = mapped_column(String(30))
   registration: Mapped[str] = mapped_column(String(30))
   purchased_dt: Mapped[date] = mapped_column(Date)
   created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

"""
class OwnerUpdateRequest(OrmBase):
   __tablename__ = 'owner'
   __table_args__ = {'extend_existing':True}

   id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
   emp_number: Mapped[int] = None
   last_name: Mapped[Optional[str]] = None
   first_name: Mapped[Optional[str]] = None
   middle_name: Mapped[Optional[str]] = None
   email: Mapped[Optional[str]] =  None
"""
