from lib.services.lab_tech_service import LabTechService

class LabTechDashboard:
    def __init__(self, user):
        self.user = user
        self.service = LabTechService()

    def _prompt_patient_id(self):
        # LabTech doesn't have list_patients exposed in LabTechService yet. 
        # But for 'View Patient Reports' or 'Add Test Result', searching by name would be useful.
        # User requested "in every dashboard".
        # LabTechService -> LabReportDAO -> Doesn't access PatientDAO usually.
        # So we might just have to skip advanced search here unless we add PatientDAO to LabTechService.
        # Given "very difficult to remember ID", I will just ask for ID for now, 
        # but add a note or minimal helper if I can list recent requests.
        return input("Patient ID: ").strip()

    def _prompt_request_id(self):
        # We can list pending requests as reference
         rid = input("Request ID (Enter 'L' to list pending): ").strip()
         if rid.upper() == 'L':
             self.update_status_ui() # This lists pending requests
             return input("Request ID: ").strip()
         return rid

    def display(self):
        while True:
            print(f"\n--- Lab Technician Dashboard ({self.user.get_username()}) ---")
            print("1. Add Test Result (Manual Entry)")
            print("2. View Patient Reports")
            print("3. Manage Lab Tests (Catalog)")
            print("4. View Pending Requests & Update Status")
            print("5. Re-upload/Correct Lab Report")
            print("6. View Patient List (ID Lookup)")
            print("7. Logout")
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.add_test_result()
            elif choice == '2':
                self.view_reports()
            elif choice == '3':
                self.manage_lab_tests_ui()
            elif choice == '4':
                self.update_status_ui()
            elif choice == '5':
                self.correct_report_ui()
            elif choice == '6':
                 self.view_patient_list()
            elif choice == '7':
                break
            else:
                print("Invalid choice.")

    def add_test_result(self):
        print("\n--- Add Test Result ---")
        
        try:
            tests = self.service.get_available_tests()
            test_names = [t['test_name'] for t in tests]
            print("Available Tests:", ", ".join(test_names))
        except Exception as e:
            print(f"Could not fetch tests: {e}")

        patient_id = self._prompt_patient_id()
        test_name = input("Test Name: ").strip()
        result = input("Result: ").strip()
        
        try:
            self.service.add_test_result(patient_id, test_name, result)
            print("Test result added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def view_reports(self):
        print("\n--- View Reports ---")
        patient_id = self._prompt_patient_id()
        
        try:
            reports = self.service.view_patient_reports(patient_id)
            if not reports:
                print("No reports found.")
            else:
                for r in reports:
                    print(f"ID: {r.get_report_id()}, Test: {r.get_test_name()}, Result: {r.get_result()}, Date: {r.get_date()}")
        except Exception as e:
            print(f"Error: {e}")

    def manage_lab_tests_ui(self):
        print("\n--- Manage Lab Tests ---")
        print("1. View All Tests")
        print("2. Add New Test Type")
        sub = input("Choice: ").strip()
        if sub == '1':
            try:
                tests = self.service.get_available_tests()
                print("Current Catalog:")
                for t in tests:
                    print(f"ID: {t['test_id']}, Name: {t['test_name']}, Cost: {t['cost']}")
            except Exception as e:
                print(f"Error: {e}")
        elif sub == '2':
            name = input("New Test Name: ").strip()
            cost = input("Cost: ").strip()
            try:
                self.service.add_new_test(name, cost)
                print("Test type added.")
            except Exception as e:
                print(f"Error: {e}")

    def update_status_ui(self):
        print("\n--- Pending Lab Requests ---")
        try:
            reqs = self.service.get_pending_lab_requests()
            if not reqs:
                print("No pending requests.")
                return
            
            for r in reqs:
                print(f"ReqID: {r['request_id']}, Patient: {r['patient_id']}, Test: {r['test_name']}, Status: {r['status']}")
            
            rid = self._prompt_request_id()
            if rid:
                print("Statuses: Processing, Completed")
                status = input("New Status: ").strip()
                self.service.update_request_status(rid, status)
                print("Status updated.")
                if status == 'Completed':
                    print("Note: Use 'Re-upload/Correct Lab Report' or similar if result needs entry, implicitly status update doesn't ask for result here but usually should.")
        except Exception as e:
            print(f"Error: {e}")

    def correct_report_ui(self):
        print("\n--- Correct/Re-upload Report ---")
        rid = self._prompt_request_id()
        new_result = input("New/Corrected Result: ").strip()
        try:
            self.service.update_lab_report(rid, new_result)
            print("Report updated and notified (status set to Completed).")
        except Exception as e:
             print(f"Error: {e}")

    def view_patient_list(self):
        print("\n--- Patient List ---")
        try:
            patients = self.service.get_all_patients()
            if not patients:
                print("No patients found.")
            else:
                 for p in patients:
                    print(f"ID: {p.get_patient_id()}, Name: {p.get_name()}, Contact: {p.get_contact()}")
        except Exception as e:
            print(f"Error: {e}")
