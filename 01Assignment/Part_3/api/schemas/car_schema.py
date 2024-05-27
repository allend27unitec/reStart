from pydantic import (
        BaseModel as PydanticBase, 
        Field, 
        ConfigDict 
        )
from typing import Optional
from datetime import datetime

class BaseModel(PydanticBase):
    class Config:
        model_config = ConfigDict(
            extra='ignore', 
            from_attributes=True,
            arbitrary_types_allowed = True,
            )

class CarBase(BaseModel):
#    model_config = ConfigDict(from_attributes=True)
    id: Optional[int]
    make: str 
    model: str
    style: str
    year: str 
    updated_at: datetime
    created_at: datetime

class CarCreate(BaseModel):
    pass

class CarUpdate(BaseModel):
    make: Optional[str]
    model: Optional[str]
    updated_at: datetime

class CarRead(BaseModel):
    id: Optional[int] = None
    make: Optional[str]
    model: Optional[str]
    style: str
    year: Optional[str]
