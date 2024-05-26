from dataclasses import dataclass
from .contract import Contract

@dataclass
class NoContract(Contract):

    def contract_type(self) -> str:
        return "No Contract"

    def get_payment(self) -> int:
        return 0

