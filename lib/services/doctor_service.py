from dao.impl.appointment_dao_impl import AppointmentDAOImpl
from dao.impl.lab_request_dao_impl import LabRequestDAOImpl
from dao.impl.lab_report_dao_impl import LabReportDAOImpl
from dao.impl.prescription_dao_impl import PrescriptionDAOImpl
from dao.impl.medicine_dao_impl import MedicineDAOImpl
from dao.impl.patient_dao_impl import PatientDAOImpl
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
        self.patient_dao = PatientDAOImpl()

    def get_appointments(self, doctor_id):
        """
        Purpose: Retrieves a list of appointments assigned to a specific doctor.
        Context: Called by DoctorDashboard.view_appointments to list schedule.
        Calls: AppointmentDAOImpl.get_appointments_by_doctor
        """
        return self.appointment_dao.get_appointments_by_doctor(doctor_id)

    def diagnose_patient(self, appointment_id, diagnosis, prescription):
        """
        Purpose: Records a diagnosis and initial prescription for a patient during an appointment.
        Context: Legacy alias for record_consultation. Called by DoctorDashboard.diagnose_patient.
        Calls: self.record_consultation
        """
        self.record_consultation(appointment_id, diagnosis, prescription)

    def record_consultation(self, appointment_id, diagnosis, prescription):
        """
        Purpose: Updates an appointment with diagnosis details and text-based prescription notes. Sets status to 'Diagnosed'.
        Context: Called by DoctorDashboard.record_consultation for documentation.
        Calls: Validators.validate_id, AppointmentDAOImpl.get_appointment_by_id, AppointmentDAOImpl.update_appointment
        """
        err = Validators.validate_id(appointment_id)
        if err: raise ValueError(err)
        
        appt = self.appointment_dao.get_appointment_by_id(appointment_id)
        if appt:
            appt.set_status("Diagnosed")
            appt.set_diagnosis(diagnosis)
            if prescription:
                appt.set_prescription(prescription)
            self.appointment_dao.update_appointment(appt)

    def prescribe_medication(self, appointment_id, prescription):
        """
        Purpose: Appends a text string to the appointment's prescription field (Legacy/Notes).
        Context: Called by DoctorDashboard.prescribe_medication (legacy path).
        Calls: AppointmentDAOImpl.get_appointment_by_id, AppointmentDAOImpl.update_appointment
        """
        appointment = self.appointment_dao.get_appointment_by_id(appointment_id)
        if not appointment: raise ValueError("Appointment not found")
        
        current_presc = appointment.get_prescription()
        new_presc = f"{current_presc}; {prescription}" if current_presc else prescription
        appointment.set_prescription(new_presc)
        self.appointment_dao.update_appointment(appointment)

    def add_prescription_item(self, appointment_id, medicine_id, dosage, duration, quantity):
        """
        Purpose: Creates a structured prescription entry and syncs it to the appointment's text notes.
        Context: Called by DoctorDashboard.prescribe_medication for adding specific items.
        Calls: PrescriptionDAOImpl.create_prescription, MedicineDAOImpl.get_medicine_by_id, AppointmentDAOImpl.update_appointment
        """
        err = Validators.validate_id(appointment_id)
        if err: raise ValueError(err)
        err = Validators.validate_id(medicine_id)
        if err: raise ValueError(err)
        
        p = Prescription(appointment_id=appointment_id, medicine_id=medicine_id, dosage=dosage, duration=duration, quantity=quantity)
        self.prescription_dao.create_prescription(p)

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
            print(f"Warning: Failed to update legacy prescription text: {e}")

    def get_all_medicines(self):
        """
        Purpose: Retrieves a list of all available medicines in the inventory.
        Context: Called by DoctorDashboard to show available options for prescription.
        Calls: MedicineDAOImpl.search_medicines
        """
        return self.medicine_dao.search_medicines("")

    def get_prescribed_items(self, appointment_id):
        """
        Purpose: Retrieves structured prescription items for a specific appointment.
        Context: Called by dashboards or history viewers to see detailed medication list.
        Calls: PrescriptionDAOImpl.get_prescriptions_by_appointment
        """
        return self.prescription_dao.get_prescriptions_by_appointment(appointment_id)

    def prescribe_lab_test(self, appointment_id, patient_id, test_id):
        """
        Purpose: Creates a new Lab Request for a patient.
        Context: Called by DoctorDashboard.prescribe_lab_test.
        Calls: LabRequestDAOImpl.create_request
        """
        request = LabRequest(appointment_id=appointment_id, patient_id=patient_id, test_id=test_id, status='Pending')
        return self.lab_request_dao.create_request(request)

    def view_medical_history(self, patient_id):
        """
        Purpose: Retrieves past appointments and medical records for a patient.
        Context: Called by DoctorDashboard.view_medical_history.
        Calls: AppointmentDAOImpl.get_appointments_by_patient
        """
        return self.appointment_dao.get_appointments_by_patient(patient_id)

    def update_consultation_notes(self, appointment_id, diagnosis, prescription):
        """
        Purpose: Updates existing consultation notes.
        Context: Called by DoctorDashboard.update_consultation_notes.
        Calls: self.record_consultation
        """
        self.record_consultation(appointment_id, diagnosis, prescription)

    def approve_lab_test_report(self, request_id):
        """
        Purpose: Updates the status of a Lab Request to 'Approved' after review.
        Context: Called by DoctorDashboard.approve_lab_report.
        Calls: LabRequestDAOImpl.get_request_by_id, LabRequestDAOImpl.update_request
        """
        request = self.lab_request_dao.get_request_by_id(request_id)
        if not request: raise ValueError("Request not found")
        request.set_status("Approved")
        self.lab_request_dao.update_request(request)

    def recommend_follow_up(self, patient_id, doctor_id, date):
        """
        Purpose: Creates a new appointment with status 'Follow-Up Recommended'.
        Context: Called by DoctorDashboard.recommend_follow_up.
        Calls: AppointmentDAOImpl.create_appointment
        """
        err = Validators.validate_future_date(date)
        if err: raise ValueError(err)

        appt = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date, status="Follow-Up")
        return self.appointment_dao.create_appointment(appt)

    def generate_medical_certificate(self, patient_id, diagnosis, days_rest):
        """
        Purpose: Generates a text string representing a medical certificate.
        Context: Called by DoctorDashboard.generate_medical_certificate.
        Calls: PatientDAO.get_patient_by_id
        """
        # Validate ID
        err = Validators.validate_id(patient_id)
        if err: raise ValueError(f"Invalid Patient ID: {err}")
        
        # Validate Days
        if not str(days_rest).isdigit() or int(days_rest) <= 0:
            raise ValueError("Days of rest must be a positive number.")

        # Fetch Patient Data
        patient = self.patient_dao.get_patient_by_id(patient_id)
        if not patient:
            raise ValueError(f"Patient with ID {patient_id} not found.")

        # Generate Certificate
        return (
            "========================================\n"
            "          MEDICAL CERTIFICATE           \n"
            "========================================\n"
            f"To whom it may concern,\n\n"
            f"This is to certify that Mr./Ms. {patient.get_name()} (Age: {patient.get_age()})\n"
            f"Patient ID: {patient_id}\n"
            f"has been under my care and is diagnosed with: {diagnosis}.\n\n"
            f"Recommendation: {days_rest} days of rest is advised for recovery.\n\n"
            "Doctor Signature: __________________\n"
            "========================================"
        )

    def mark_consultation_completed(self, appointment_id):
        """
        Purpose: Marks an appointment/consultation as 'Completed'.
        Context: Called by DoctorDashboard.complete_consultation.
        Calls: AppointmentDAOImpl.get_appointment_by_id, AppointmentDAOImpl.update_appointment
        """
        appointment = self.appointment_dao.get_appointment_by_id(appointment_id)
        if not appointment: raise ValueError("Appointment not found")
        appointment.set_status("Completed")
        self.appointment_dao.update_appointment(appointment)

    def get_test_list(self):
        """
        Purpose: Retrieves the list of available lab tests (Catalog).
        Context: Called by DoctorDashboard to show test options.
        Calls: LabReportDAOImpl.get_all_tests
        """
        return self.lab_report_dao.get_all_tests()

    def get_appointment_details(self, appointment_id):
        """
        Purpose: Retrieves detailed information for a specific appointment.
        Context: Called by DoctorDashboard for pre-filling update forms.
        Calls: AppointmentDAOImpl.get_appointment_by_id
        """
        return self.appointment_dao.get_appointment_by_id(appointment_id)
