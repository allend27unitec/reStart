import abc
from pydantic import (
        BaseModel as PydanticBase, 
        EmailStr, 
        field_validator, 
        Field, 
        ConfigDict, 
        Discriminator, 
        Tag,
        Json
        )
from typing import Optional, List, Union, Literal, Any
from typing_extensions import Annotated
from uuid import UUID, uuid4
from datetime import datetime
from models.employee_model import Gender, Role, Department
from classes.contract import Contract
from classes.commission_contract import CommissionContract
from classes.freelancer_contract import FreelancerContract
#from classes.hourly_contract import HourlyContract
#from classes.salaried_contract import SalariedContract
#from classes.no_contract import NoContract

class BaseModel(PydanticBase):
    class Config:
        model_config = ConfigDict(
            extra='ignore', 
            from_attributes=True,
            arbitrary_types_allowed = True,
            )

def contract_discriminator(c: str) -> str:
    print(f"c is {c}")
    if (not isinstance(c, (dict, Contract))):
        raise ValueError("Invalid contract type: ", c)
    return 'ok'

class EmployeeCreate(BaseModel):
    password: str

class EmployeeUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class EmploymentModel(BaseModel):
    id: int 
    name: str 
    description: str 

class FreelancerModel(BaseModel):
    type: Literal['freelancer']
    rate: int
    hours: int

    def to_contract(self):
        return FreelancerContract(rate=self.rate, hours=self.hours)
    
class CommissionModel(BaseModel):
    type: Literal['commission']
    rate: int
    hours: int

    def to_contract(self):
        return CommissionContract(commission=self.rate, num_contracts=self.hours)

ContractModel = Union[FreelancerModel, CommissionModel]

class EmployeeBase(BaseModel, abc.ABC):
    id: UUID = Field(default_factory=uuid4, frozen=True)
    emp_number: str
    username: str 
    first_name: str 
    last_name: str  
    middle_name: str
    salary: int = Field(gt=4000000, description="Salary must be more than $40,000")
    email: EmailStr
    hashed_password: str
    email_verified_at: datetime = Field(default_factory=datetime.now)
    is_two_factor_auth_enabled: bool
    active: int
    has_verified_email: bool
    gender: Gender
    roles: List[Role] 
    department: Department
    contract_type: ContractModel = Field(..., discriminator='type')
    contract_data: Json
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator('salary')
    def min_salary(cls, s:int):
       if (s < 4000000):
           raise ValueError('Salary must be more than 40000')
       return s


    @property
    def full_name(self):
      return f"{self.last_name}, {self.first_name}"

    @full_name.setter
    def full_name(self, value):
      parts = value.split(' ')
      self.first_name = parts[0]
      self.last_name = parts[-1]

    def calculate_emp_salary(self, hours:int | float) -> str:
      base = hours * (self.salary / 2000)
      overtime = 0
      if (hours >= 50):
            overtime = (hours - 50) * (self.salary / 2000)
      return (f"{base+overtime:.2f}")

    def print_emp_details(self) -> None:
      pass

    def __repr__(self) -> str:
      return f"User(id={self.id!r}, name={self.last_name!r}, {self.first_name!r}"

class EmployeeRead(BaseModel):
    id: Optional[UUID] 
    emp_number: Optional[str]
    username: Optional[str] 
    first_name: Optional[str]
    last_name: Optional[str ]
    middle_name: Optional[str] 
    salary: Optional[int] 
    email: Optional[str] 
    hashed_password: Optional[str] = None
    email_verified_at: Optional[datetime] = None
    is_two_factor_auth_enabled: Optional[int] = None
    active: Optional[int] = None 
    has_verified_email: Optional[int] = None
    gender: Optional[Gender] 
    roles: Optional[List[Role]]
    department: Optional[Department]
    # contract_id: Optional[int]
    # contract: Optional[EmploymentContract]
    contract_type: ContractModel = Field(..., discriminator='type')
    contract_data: Json


'''
     Annotated[
        Union[
            Annotated['CommissionContract', Tag('ok')], 
            Annotated['HourlyContract', Tag('ok')],
            Annotated['FreelancerContract', Tag('ok')],
            Annotated['SalariedContract',Tag('ok')], 
            Annotated['NoContract',Tag('ok')], 
        ],
        Discriminator(contract_discriminator),
    ]
'''
