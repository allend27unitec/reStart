from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional, List
from uuid import UUID, uuid4
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, BigInteger, String, DateTime, Date, Boolean, Integer
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
from datetime import datetime, date

# Set up ORM

class Car(OrmBase): 
    __tablename__ = "car"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    make: Mapped[str] = mapped_column(String(30))
    model: Mapped[str] = mapped_column(String(30))
    style: Mapped[str] = mapped_column(String(30))
    colour: Mapped[str] = mapped_column(String(30))
    year: Mapped[date] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class CarUpdateRequest(OrmBase):
    __tablename__ = 'car'
    __table_args__ = {'extend_existing':True}

    make: Mapped[Optional[str]] = None
    model: Mapped[Optional[str]] = None
    style: Mapped[Optional[str]] = None
    colour: Mapped[Optional[str]] = None
    year: Mapped[Optional[str]] = None
