from pydantic import BaseModel
from typing import Union

class Contract(BaseModel):
    contract_type: str

class FreelancerContract(Contract):
    rate: float
    hours: int

class CommissionContract(Contract):
    commission_rate: float
    total_sales: float

class SalariedContract(Contract):
    salary: float
    bonus: float

class Employee(BaseModel):
    first_name: str
    last_name: str
    emp_number: str
    salary: float
    contract: Union[FreelancerContract, CommissionContract, SalariedContract]

    class Config:
        json_encoders = {
            Contract: lambda v: v.dict()
        }

    def model_dump(self, *args, **kwargs):
        employee_dict = super().dict(*args, **kwargs)
        contract_dict = self.contract.dict()
        contract_type = contract_dict.pop("contract_type")
        contract_dict["contract_type"] = contract_type
        employee_dict["contract"] = contract_dict
        return employee_dict

# Example usage
freelancer_contract = FreelancerContract(contract_type="freelancer", rate=100, hours=40)
employee = Employee(
    first_name="John",
    last_name="Doe",
    emp_number="E1234",
    salary=50000,
    contract=freelancer_contract
)

print(employee.model_dump())

