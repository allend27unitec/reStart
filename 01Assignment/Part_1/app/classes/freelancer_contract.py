from dataclasses import dataclass
from .contract import Contract

@dataclass
class FreelancerContract(Contract):

    rate: int
    hours: int = 0
    gst_number: str = ""
    
    def contract_type(self) -> str:
        return "Freelancer"

    def get_payment(self) -> int:
        return int(self.rate * self.hours)

