from dao.impl.patient_dao_impl import PatientDAOImpl
from dao.impl.appointment_dao_impl import AppointmentDAOImpl
from models.patient import Patient
from models.appointment import Appointment
from validation.validators import Validators

class ReceptionistService:
    def __init__(self):
        self.patient_dao = PatientDAOImpl()
        self.appointment_dao = AppointmentDAOImpl()

    def register_patient(self, name, age, gender, contact):
        err = Validators.validate_name(name)
        if err: raise ValueError(err)
        err = Validators.validate_phone(contact)
        if err: raise ValueError(err)
        if not age or int(age) <= 0: raise ValueError("Invalid age")
        
        patient = Patient(name=name, age=age, gender=gender, contact=contact)
        return self.patient_dao.create_patient(patient)

    def book_appointment(self, patient_id, doctor_id, date):
        err = Validators.validate_id(patient_id)
        if err: raise ValueError(err)
        err = Validators.validate_id(doctor_id)
        if err: raise ValueError(err)
        
        appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date, status="Scheduled")
        return self.appointment_dao.create_appointment(appointment)
    
    def get_all_patients(self):
        return self.patient_dao.get_all_patients()
