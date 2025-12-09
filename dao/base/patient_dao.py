from abc import ABC, abstractmethod
from models.patient import Patient

class PatientDAO(ABC):
    @abstractmethod
    def create_patient(self, patient):
        pass

    @abstractmethod
    def get_patient_by_id(self, patient_id):
        pass

    @abstractmethod
    def get_all_patients(self):
        pass

    @abstractmethod
    def update_patient(self, patient):
        pass

    @abstractmethod
    def search_patients(self, query):
        pass
