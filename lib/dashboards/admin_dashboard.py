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

    # ------- Role Validation -------
        role = input("Role (Doctor/Receptionist/Pharmacist/LabTech): ").strip().lower()
        valid_roles = ["doctor", "receptionist", "pharmacist", "labtech"]

        if role not in valid_roles:
            print(f"❌ Invalid role '{role}'. Allowed roles: {valid_roles}")
            return

    # ------- Contact Validation -------
        contact = input("Contact: ").strip()
        if not contact.isdigit() or len(contact) != 10:
            print("❌ Invalid contact number. It must be exactly 10 digits.")
            return

    # ------- Username Validation -------
        username = input("Username: ").strip()

    # Must not be only digits
        if username.isdigit():
            print("❌ Invalid username: Username cannot contain only numbers.")
            return

    # Optional: username format rule
        if not username.isalnum():
            print("❌ Invalid username: Only letters and numbers allowed. No spaces or symbols.")
            return

    # ------- Password Validation -------
        # password = input("Password: ").strip()
        if len(password) < 4:
            print("❌ Password must be at least 4 characters long.")
            return

        try:
            self.service.add_staff(name, role, contact, username, password)
            print("✔️ Staff added successfully.")
        except Exception as e:
            print(f"❌ Error: {e}")



    def view_staff(self):
        print("\n--- Staff List ---")
        try:
            staff_list = self.service.get_all_staff()
            for s in staff_list:
                print(f"ID: {s.get_staff_id()}, Name: {s.get_name()}, Role: {s.get_role()}, Contact: {s.get_contact()}")
        except Exception as e:
            print(f"Error: {e}")
