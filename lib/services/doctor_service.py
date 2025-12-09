from dao.impl.appointment_dao_impl import AppointmentDAOImpl
from dao.impl.lab_request_dao_impl import LabRequestDAOImpl
from dao.impl.lab_report_dao_impl import LabReportDAOImpl
from dao.impl.prescription_dao_impl import PrescriptionDAOImpl
from dao.impl.medicine_dao_impl import MedicineDAOImpl
from models.appointment import Appointment
from models.lab_request import LabRequest
from models.prescription import Prescription
from validation.validators import Validators

class DoctorService:
    def __init__(self):
        self.appointment_dao = AppointmentDAOImpl()
        self.lab_request_dao = LabRequestDAOImpl()
        self.lab_report_dao = LabReportDAOImpl()
        self.prescription_dao = PrescriptionDAOImpl()
        self.medicine_dao = MedicineDAOImpl()

    def get_appointments(self, doctor_id):
        return self.appointment_dao.get_appointments_by_doctor(doctor_id)

    def diagnose_patient(self, appointment_id, diagnosis, prescription):
        self.record_consultation(appointment_id, diagnosis, prescription)

    def record_consultation(self, appointment_id, diagnosis, prescription):
        err = Validators.validate_id(appointment_id)
        if err: raise ValueError(err)
        
        # We still update the diagnosis text in appointment.
        # 'prescription' here might be general notes from old flow.
        appt = self.appointment_dao.get_appointment_by_id(appointment_id)
        if appt:
            appt.set_status("Diagnosed")
            appt.set_diagnosis(diagnosis)
            # append notes or set them? Set for now.
            if prescription:
                appt.set_prescription(prescription) # Keeping this for text notes as well?
            self.appointment_dao.update_appointment(appt)

    def prescribe_medication(self, appointment_id, prescription):
        # Legacy/Simple Text Prescription
        appointment = self.appointment_dao.get_appointment_by_id(appointment_id)
        if not appointment: raise ValueError("Appointment not found")
        
        current_presc = appointment.get_prescription()
        new_presc = f"{current_presc}; {prescription}" if current_presc else prescription
        appointment.set_prescription(new_presc)
        self.appointment_dao.update_appointment(appointment)

    def add_prescription_item(self, appointment_id, medicine_id, dosage, duration, quantity):
        # New Structured Prescription
        err = Validators.validate_id(appointment_id)
        if err: raise ValueError(err)
        err = Validators.validate_id(medicine_id)
        if err: raise ValueError(err)
        
        # Add to structured table
        p = Prescription(appointment_id=appointment_id, medicine_id=medicine_id, dosage=dosage, duration=duration, quantity=quantity)
        self.prescription_dao.create_prescription(p)

        # Update legacy/text field in Appointment for history view
        try:
            medicine = self.medicine_dao.get_medicine_by_id(medicine_id)
            med_name = medicine.get_name() if medicine else f"Med#{medicine_id}"
            
            appt = self.appointment_dao.get_appointment_by_id(appointment_id)
            if appt:
                new_entry = f"{med_name} ({dosage}, {duration}, Qty:{quantity})"
                current = appt.get_prescription()
                updated = f"{current}; {new_entry}" if current else new_entry
                appt.set_prescription(updated)
                self.appointment_dao.update_appointment(appt)
        except Exception as e:
            # Don't fail the whole transaction if legacy update fails, but good to log.
            print(f"Warning: Failed to update legacy prescription text: {e}")

    def get_all_medicines(self):
        return self.medicine_dao.search_medicines("") # empty query returns all? No, search_medicines usually needs query. 
        # Actually I need get_all in MedicineDAO or search with empty string behaving like get all.
        # Let's check MedicineDAOImpl later, but commonly search '' might fail or return all.
        # Assuming search_medicines works for now or I use another way.
        # Wait, MedicineDAOImpl.search_medicines executes "WHERE name LIKE %s". '%%' matches all.
        return self.medicine_dao.search_medicines("")

    def get_prescribed_items(self, appointment_id):
        return self.prescription_dao.get_prescriptions_by_appointment(appointment_id)

    def prescribe_lab_test(self, appointment_id, patient_id, test_id):
        request = LabRequest(appointment_id=appointment_id, patient_id=patient_id, test_id=test_id, status='Pending')
        return self.lab_request_dao.create_request(request)

    def view_medical_history(self, patient_id):
        return self.appointment_dao.get_appointments_by_patient(patient_id)

    def update_consultation_notes(self, appointment_id, diagnosis, prescription):
        self.record_consultation(appointment_id, diagnosis, prescription)

    def approve_lab_test_report(self, request_id):
        request = self.lab_request_dao.get_request_by_id(request_id)
        if not request: raise ValueError("Request not found")
        request.set_status("Approved")
        self.lab_request_dao.update_request(request)

    def recommend_follow_up(self, patient_id, doctor_id, date):
        appt = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date, status="Follow-Up Recommended")
        return self.appointment_dao.create_appointment(appt)

    def generate_medical_certificate(self, patient_id, diagnosis, days_rest):
        return f"MEDICAL CERTIFICATE\nTo whom it may concern,\nPatient ID {patient_id} is diagnosed with {diagnosis} and is recommended {days_rest} days of rest."

    def mark_consultation_completed(self, appointment_id):
        appointment = self.appointment_dao.get_appointment_by_id(appointment_id)
        if not appointment: raise ValueError("Appointment not found")
        appointment.set_status("Completed")
        self.appointment_dao.update_appointment(appointment)

    def get_test_list(self):
        return self.lab_report_dao.get_all_tests()
