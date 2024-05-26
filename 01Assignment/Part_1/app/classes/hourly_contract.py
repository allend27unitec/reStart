from dataclasses import dataclass
from typing import Optional
from .contract import Contract

@dataclass
class HourlyContract(Contract):
    # Contract type for an employee being paid on an hourly basis.

    rate: int = 0
    hours: int = 0
    overhead: int = 0

    def contract_type(self) -> str:
        return "Hourly Contract"

    def get_payment(self) -> int:
        return self.rate * self.hours + self.overhead

