from abc import ABC, abstractmethod
from models.appointment import Appointment

class AppointmentDAO(ABC):
    @abstractmethod
    def create_appointment(self, appointment):
        pass

    @abstractmethod
    def get_appointments_by_doctor(self, doctor_id):
        pass

    @abstractmethod
    def get_appointment_by_id(self, appointment_id):
        pass

    @abstractmethod
    def get_all_appointments(self):
        pass
    
    @abstractmethod
    def update_appointment(self, appointment):
        pass
