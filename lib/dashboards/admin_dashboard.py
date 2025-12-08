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
            print("3. Logout")
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.add_staff()
            elif choice == '2':
                self.view_staff()
            elif choice == '3':
                print("Logging out...")
                break
            else:
                print("Invalid choice.")

    def add_staff(self):
        print("\n--- Add Staff ---")
        name = input("Name: ").strip()
        role = input("Role (Doctor/Receptionist/Pharmacist/LabTech): ").strip()
        contact = input("Contact: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
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
