from dao.impl.appointment_dao_impl import AppointmentDAOImpl
from validation.validators import Validators

class DoctorService:
    def __init__(self):
        self.appointment_dao = AppointmentDAOImpl()

    def get_appointments(self, doctor_id):
        # In a real app, doctor_id would come from the logged in user's staff record.
        # For now, we assume the dashboard passes the correct ID.
        return self.appointment_dao.get_appointments_by_doctor(doctor_id)

    def diagnose_patient(self, appointment_id, diagnosis, prescription):
        err = Validators.validate_id(appointment_id)
        if err: raise ValueError(err)
        err = Validators.validate_non_empty(diagnosis, "Diagnosis")
        if err: raise ValueError(err)
        err = Validators.validate_non_empty(prescription, "Prescription")
        if err: raise ValueError(err)

        # Retrieve appointment first (optional, but good for verification)
        # For now, just update
        # We need to create an Appointment object with the ID and new data
        # But the DAO update method expects an object.
        # We should probably fetch it first or just create a dummy object with the ID.
        # Let's fetch it if we had a get_by_id, but we don't have it in the interface yet.
        # Wait, AppointmentDAO has get_appointments_by_doctor and get_all.
        # I'll just create an object with the ID and the fields to update.
        
        from models.appointment import Appointment
        appt = Appointment(appointment_id=appointment_id, status="Diagnosed", diagnosis=diagnosis, prescription=prescription)
        self.appointment_dao.update_appointment(appt)
