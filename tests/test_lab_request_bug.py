from lib.services.doctor_service import DoctorService
from dao.impl.patient_dao_impl import PatientDAOImpl
from dao.impl.appointment_dao_impl import AppointmentDAOImpl
from dao.impl.lab_report_dao_impl import LabReportDAOImpl
from models.patient import Patient
from models.appointment import Appointment

def test_bug():
    try:
        # Setup Data
        p_dao = PatientDAOImpl()
        a_dao = AppointmentDAOImpl()
        lr_dao = LabReportDAOImpl() # for tests

        # Create Patient
        pat = Patient(name="TestPatient", age=30, gender="M", contact="1234567890", blood_group="O+", address="Test Addr")
        pat = p_dao.create_patient(pat)
        print(f"Patient Created: {pat.get_patient_id()}")

        # Create Appointment
        appt = Appointment(patient_id=pat.get_patient_id(), doctor_id=1, date="2025-01-01", status="Scheduled")
        appt = a_dao.create_appointment(appt)
        print(f"Appointment Created: {appt.get_appointment_id()}")

        # Get Test ID (assuming some exist)
        tests = lr_dao.get_all_tests()
        if not tests:
            print("No lab tests found in DB. Inserting mock test.")
            # We can't insert via DAO easily here as LabReportDAO doesn't create *tests* (only Catalog management in LabTechService?) 
            # Actually LabReportDAOImpl has get_all_tests (SELECT * FROM lab_tests).
            # Assuming hms_schema_update ran, there are tests.
            pass
        else:
            print(f"Found {len(tests)} tests.")
        
        test_id = tests[0].get_test_id() if tests else 1

        # Test Prescribe Lab Request
        service = DoctorService()
        req = service.prescribe_lab_test(appt.get_appointment_id(), pat.get_patient_id(), test_id)
        print(f"Lab Request Created: ID {req.get_request_id()}")

        # Verify Persistence
        from dao.impl.lab_request_dao_impl import LabRequestDAOImpl
        lrq_dao = LabRequestDAOImpl()
        fetched = lrq_dao.get_request_by_id(req.get_request_id())
        
        if fetched:
            print(f"SUCCESS: Fetched Request {fetched.get_request_id()}, Status: {fetched.get_status()}")
        else:
            print("FAILURE: Could not fetch created request from DB.")

    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_bug()
