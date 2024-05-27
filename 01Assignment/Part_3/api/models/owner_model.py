from typing import Optional
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Date, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from .base_model import OrmBase
from .car_model import Car
from datetime import datetime, date

# Set up ORM

class Owner(OrmBase): 
   __tablename__ = "owner"
   __table_args__ = {"sqlite_autoincrement": False}
   
   id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
   last_name: Mapped[str] = mapped_column(String(255))
   first_name: Mapped[str] = mapped_column(String(255))
   middle_name: Mapped[str] = mapped_column(String(255), nullable=True)
   email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
   updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
   created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

class OwnsCar(OrmBase): 
   __tablename__ = "ownscar"
   
   id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
   owner_id = Column(Integer, ForeignKey('owner.id'))
   owner: Mapped[Owner] = relationship('Owner')
   car_id = Column(Integer, ForeignKey('car.id'))
   car: Mapped[Car] = relationship('Car')
   colour: Mapped[str] = mapped_column(String(255))
   vin: Mapped[str] = mapped_column(String(255))  
   purchased_dt: Mapped[date] = mapped_column(Date)
   updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
   created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

class OwnerUpdateRequest(OrmBase):
   __tablename__ = 'owner'
   __table_args__ = {
        'extend_existing':True, 
        }

   last_name: Mapped[Optional[str]]
   first_name: Mapped[Optional[str]]
   middle_name: Mapped[Optional[str]]
   email: Mapped[Optional[str]]
   updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
