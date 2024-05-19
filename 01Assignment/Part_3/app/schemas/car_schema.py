from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, validator
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from models.car_model import Car

class CarBase(BaseModel):
#    model_config = ConfigDict(from_attributes=True)
    id: Optional[UUID] = uuid4()
    make: str = None
    model: str = None
    style: str = None
    colour: str = None
    year: str = None
    created_at: datetime = None

class CarCreate(BaseModel):
    pass

class CarUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None

class CarRead(BaseModel):
    id: Optional[UUID] = None
    make: str = None
    model: str = None
    style: str = None
    colour: str = None
