from abc import ABC, abstractmethod
from models.medicine import Medicine

class MedicineDAO(ABC):
    @abstractmethod
    def create_medicine(self, medicine):
        pass

    @abstractmethod
    def get_medicine_by_id(self, medicine_id):
        pass

    @abstractmethod
    def get_all_medicines(self):
        pass

    @abstractmethod
    def update_medicine_stock(self, medicine_id, quantity):
        pass

    @abstractmethod
    def update_medicine(self, medicine):
        pass

    @abstractmethod
    def search_medicines(self, query):
        pass

    @abstractmethod
    def get_low_stock_medicines(self):
        pass
    
    @abstractmethod
    def get_expiring_medicines(self, threshold_date):
        pass
