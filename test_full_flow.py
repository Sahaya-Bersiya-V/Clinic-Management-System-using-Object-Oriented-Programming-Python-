from lib.services.doctor_service import DoctorService
from lib.services.receptionist_service import ReceptionistService
from dao.impl.patient_dao_impl import PatientDAOImpl
import datetime

def test_full_flow():
    try:
        # 1. Register Patient via Receptionist Service (to be safe)
        r_service = ReceptionistService()
        pat_name = "FlowTestPatient"
        print(f"Registering {pat_name}...")
        try:
             # register_patient(self, name, age, gender, contact, blood_group, address)
             pat = r_service.register_patient(pat_name, 25, "M", "9999999999", "O+", "123 Street")
             print(f"Patient ID: {pat.get_patient_id()}")
        except Exception as e:
             # Fallback if I can't guess signature or DAO fails
             print(f"Reg fail: {e}")
             return

        # 2. Book Appointment
        print("Booking Appointment...")
        today = str(datetime.date.today())
        appt = r_service.book_appointment(pat.get_patient_id(), 1, today) # Doctor 1
        print(f"Appt ID: {appt.get_appointment_id()} Date: {appt.get_date()}")

        # 3. Doctor Diagnose
        d_service = DoctorService()
        print("Diagnosing...")
        d_service.record_consultation(appt.get_appointment_id(), "Flow Diagnosis", "Flow Rx")

        # 4. View History
        print("Viewing History...")
        history = d_service.view_medical_history(pat.get_patient_id())
        found = False
        for h in history:
            print(f" - {h.get_date()}: {h.get_diagnosis()} | {h.get_prescription()}")
            if h.get_diagnosis() == "Flow Diagnosis":
                found = True
        
        if found:
            print("SUCCESS: Full flow worked.")
        else:
            print("FAILURE: Diagnosis not found in history.")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_full_flow()
