from typing import Optional
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from .base_model import OrmBase
from datetime import datetime, date

# Set up ORM

class Car(OrmBase): 
    __tablename__ = "car"
    __table_args__ = {"sqlite_autoincrement": False}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    make: Mapped[str] = mapped_column(String(255))
    model: Mapped[str] = mapped_column(String(255))
    style: Mapped[str] = mapped_column(String(255))
    year: Mapped[str] = mapped_column(String(4))  # model year
    # updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    # created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime)
    created_at: Mapped[str] = mapped_column(DateTime)

class CarUpdateRequest(OrmBase):
    __tablename__ = 'car'
    __table_args__ = {'extend_existing':True}

    make: Mapped[Optional[str]] 
    model: Mapped[Optional[str]]
    style: Mapped[Optional[str]]
    year: Mapped[Optional[str]]
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

