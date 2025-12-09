from abc import ABC, abstractmethod

class BillDAO(ABC):
    @abstractmethod
    def create_bill(self, bill):
        pass
