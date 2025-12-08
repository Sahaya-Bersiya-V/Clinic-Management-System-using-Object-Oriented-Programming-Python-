from abc import ABC, abstractmethod
from models.medicine import Medicine

class MedicineDAO(ABC):
    @abstractmethod
    def create_medicine(self, medicine):
        pass

    @abstractmethod
    def get_all_medicines(self):
        pass

    @abstractmethod
    def update_medicine_stock(self, medicine_id, quantity):
        pass
