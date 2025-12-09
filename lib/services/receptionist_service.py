from dao.impl.patient_dao_impl import PatientDAOImpl
from dao.impl.appointment_dao_impl import AppointmentDAOImpl
from dao.impl.bill_dao_impl import BillDAOImpl
from models.patient import Patient
from models.appointment import Appointment
from models.bill import Bill
from datetime import date
from validation.validators import Validators

class ReceptionistService:
    def __init__(self):
        self.patient_dao = PatientDAOImpl()
        self.appointment_dao = AppointmentDAOImpl()
        self.bill_dao = BillDAOImpl()

    def register_patient(self, name, age, gender, contact, blood_group, address):
        err = Validators.validate_name(name)
        if err: raise ValueError(err)
        err = Validators.validate_phone(contact)
        if err: raise ValueError(err)
        if not age or int(age) <= 0: raise ValueError("Invalid age")
        
        patient = Patient(name=name, age=age, gender=gender, contact=contact, blood_group=blood_group, address=address)
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

    def get_patient_details(self, patient_id):
        return self.patient_dao.get_patient_by_id(patient_id)

    def generate_bill(self, patient_id, appointment_id, total_amount, discount):
        try:
            total_amount = float(total_amount)
            discount = float(discount)
            final_amount = total_amount - discount
            bill = Bill(patient_id=patient_id, appointment_id=appointment_id, total_amount=total_amount, discount=discount, final_amount=final_amount, status='Paid', date=str(date.today()))
            return self.bill_dao.create_bill(bill)
        except ValueError:
            raise ValueError("Invalid amount or discount")

    def update_patient_details(self, patient_id, name, age, gender, contact, blood_group, address):
        patient = self.patient_dao.get_patient_by_id(patient_id)
        if not patient: raise ValueError("Patient not found")
        patient.set_name(name)
        patient.set_age(age)
        patient.set_gender(gender)
        patient.set_contact(contact)
        patient.set_blood_group(blood_group)
        patient.set_address(address)
        self.patient_dao.update_patient(patient)

    def cancel_appointment(self, appointment_id):
        appointment = self.appointment_dao.get_appointment_by_id(appointment_id)
        if not appointment: raise ValueError("Appointment not found")
        appointment.set_status("Cancelled")
        self.appointment_dao.update_appointment(appointment)

    def search_patient_record(self, query):
        return self.patient_dao.search_patients(query)

    def get_bill_receipt(self, bill_id):
        return self.bill_dao.get_bill_by_id(bill_id)

    def check_doctor_availability(self, doctor_id):
        return self.appointment_dao.get_appointments_by_doctor(doctor_id)

    def check_in_patient(self, appointment_id):
        appointment = self.appointment_dao.get_appointment_by_id(appointment_id)
        if not appointment: raise ValueError("Appointment not found")
        appointment.set_status("Checked-In")
        self.appointment_dao.update_appointment(appointment)
