from lib.services.lab_tech_service import LabTechService

class LabTechDashboard:
    def __init__(self, user):
        self.user = user
        self.service = LabTechService()

    def display(self):
        while True:
            print(f"\n--- Lab Technician Dashboard ({self.user.get_username()}) ---")
            print("1. Add Test Result")
            print("2. View Patient Reports")
            print("3. Logout")
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.add_test_result()
            elif choice == '2':
                self.view_reports()
            elif choice == '3':
                break
            else:
                print("Invalid choice.")

    def add_test_result(self):
        print("\n--- Add Test Result ---")
        
        try:
            tests = self.service.get_available_tests()
            print("Available Tests:", ", ".join(tests))
        except Exception as e:
            print(f"Could not fetch tests: {e}")

        patient_id = input("Patient ID: ").strip()
        print("Choose your test from options")
        print("""
        1.Blood Count (CBC)
        2.X-Ray
        3.Urinalysis
        4.MRI Scan""")
        test_name = input("Test Name: ").strip()
        result = input("Result: ").strip()
        
        try:
            self.service.add_test_result(patient_id, test_name, result)
            print("Test result added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def view_reports(self):
        print("\n--- View Reports ---")
        patient_id = input("Patient ID: ").strip()
        
        try:
            reports = self.service.view_patient_reports(patient_id)
            for r in reports:
                print(f"ID: {r.get_report_id()}, Test: {r.get_test_name()}, Result: {r.get_result()}, Date: {r.get_date()}")
        except Exception as e:
            print(f"Error: {e}")
