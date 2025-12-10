from lib.services.receptionist_service import ReceptionistService

class ReceptionistDashboard:
    def __init__(self, user):
        self.user = user
        self.service = ReceptionistService()

    def display(self):
        while True:
            print(f"\n--- Receptionist Dashboard ({self.user.get_username()}) ---")
            print("1. Register Patient")
            print("2. Book Appointment")
            print("3. View All Patients")
            print("4. Generate Consultation Billing")
            print("5. Update Patient Details")
            print("6. Cancel Appointment")
            print("7. Search Patient Record")
            print("8. Print Billing Receipt")
            print("9. Check Doctor Availability")
            print("10. Patient Check-in")
            print("11. View Booked Appointments")
            print("12. View My Profile")
            print("13. Logout")
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.register_patient()
            elif choice == '2':
                self.book_appointment()
            elif choice == '3':
                self.view_patients()
            elif choice == '4':
                self.generate_bill()
            elif choice == '5':
                self.update_patient()
            elif choice == '6':
                self.cancel_appointment()
            elif choice == '7':
                self.search_patient()
            elif choice == '8':
                self.print_receipt()
            elif choice == '9':
                self.check_doctor_availability()
            elif choice == '10':
                self.check_in_patient()
            elif choice == '11':
                self.view_appointments()
            elif choice == '12':
                self.view_profile()
            elif choice == '13':
                break
            else:
                print("Invalid choice.")

    def register_patient(self):
        print("\n--- Register Patient ---")
        name = input("Name: ").strip()
        age = input("Age: ").strip()
        gender = input("Gender: ").strip()
        contact = input("Contact: ").strip()
        blood_group = input("Blood Group: ").strip()
        address = input("Address: ").strip()
        
        try:
            patient = self.service.register_patient(name, age, gender, contact, blood_group, address)
            print(f"Patient registered successfully. New Patient ID: {patient.get_patient_id()}")
            
            book_now = input("Book appointment for this patient now? (y/n): ").strip().lower()
            if book_now == 'y':
                self.book_appointment(patient_id=str(patient.get_patient_id()))
                
        except Exception as e:
            print(f"Error: {e}")

    def book_appointment(self, patient_id=None):
        print("\n--- Book Appointment ---")
        if not patient_id:
            patient_id = input("Patient ID: ").strip()
        
        # Fetch and show patient details first
        try:
            patient = self.service.get_patient_details(patient_id)
            if not patient:
                print("Patient not found. Please register first.")
                return
            print(f"Booking for: {patient.get_name()} | Contact: {patient.get_contact()}")
            
            confirm = input("Confirm patient details? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Booking cancelled.")
                return

        except Exception as e:
            print(f"Error fetching patient: {e}")
            return

        doctor_id = input("Doctor ID: ").strip()
        date = input("Date (YYYY-MM-DD): ").strip()
        
        try:
            self.service.book_appointment(patient_id, doctor_id, date)
            print(f"Appointment booked successfully for {patient.get_name()}.")
        except Exception as e:
            print(f"Error: {e}")

    def view_patients(self):
        print("\n--- Patient List ---")
        try:
            patients = self.service.get_all_patients()
            for p in patients:
                print(f"ID: {p.get_patient_id()}, Name: {p.get_name()}, Age: {p.get_age()}, Blood: {p.get_blood_group()}, Contact: {p.get_contact()}")
        except Exception as e:
            print(f"Error: {e}")

    def generate_bill(self):
        print("\n--- Generate Bill ---")
        try:
            pid = input("Patient ID: ")
            aid = input("Appointment ID: ")
            total = input("Total Amount: ")
            discount = input("Discount: ")
            bill = self.service.generate_bill(pid, aid, total, discount)
            print(f"Bill Generated! ID: {bill.get_bill_id()}, Final Amount: {bill.get_final_amount()}")
        except Exception as e: print(f"Error: {e}")

    def update_patient(self):
        print("\n--- Update Patient ---")
        try:
            pid = input("Patient ID: ")
            name = input("New Name: ")
            age = input("New Age: ")
            gender = input("New Gender: ")
            contact = input("New Contact: ")
            blood_group = input("New Blood Group: ")
            address = input("New Address: ")
            self.service.update_patient_details(pid, name, age, gender, contact, blood_group, address)
            print("Patient Details Updated.")
        except Exception as e: print(f"Error: {e}")

    def cancel_appointment(self):
        print("\n--- Cancel Appointment ---")
        try:
            aid = input("Appointment ID: ")
            self.service.cancel_appointment(aid)
            print("Appointment Cancelled.")
        except Exception as e: print(f"Error: {e}")

    def search_patient(self):
        print("\n--- Search Patient ---")
        try:
            query = input("Enter Name or Contact: ")
            patients = self.service.search_patient_record(query)
            for p in patients:
                print(f"ID: {p.get_patient_id()}, Name: {p.get_name()}, Contact: {p.get_contact()}, Blood: {p.get_blood_group()}")
        except Exception as e: print(f"Error: {e}")

    def print_receipt(self):
        print("\n--- Print Receipt ---")
        try:
            bid = input("Bill ID: ")
            bill = self.service.get_bill_receipt(bid)
            if bill:
                print(f"Receipt:\nBill ID: {bill.get_bill_id()}\nPatient ID: {bill.get_patient_id()}\nAmount: {bill.get_final_amount()}\nDate: {bill.get_date()}")
            else:
                print("Bill not found.")
        except Exception as e: print(f"Error: {e}")

    def check_doctor_availability(self):
        print("\n--- Check Doctor Availability ---")
        try:
            did = input("Doctor ID: ")
            apps = self.service.check_doctor_availability(did)
            if not apps:
                print("Doctor has no appointments.")
            else:
                print(f"Appointments for Doctor {did}:")
                for a in apps:
                    print(f"ID: {a.get_appointment_id()}, Date: {a.get_date()}, Status: {a.get_status()}")
        except Exception as e: print(f"Error: {e}")

    def check_in_patient(self):
        print("\n--- Check In Patient ---")
        try:
            aid = input("Appointment ID: ")
            self.service.check_in_patient(aid)
            print("Patient Checked In.")
        except Exception as e: print(f"Error: {e}")

    def view_appointments(self):
        print("\n--- Booked Appointments ---")
        try:
            appointments = self.service.get_all_appointments()
            if not appointments:
                print("No appointments found.")
            else:
                for a in appointments:
                    print(f"ID: {a.get_appointment_id()}, Patient ID: {a.get_patient_id()}, Doctor ID: {a.get_doctor_id()}, Date: {a.get_date()}, Status: {a.get_status()}")
        except Exception as e:
            print(f"Error: {e}")

    def view_profile(self):
        """
        Purpose: Displays the profile details of the currently logged-in Receptionist.
        Context: Called from self.display menu option 12.
        Calls: ReceptionistService.get_current_staff_profile
        """
        print("\n--- My Profile ---")
        try:
            profile = self.service.get_current_staff_profile(self.user.get_user_id())
            if profile:
                print(f"Name: {profile.get_name()}")
                print(f"Role: {profile.get_role()}")
                print(f"Contact: {profile.get_contact()}")
                if profile.get_specialization():
                    print(f"Specialization: {profile.get_specialization()}")
                print(f"Shift: {profile.get_shift_start()} - {profile.get_shift_end()}")
            else:
                print("Profile details not found.")
        except Exception as e:
            print(f"Error: {e}")
