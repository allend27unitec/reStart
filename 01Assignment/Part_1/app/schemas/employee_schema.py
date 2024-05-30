import abc
from pydantic import (
        BaseModel as PydanticBase, 
        EmailStr,
        computed_field, 
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
from classes.contract import Contract
from classes.commission_contract import CommissionContract
from classes.freelancer_contract import FreelancerContract
from classes.hourly_contract import HourlyContract
from classes.salaried_contract import SalariedContract
from classes.no_contract import NoContract

class BaseModel(PydanticBase):
    class Config:
        model_config = ConfigDict(
            extra='ignore', 
            from_attributes=True,
            arbitrary_types_allowed = True,
            )

def contract_discriminator(c: str) -> str:
    print(f"Discriminator c is {c}")
    if (not isinstance(c, (dict, Contract))):
        raise ValueError("Invalid contract type: ", c)
    return c

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
    ctype: Literal['freelancer']
    rate: int
    hours: int

    def to_contract(self):
        return FreelancerContract(rate=self.rate, hours=self.hours)
    
class CommissionModel(BaseModel):
    ctype: Literal['commission']
    commission: int
    num_contracts: int

    def to_contract(self):
        return CommissionContract(commission=self.commission, num_contracts=self.num_contracts)

class SalariedModel(BaseModel):
    ctype: Literal['salaried']
    salary: int
    hours: int

    def to_contract(self):
        return SalariedContract(salary=self.salary, hours=self.hours)
    
class HourlyModel(BaseModel):
    ctype: Literal['hourly']
    rate: int
    hours: int
    overhead:int

    def to_contract(self):
        return HourlyContract(rate=self.rate, hours=self.hours, overhead = self.overhead)

class NoContractModel(BaseModel):
    ctype: Literal['none']

    def to_contract(self):
        return NoContract()

class ContractModel(BaseModel):
    contract: Union[FreelancerModel, CommissionModel, 
                    HourlyModel, SalariedModel, NoContractModel
                    ] = Field(..., discriminator='ctype')

    def execute_contract(self):
        return self.contract.to_contract()


class EmployeeBase(BaseModel, abc.ABC):
    id: UUID = Field(default_factory=uuid4, frozen=True)
    emp_number: str
    username: str 
    first_name: str 
    last_name: str  
    middle_name: str
    salary: int = Field(gt=4000000, description="Salary must be more than $40,000")
    email: EmailStr
    contract_type: ContractModel 
    updated_at: datetime
    created_at: datetime

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
    id: UUID 
    emp_number: Optional[str]
    username: Optional[str] 
    first_name: Optional[str]
    last_name: Optional[str ]
    middle_name: Optional[str] 
    salary: Optional[int] 
    email: Optional[str] 
    contract_type: Optional[str]
    updated_at: datetime
    created_at: datetime
    
class EmployeeShort(BaseModel):
    emp_number: Optional[str]
    first_name: str = Field(exclude=True)
    last_name: str = Field(exclude=True)
    salary: Optional[int] 
    contract_type: str
    updated_at: datetime

    @computed_field
    @property
    def full_name(self) -> str:
      return f"{self.last_name}, {self.first_name}"

    #override 
    def model_dump(self, *args, **kwargs):
        od = super().model_dump(*args, **kwargs)
        full_name = self.full_name
        emp_number = od.pop('emp_number')
        salary = od.pop('salary')
        contract_type = od.pop('contract_type')
        updated_at = od.pop('updated_at')
        
        ordered_dict = {
            'emp_number': emp_number,
            'full_name': full_name,
            'salary': salary,
            'contract_type': contract_type,
            'updated-at': updated_at
        }
        return ordered_dict
    
 

class EmployeePaymentsDTO(BaseModel):
    employee: EmployeeShort
    payment: str
    contract_type: str

    # override
    def model_dump(self, *args, **kwargs):
        od = super().model_dump(*args, **kwargs)
        short_dump = self.employee.model_dump()
        od.update(short_dump)
        od.pop('employee')

        ordered_dict = {
            'employee': short_dump,
            'contract_type': self.contract_type,
            'payment': self.payment
        }
        return ordered_dict

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
