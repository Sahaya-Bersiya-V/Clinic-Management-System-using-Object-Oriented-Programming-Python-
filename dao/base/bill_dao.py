from abc import ABC, abstractmethod

class BillDAO(ABC):
    @abstractmethod
    def create_bill(self, bill):
        pass

    @abstractmethod
    def get_bill_by_id(self, bill_id):
        pass
