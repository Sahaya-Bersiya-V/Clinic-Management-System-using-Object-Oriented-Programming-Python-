from lib.services.doctor_service import DoctorService

class DoctorDashboard:
    def __init__(self, user):
        self.user = user
        self.service = DoctorService()

    def display(self):
        while True:
            print(f"\n--- Doctor Dashboard ({self.user.get_username()}) ---")
            print("1. View Appointments")
            print("2. Record Consultation Notes")
            print("3. Prescribe Medication")
            print("4. Prescribe Lab Test")
            print("5. View Patient Medical History")
            print("6. Update Consultation Notes")
            print("7. Approve Lab Test Report")
            print("8. Recommend Follow-Up Appointment")
            print("9. Generate Medical Certificate")
            print("10. Mark Consultation as Completed")
            print("11. Logout")
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.view_appointments()
            elif choice == '2':
                self.record_consultation()
            elif choice == '3':
                self.prescribe_medication()
            elif choice == '4':
                self.prescribe_lab_test()
            elif choice == '5':
                self.view_medical_history()
            elif choice == '6':
                self.record_consultation() # Same as record
            elif choice == '7':
                self.approve_lab_report()
            elif choice == '8':
                self.recommend_follow_up()
            elif choice == '9':
                self.generate_medical_certificate()
            elif choice == '10':
                self.complete_consultation()
            elif choice == '11':
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

    def record_consultation(self):
        print("\n--- Record/Update Consultation Notes ---")
        appt_id = input("Appointment ID: ").strip()
        
        try:
            appt = self.service.get_appointment_details(appt_id)
            if not appt:
                print("Appointment not found.")
                return
                
            print(f"Patient ID: {appt.get_patient_id()}")
            print(f"Date: {appt.get_date()}")
            
            # Show current
            curr_diag = appt.get_diagnosis() or ""
            curr_rx = appt.get_prescription() or ""
            
            print(f"Current Diagnosis: {curr_diag}")
            diagnosis = input(f"New Diagnosis (Enter to keep): ").strip() or curr_diag
            
            print(f"Current Prescription (Text Note): {curr_rx}")
            prescription = input(f"New Prescription (Enter to keep): ").strip() or curr_rx
            
            self.service.record_consultation(appt_id, diagnosis, prescription)
            print("Consultation notes updated.")
            
        except Exception as e:
            print(f"Error: {e}")

    def prescribe_medication(self):
        print("\n--- Prescribe Medication ---")
        appt_id = input("Appointment ID: ").strip()
        
        # Show Medicines
        try:
            meds = self.service.get_all_medicines()
            print("Available Medicines:")
            for m in meds:
                print(f"ID: {m.get_medicine_id()}, Name: {m.get_name()}, Stock: {m.get_quantity()}")
        except Exception as e:
            print(f"Error fetching medicines: {e}")
            return

        while True:
            print("\nAdd Medication Item:")
            mid = input("Medicine ID: ").strip()
            if not mid: break # Exit loop if empty
            
            dosage = input("Dosage (e.g., 500mg): ").strip()
            duration = input("Duration (e.g., 5 days): ").strip()
            quantity = input("Quantity: ").strip()
            
            try:
                self.service.add_prescription_item(appt_id, mid, dosage, duration, quantity)
                print("Item added to prescription.")
            except Exception as e:
                print(f"Error adding item: {e}")
            
            more = input("Add another? (y/n): ").lower()
            if more != 'y': break

    def prescribe_lab_test(self):
        print("\n--- Prescribe Lab Test ---")
        # Show tests
        try:
            tests = self.service.get_test_list()
            print("Available Tests:")
            for t in tests:
                print(f"ID: {t['test_id']}, Name: {t['test_name']}, Cost: {t['cost']}")
            appt_id = input("Appointment ID: ").strip()
            pid = input("Patient ID: ").strip()
            tid = input("Test ID (Integer): ").strip()
            self.service.prescribe_lab_test(appt_id, pid, tid)
            print("Lab Test Prescribed.")
        except Exception as e: print(f"Error: {e}")

    def view_medical_history(self):
        print("\n--- View Medical History ---")
        pid = input("Patient ID: ").strip()
        try:
            history = self.service.view_medical_history(pid)
            for h in history:
                print(f"Date: {h.get_date()}, Diagnosis: {h.get_diagnosis()}, Rx: {h.get_prescription()}")
        except Exception as e: print(f"Error: {e}")

    def approve_lab_report(self):
        print("\n--- Approve Lab Report ---")
        rid = input("Lab Request ID: ").strip()
        try:
            self.service.approve_lab_test_report(rid)
            print("Lab Report Approved.")
        except Exception as e: print(f"Error: {e}")

    def recommend_follow_up(self):
        print("\n--- Recommend Follow-Up ---")
        pid = input("Patient ID: ").strip()
        did = input("Doctor ID: ").strip()
        date = input("Date (YYYY-MM-DD): ").strip()
        try:
            self.service.recommend_follow_up(pid, did, date)
            print("Follow-up Recommended (Appointment Created).")
        except Exception as e: print(f"Error: {e}")

    def generate_medical_certificate(self):
        print("\n--- Generate Medical Certificate ---")
        pid = input("Patient ID: ").strip()
        diag = input("Diagnosis: ").strip()
        days = input("Days of Rest: ").strip()
        try:
            cert = self.service.generate_medical_certificate(pid, diag, days)
            print(cert)
        except Exception as e: print(f"Error: {e}")

    def complete_consultation(self):
        print("\n--- Complete Consultation ---")
        aid = input("Appointment ID: ").strip()
        try:
            self.service.mark_consultation_completed(aid)
            print("Consultation Marked as Completed.")
        except Exception as e: print(f"Error: {e}")

    # Legacy alias ref
    def diagnose_patient(self):
        self.record_consultation()
