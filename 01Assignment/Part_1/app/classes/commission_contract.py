from dataclasses import dataclass
from .contract import Contract

@dataclass
class CommissionContract(Contract):

    commission: int
    num_contracts: int = 0

    def contract_type(self) -> str:
        return "Commission"

    def get_payment(self) -> int:
        return self.commission * self.num_contracts 
