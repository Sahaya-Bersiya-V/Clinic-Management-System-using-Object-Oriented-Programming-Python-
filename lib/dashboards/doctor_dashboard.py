from lib.services.doctor_service import DoctorService

class DoctorDashboard:
    def __init__(self, user):
        self.user = user
        self.service = DoctorService()

    def display(self):
        while True:
            print(f"\n--- Doctor Dashboard ({self.user.get_username()}) ---")
            print("1. View Appointments")
            print("2. Diagnose Patient")
            print("3. Logout")
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.view_appointments()
            elif choice == '2':
                self.diagnose_patient()
            elif choice == '3':
                break
            else:
                print("Invalid choice.")

    def view_appointments(self):
        # In a real system, we'd map the user_id to a doctor_id.
        # For this demo, we'll ask for doctor ID or assume 1 if not mapped.
        # Since we don't have a session mapping user->staff, I'll ask for Doctor ID for demo purposes
        # OR I could fetch the staff record for this user.
        # Given the constraints, I'll ask for Doctor ID to keep it simple but functional.
        doctor_id = input("Enter your Doctor ID to view appointments: ").strip()
        
        try:
            appts = self.service.get_appointments(doctor_id)
            print("\n--- Appointments ---")
            for a in appts:
                print(f"ID: {a.get_appointment_id()}, Patient ID: {a.get_patient_id()}, Date: {a.get_date()}, Status: {a.get_status()}")
        except Exception as e:
            print(f"Error: {e}")

    def diagnose_patient(self):
        print("\n--- Diagnose Patient ---")
        appt_id = input("Appointment ID: ").strip()
        diagnosis = input("Diagnosis: ").strip()
        prescription = input("Prescription: ").strip()
        
        try:
            self.service.diagnose_patient(appt_id, diagnosis, prescription)
            print("Diagnosis added successfully.")
        except Exception as e:
            print(f"Error: {e}")
