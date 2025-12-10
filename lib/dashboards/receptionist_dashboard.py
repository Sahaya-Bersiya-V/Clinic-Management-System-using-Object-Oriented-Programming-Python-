from lib.services.receptionist_service import ReceptionistService

class ReceptionistDashboard:
    def __init__(self, user):
        self.user = user
        self.service = ReceptionistService()

    def _print_table(self, title, headers, rows):
        if not rows:
            print(f"\n   No data available for {title}.")
            return

        # Calculate widths
        widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))

        # Spacing padding
        ws = [w + 2 for w in widths]

        # Lines using box drawing chars
        top = "╔" + "╤".join(["═" * w for w in ws]) + "╗"
        head_sep = "╠" + "╪".join(["═" * w for w in ws]) + "╣"
        bot = "╚" + "╧".join(["═" * w for w in ws]) + "╝"
        
        print(f"\n   {title}")
        print("  " + top)
        
        # Header
        header_content = "║" + "│".join([f" {str(h):<{widths[i]}} " for i, h in enumerate(headers)]) + "║"
        print("  " + header_content)
        print("  " + head_sep)
        
        # Rows
        for row in rows:
            row_content = "║" + "│".join([f" {str(c):<{widths[i]}} " for i, c in enumerate(row)]) + "║"
            print("  " + row_content)
            
        print("  " + bot)

    def _prompt_patient_id(self):
        while True:
            pid = input("   Patient ID (Enter 'S' to search, 'L' to list all): ").strip()
            if pid.upper() == 'S':
                self.search_patient()
            elif pid.upper() == 'L':
                self.view_patients()
            elif pid:
                return pid

    def _prompt_doctor_id(self):
        while True:
            did = input("   Doctor ID (Enter 'L' to list all doctors): ").strip()
            if did.upper() == 'L':
                    try:
                        doctors = self.service.get_doctor_list()
                        headers = ["ID", "Name", "Specialization"]
                        rows = [[d.get_staff_id(), d.get_name(), d.get_specialization()] for d in doctors]
                        self._print_table("Doctor List", headers, rows)
                    except Exception as e:
                        print(f"   Error fetching doctors: {e}")
            elif did:
                return did

    def _prompt_appointment_id(self):
        while True:
            aid = input("   Appointment ID (Enter 'L' to list all): ").strip()
            if aid.upper() == 'L':
                self.view_appointments()
            elif aid:
                return aid

    def display(self):
        while True:
            print("\n" + "═" * 60)
            print(f"   RECEPTIONIST DASHBOARD  ({self.user.get_username()})".center(60))
            print("═" * 60 + "\n")
            
            options = [
                ("1", "Register Patient"), ("2", "Book Appointment"),
                ("3", "View All Patients"), ("4", "Generate Consultation Billing"),
                ("5", "Update Patient Details"), ("6", "Cancel Appointment"),
                ("7", "Search Patient Record"), ("8", "Print Billing Receipt"),
                ("9", "Check Doctor Availability"), ("10", "Patient Check-in"),
                ("11", "View Booked Appointments"), ("12", "Logout")
            ]
            
            # Display options in a grid or columns
            for i in range(0, len(options), 2):
                opt1 = f"[ {options[i][0]:>2} ] {options[i][1]}"
                opt2 = ""
                if i + 1 < len(options):
                    opt2 = f"[ {options[i+1][0]:>2} ] {options[i+1][1]}"
                print(f"   {opt1:<35} {opt2}")
            
            print("\n" + "─" * 60)
            choice = input("   Enter choice: ").strip()

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
                break
            else:
                print("Invalid choice.")

    def register_patient(self):
        print(f"\n   REGISTER PATIENT")
        name = input("   Name: ").strip()
        age = input("   Age: ").strip()
        gender = input("   Gender: ").strip()
        contact = input("   Contact: ").strip()
        blood_group = input("   Blood Group: ").strip()
        address = input("   Address: ").strip()
        
        try:
            patient = self.service.register_patient(name, age, gender, contact, blood_group, address)
            print(f"Patient registered successfully. New Patient ID: {patient.get_patient_id()}")
            
            book_now = input("   Book appointment for this patient now? (y/n): ").strip().lower()
            if book_now == 'y':
                self.book_appointment(patient_id=str(patient.get_patient_id()))
                
        except Exception as e:
            print(f"Error: {e}")

    def book_appointment(self, patient_id=None):
        print(f"\n   BOOK APPOINTMENT")
        if not patient_id:
            patient_id = self._prompt_patient_id()
        
        # Fetch and show patient details first
        try:
            patient = self.service.get_patient_details(patient_id)
            if not patient:
                print("Patient not found. Please register first.")
                return
            print(f"Booking for: {patient.get_name()} | Contact: {patient.get_contact()}")
            
            confirm = input("   Confirm patient details? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Booking cancelled.")
                return

        except Exception as e:
            print(f"Error fetching patient: {e}")
            return

        doctor_id = self._prompt_doctor_id()
        date = input("   Date (YYYY-MM-DD): ").strip()
        
        try:
            self.service.book_appointment(patient_id, doctor_id, date)
            print(f"Appointment booked successfully for {patient.get_name()}.")
        except Exception as e:
            print(f"Error: {e}")

    def view_patients(self):
        try:
            patients = self.service.get_all_patients()
            headers = ["ID", "Name", "Age", "Blood", "Contact"]
            rows = [[p.get_patient_id(), p.get_name(), p.get_age(), p.get_blood_group(), p.get_contact()] for p in patients]
            self._print_table("Patient List", headers, rows)
        except Exception as e:
            print(f"   Error: {e}")

    def generate_bill(self):
        print(f"\n   GENERATE BILL")
        try:
            pid = self._prompt_patient_id()
            aid = self._prompt_appointment_id()
            total = input("   Total Amount: ")
            discount = input("   Discount: ")
            bill = self.service.generate_bill(pid, aid, total, discount)
            print(f"\n   Bill Generated Successfully!")
            print(f"      Bill ID:      {bill.get_bill_id()}")
            print(f"      Final Amount: {bill.get_final_amount()}")
        except Exception as e: print(f"   Error: {e}")

    def update_patient(self):
        print(f"\n   UPDATE PATIENT")
        try:
            pid = self._prompt_patient_id()
            name = input("   New Name: ")
            age = input("   New Age: ")
            gender = input("   New Gender: ")
            contact = input("   New Contact: ")
            blood_group = input("   New Blood Group: ")
            address = input("   New Address: ")
            self.service.update_patient_details(pid, name, age, gender, contact, blood_group, address)
            print("   Patient Details Updated.")
        except Exception as e: print(f"   Error: {e}")

    def cancel_appointment(self):
        print(f"\n   CANCEL APPOINTMENT")
        try:
            aid = self._prompt_appointment_id()
            self.service.cancel_appointment(aid)
            print("   Appointment Cancelled.")
        except Exception as e: print(f"   Error: {e}")

    def search_patient(self):
        print("\n   Search Patient")
        try:
            query = input("   Enter Name or Contact: ")
            patients = self.service.search_patient_record(query)
            headers = ["ID", "Name", "Contact", "Blood Group"]
            rows = [[p.get_patient_id(), p.get_name(), p.get_contact(), p.get_blood_group()] for p in patients]
            self._print_table("Search Results", headers, rows)
        except Exception as e: print(f"   Error: {e}")

    def print_receipt(self):
        print(f"\n   PRINT RECEIPT")
        try:
            bid = input("   Enter Bill ID: ")
            bill = self.service.get_bill_receipt(bid)
            if bill:
                print("\n   ╔════════════════════════════════╗")
                print("   ║           RECEIPT              ║")
                print("   ╠════════════════════════════════╣")
                print(f"   ║ Bill ID:    {str(bill.get_bill_id()):<18} ║")
                print(f"   ║ Patient ID: {str(bill.get_patient_id()):<18} ║")
                print(f"   ║ Amount:     {str(bill.get_final_amount()):<18} ║")
                print(f"   ║ Date:       {str(bill.get_date()):<18} ║")
                print("   ╚════════════════════════════════╝")
            else:
                print("   Bill not found.")
        except Exception as e: print(f"   Error: {e}")

    def check_doctor_availability(self):
        print(f"\n   CHECK DOCTOR AVAILABILITY")
        try:
            did = self._prompt_doctor_id()
            apps = self.service.check_doctor_availability(did)
            if not apps:
                print("   Doctor has no appointments.")
            else:
                headers = ["ID", "Date", "Status"]
                rows = [[a.get_appointment_id(), a.get_date(), a.get_status()] for a in apps]
                self._print_table(f"Appointments for Doctor {did}", headers, rows)
        except Exception as e: print(f"   Error: {e}")

    def check_in_patient(self):
        print(f"\n   CHECK IN PATIENT")
        try:
            aid = self._prompt_appointment_id()
            self.service.check_in_patient(aid)
            print("   Patient Checked In.")
        except Exception as e: print(f"   Error: {e}")

    def view_appointments(self):
        try:
            appointments = self.service.get_all_appointments()
            if not appointments:
                print("\n   No appointments found.")
            else:
                headers = ["ID", "Patient ID", "Doctor ID", "Date", "Status"]
                rows = [[a.get_appointment_id(), a.get_patient_id(), a.get_doctor_id(), a.get_date(), a.get_status()] for a in appointments]
                self._print_table("Booked Appointments", headers, rows)
        except Exception as e:
            print(f"   Error: {e}")
