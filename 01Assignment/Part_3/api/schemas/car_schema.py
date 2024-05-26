from pydantic import (
        BaseModel as PydanticBase, 
        EmailStr, 
        field_validator, 
        Field, 
        ConfigDict, 
        Discriminator, 
        Tag
        )
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from models.car_model import Car

class BaseModel(PydanticBase):
    class Config:
        model_config = ConfigDict(
            extra='ignore', 
            from_attributes=True,
            arbitrary_types_allowed = True,
            )

class CarBase(BaseModel):
#    model_config = ConfigDict(from_attributes=True)
    id: Optional[UUID] = uuid4()
    make: str 
    model: str
    style: str
    colour: str
    year: str 
    created_at: datetime = Field(default_factory=datetime.now)

class CarCreate(BaseModel):
    pass

class CarUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None

class CarRead(BaseModel):
    id: Optional[UUID] = None
    make: str 
    model: str
    style: str
    colour: str
