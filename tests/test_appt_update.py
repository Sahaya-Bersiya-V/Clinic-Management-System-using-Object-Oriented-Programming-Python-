from lib.services.doctor_service import DoctorService
from dao.impl.appointment_dao_impl import AppointmentDAOImpl
from models.appointment import Appointment
import datetime

def test_appt_update():
    try:
        dao = AppointmentDAOImpl()
        
        # Create Dummy Appointment
        appt = Appointment(patient_id=1, doctor_id=1, date="2025-12-09", status="Scheduled")
        appt = dao.create_appointment(appt)
        print(f"Created Appt ID: {appt.get_appointment_id()} Date: {appt.get_date()}")

        # Record Consultation
        service = DoctorService()
        print("Recording Consultation...")
        service.record_consultation(appt.get_appointment_id(), "Flu", "Rest and Water")

        # Verify
        updated = dao.get_appointment_by_id(appt.get_appointment_id())
        print(f"Updated Appt: Diagnosis='{updated.get_diagnosis()}', Rx='{updated.get_prescription()}', Status='{updated.get_status()}'")

        if updated.get_diagnosis() == "Flu" and "Rest" in updated.get_prescription():
            print("SUCCESS: Data filled correctly.")
        else:
            print("FAILURE: Data NOT filled.")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_appt_update()
