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
            print("4. Logout")
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.register_patient()
            elif choice == '2':
                self.book_appointment()
            elif choice == '3':
                self.view_patients()
            elif choice == '4':
                break
            else:
                print("Invalid choice.")

    def register_patient(self):
        print("\n--- Register Patient ---")
        name = input("Name: ").strip()
        age = input("Age: ").strip()
        gender = input("Gender: ").strip()
        contact = input("Contact: ").strip()
        
        try:
            self.service.register_patient(name, age, gender, contact)
            print("Patient registered successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def book_appointment(self):
        print("\n--- Book Appointment ---")
        patient_id = input("Patient ID: ").strip()
        doctor_id = input("Doctor ID: ").strip()
        date = input("Date (YYYY-MM-DD): ").strip()
        
        try:
            self.service.book_appointment(patient_id, doctor_id, date)
            print("Appointment booked successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def view_patients(self):
        print("\n--- Patient List ---")
        try:
            patients = self.service.get_all_patients()
            for p in patients:
                print(f"ID: {p.get_patient_id()}, Name: {p.get_name()}, Age: {p.get_age()}, Contact: {p.get_contact()}")
        except Exception as e:
            print(f"Error: {e}")
