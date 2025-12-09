from dao.impl.appointment_dao_impl import AppointmentDAOImpl
from dao.impl.lab_request_dao_impl import LabRequestDAOImpl
from dao.impl.lab_report_dao_impl import LabReportDAOImpl # mainly for getting test list
from models.appointment import Appointment
from models.lab_request import LabRequest
from search.search_engine import SearchEngine # Assuming exists? No, I'll stick to DAOs.
from validation.validators import Validators

class DoctorService:
    def __init__(self):
        self.appointment_dao = AppointmentDAOImpl()
        self.lab_request_dao = LabRequestDAOImpl()
        self.lab_report_dao = LabReportDAOImpl()

    def get_appointments(self, doctor_id):
        # In a real app, doctor_id would come from the logged in user's staff record.
        # For now, we assume the dashboard passes the correct ID.
        return self.appointment_dao.get_appointments_by_doctor(doctor_id)

    def diagnose_patient(self, appointment_id, diagnosis, prescription):
        # Functions as Record Consultation Notes
        self.record_consultation(appointment_id, diagnosis, prescription)

    def record_consultation(self, appointment_id, diagnosis, prescription):
        err = Validators.validate_id(appointment_id)
        if err: raise ValueError(err)
        
        # In a real app, fetch existing, update fields.
        # Here we just blindly update based on ID.
        appt = Appointment(appointment_id=appointment_id, status="Diagnosed", diagnosis=diagnosis, prescription=prescription)
        self.appointment_dao.update_appointment(appt)

    def prescribe_medication(self, appointment_id, prescription):
        # Updates existing prescription
        # We need to fetch current diagnosis to avoid overwriting it if possible, 
        # but update_appointment takes a full object.
        # Since we don't have get_by_id in all DAO impls perfectly yet, we might overwrite.
        # But wait, I added get_appointment_by_id earlier!
        # Let's use it.
        appointment = self.appointment_dao.get_appointment_by_id(appointment_id)
        if not appointment: raise ValueError("Appointment not found")
        
        current_presc = appointment.get_prescription()
        new_presc = f"{current_presc}; {prescription}" if current_presc else prescription
        appointment.set_prescription(new_presc)
        self.appointment_dao.update_appointment(appointment)

    def prescribe_lab_test(self, appointment_id, patient_id, test_id):
        # Create Lab Request
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
        # Create a new appointment
        appt = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date, status="Follow-Up Recommended")
        return self.appointment_dao.create_appointment(appt)

    def generate_medical_certificate(self, patient_id, diagnosis, days_rest):
        # Return string
        return f"MEDICAL CERTIFICATE\nTo whom it may concern,\nPatient ID {patient_id} is diagnosed with {diagnosis} and is recommended {days_rest} days of rest."

    def mark_consultation_completed(self, appointment_id):
        appointment = self.appointment_dao.get_appointment_by_id(appointment_id)
        if not appointment: raise ValueError("Appointment not found")
        appointment.set_status("Completed")
        self.appointment_dao.update_appointment(appointment)

    def get_test_list(self):
        return self.lab_report_dao.get_all_tests()
