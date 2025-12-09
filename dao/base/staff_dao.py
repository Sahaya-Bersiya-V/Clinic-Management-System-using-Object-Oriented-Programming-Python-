from abc import ABC, abstractmethod
from models.staff import Staff

class StaffDAO(ABC):
    @abstractmethod
    def create_staff(self, staff):
        pass

    @abstractmethod
    def get_all_staff(self):
        pass

    @abstractmethod
    def get_staff_by_id(self, staff_id):
        pass

    @abstractmethod
    def update_staff(self, staff):
        pass

    @abstractmethod
    def delete_staff(self, staff_id):
        pass

    @abstractmethod
    def get_staff_by_role(self, role):
        pass

    @abstractmethod
    def deactivate_staff(self, staff_id):
        pass

