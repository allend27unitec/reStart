from dataclasses import dataclass
from .contract import Contract

@dataclass
class SalariedContract(Contract):

    hours: int = 0
    salary: int = 0
    def get_payment(self) -> int:
        return self.calculate_emp_salary() 

    def contract_type(self) -> str:
        return "Salaried Contract"

    def calculate_emp_salary(self) -> int:
        overtime = self.hours - 50
        overtime_amount = int(overtime * (self.salary / 50))
        return self.salary + overtime_amount


