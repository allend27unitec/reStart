from pydantic import BaseModel, EmailStr,Field
from typing import Optional, List
from datetime import datetime, date
from models.owner_model import Owner, OwnsCar

class OwnerBase(BaseModel):
#    model_config = ConfigDict(from_attributes=True)
    id: Optional[int]
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
   
    id: Optional[int]
    owner_id: Optional[int] = None 
    car_id: Optional[int] = None 
    colour: str 
    registration: str
    purchased_dt: date 

class OwnerWithCarsDTO(BaseModel):
    # this DTO breaks normalisation rules for the convenience of a list of cars
    id: Optional[int] 
    first_name: str
    last_name: str
    middle_name: Optional[str] 
    email: str 
    cars: List[OwnsCar]

class OwnerCreateDTO(BaseModel):
    id: int 
    first_name: str
    last_name: str
    middle_name: Optional[str] 
    email: str 
    cars: List[OwnsCar]

class OwnerUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class OwnerRead(BaseModel):
    first_name: str 
    last_name: str
    middle_name: Optional[str] = None
    email: Optional[str] = None
