from pydantic import BaseModel, ConfigDict, validator, EmailStr,Field
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime, date
from models.owner_model import Owner, OwnsCar

class OwnerBase(BaseModel):
#    model_config = ConfigDict(from_attributes=True)
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name: str
    email: EmailStr
    email_verified_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)

    @property
    def full_name(self):
      return f"{self.last_name}, {self.first_name}"

    @full_name.setter
    def full_name(self, value):
      parts = value.split(' ')
      self.first_name = parts[0]
      self.last_name = parts[-1]

    def __repr__(self) -> str:
      return f"User(id={self.id!r}, name={self.last_name!r}, {self.first_name!r}"

class OwnsCar(BaseModel): 
   
    id: Optional[UUID] = uuid4()
    owner_id: Optional[UUID] = None 
    car_id: Optional[UUID] = None 
    colour: str 
    registration: str
    purchased_dt: date 

class OwnerWithCarsDTO(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str] 
    email: str 
    cars: List[OwnsCar]

class OwnerCreate(BaseModel):
    password: str

class OwnerUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class OwnerRead(BaseModel):
    id: Optional[UUID] = None
    first_name: str 
    last_name: str
    middle_name: Optional[str] = None
    email: Optional[str] = None
