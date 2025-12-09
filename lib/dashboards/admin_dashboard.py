from lib.services.admin_service import AdminService
import sys

class AdminDashboard:
    def __init__(self, user):
        self.user = user
        self.service = AdminService()

    def display(self):
        while True:
            print(f"\n--- Admin Dashboard ({self.user.get_username()}) ---")
            print("1. Add Staff")
            print("2. View All Staff")
            print("3. Remove/Deactivate Staff")
            print("4. Update Doctor Information")
            print("5. Remove Doctor")
            print("6. View Doctor List")
            print("7. Logout")
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.add_staff()
            elif choice == '2':
                self.view_staff()
            elif choice == '3':
                self.remove_deactivate_staff()
            elif choice == '4':
                self.update_doctor()
            elif choice == '5':
                self.remove_doctor()
            elif choice == '6':
                self.view_doctors()
            elif choice == '7':
                print("Logging out...")
                break
            else:
                print("Invalid choice.")

    def add_staff(self):
        print("\n--- Add Staff ---")
        name = input("Name: ").strip()

        # ------- Role Validation -------
        role = input("Role (Doctor/Receptionist/Pharmacist/LabTech): ").strip().lower()
        valid_roles = ["doctor", "receptionist", "pharmacist", "labtech"]

        if role not in valid_roles:
            print(f"Invalid role '{role}'. Allowed roles: {valid_roles}")
            return

        # ------- Contact Validation -------
        contact = input("Contact: ").strip()
        if not contact.isdigit() or len(contact) != 10:
            print("Invalid contact number. It must be exactly 10 digits.")
            return

        # ------- Username Validation -------
        username = input("Username: ").strip()

        # Must not be only digits
        if username.isdigit():
            print("Invalid username: Username cannot contain only numbers.")
            return

        # Optional: username format rule
        if not username.isalnum():
            print("Invalid username: Only letters and numbers allowed. No spaces or symbols.")
            return

        # ------- Password Validation -------
        password = input("Password: ").strip()
        if len(password) < 4:
            print("Password must be at least 4 characters long.")
            return

        try:
            self.service.add_staff(name, role, contact, username, password)
            print("Staff added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def view_staff(self):
        print("\n--- Staff List ---")
        try:
            staff_list = self.service.get_all_staff()
            for s in staff_list:
                print(f"ID: {s.get_staff_id()}, Name: {s.get_name()}, Role: {s.get_role()}, Contact: {s.get_contact()}")
        except Exception as e:
            print(f"Error: {e}")

    def remove_deactivate_staff(self):
        print("\n--- Remove/Deactivate Staff ---")
        staff_id = input("Enter Staff ID: ").strip()
        action = input("Deactivate (D) or Remove (R)? ").strip().upper()
        
        try:
            if action == 'D':
                self.service.deactivate_staff(staff_id)
                print("Staff deactivated (Login disabled).")
            elif action == 'R':
                confirm = input("Are you sure you want to permanently delete this staff? (y/n): ").lower()
                if confirm == 'y':
                    self.service.delete_staff(staff_id)
                    print("Staff removed permanently.")
            else:
                print("Invalid action.")
        except Exception as e:
            print(f"Error: {e}")

    def update_doctor(self):
        print("\n--- Update Doctor Information ---")
        staff_id = input("Enter Doctor ID: ").strip()
        try:
            staff = self.service.get_staff_by_id(staff_id)
            if not staff:
                print("Staff not found.")
                return
            
            if staff.get_role().lower() != 'doctor':
                print("ID belongs to a staff member who is NOT a doctor.")
                return

            print(f"Editing Doctor: {staff.get_name()}")
            print("Leave blank to keep current value.")
            
            name = input(f"Name ({staff.get_name()}): ").strip() or staff.get_name()
            contact = input(f"Contact ({staff.get_contact()}): ").strip() or staff.get_contact()
            specialization = input(f"Specialization ({staff.get_specialization()}): ").strip() or staff.get_specialization()
            
            staff.set_name(name)
            staff.set_contact(contact)
            staff.set_specialization(specialization)
            
            self.service.update_staff(staff)
            print("Doctor information updated.")
        except Exception as e:
            print(f"Error: {e}")

    def remove_doctor(self):
        print("\n--- Remove Doctor ---")
        staff_id = input("Enter Doctor ID: ").strip()
        try:
            staff = self.service.get_staff_by_id(staff_id)
            if not staff:
                print("Staff not found.")
                return
            
            if staff.get_role().lower() != 'doctor':
                print("ID belongs to a staff member who is NOT a doctor.")
                return
            
            confirm = input(f"Are you sure you want to remove Dr. {staff.get_name()}? (y/n): ").lower()
            if confirm == 'y':
                self.service.delete_staff(staff_id)
                print("Doctor removed.")
        except Exception as e:
            print(f"Error: {e}")

    def view_doctors(self):
        print("\n--- Doctor List ---")
        try:
            doctors = self.service.get_staff_by_role("doctor")
            if not doctors:
                print("No doctors found.")
            for doc in doctors:
                print(f"ID: {doc.get_staff_id()}, Name: {doc.get_name()}, Specialization: {doc.get_specialization()}, Contact: {doc.get_contact()}")
        except Exception as e:
            print(f"Error: {e}")
