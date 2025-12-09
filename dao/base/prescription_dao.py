from abc import ABC, abstractmethod

class PrescriptionDAO(ABC):
    @abstractmethod
    def create_prescription(self, prescription):
        pass

    @abstractmethod
    def get_prescriptions_by_appointment(self, appointment_id):
        pass
