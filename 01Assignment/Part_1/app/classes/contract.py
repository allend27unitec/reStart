from abc import ABC, abstractmethod

class Contract(ABC):
    # Represents a contract and a payment process for a particular employeee.

    # Compute how much to pay an employee under this contract.
    @abstractmethod
    def get_payment(self) -> int:
        pass
    @abstractmethod
    def contract_type(self) -> str:
        pass
