from lib.services.admin_service import AdminService
import sys

class AdminDashboard:
    def __init__(self, user):
        self.user = user
        self.service = AdminService()

    def display(self):
        """
        Purpose: Displays the main menu for the Admin Dashboard and handles user input routing.
        Context: Called by main.py after successful admin login.
        Calls: self.add_staff, self.view_staff_menu, self.update_staff_menu, etc.
        """
        while True:
            print(f"\n--- Admin Dashboard ({self.user.get_username()}) ---")
            print("="*25)
            print("1. Add Staff")
            print("2. View Staff")
            print("3. Edit/Remove Staff")
            print("4. Logout")
            print("*"*25)
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.add_staff()
            elif choice == '2':
                self.view_staff_menu()
            elif choice == '3':
                self.update_staff_menu()
            elif choice == '4':
                print("Logging out...")
                break
            else:
                print("Invalid choice.")

    def add_staff(self):
        print("\n--- Add Staff ---")
        print("="*25)
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

        # ------- Additional Details -------
        specialization = None
        if role == 'doctor':
             specialization = input("Specialization: ").strip()
        else:
             specialization = input("Specialization (Optional): ").strip() or None

        shift_start = input("Shift Start (HH:MM:SS, Optional): ").strip() or None
        shift_end = input("Shift End (HH:MM:SS, Optional): ").strip() or None

        try:
            self.service.add_staff(name, role, contact, username, password, specialization, shift_start, shift_end)
            print("Staff added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def view_staff_menu(self):
        """
        Purpose: Sub-menu for viewing staff members, allowing filtering by role.
        Context: Called from display() option 2.
        Calls: AdminService.get_all_staff, AdminService.get_staff_by_role
        """
        print("\n--- View Staff ---")
        print("1. All Staff")
        print("2. Doctors")
        print("3. Pharmacists")
        print("4. Lab Technicians")
        print("5. Receptionists")
        print("6. Back")
        
        choice = input("Filter by: ").strip()
        
        try:
            staff_list = []
            if choice == '1':
                staff_list = self.service.get_all_staff()
            elif choice == '2':
                staff_list = self.service.get_staff_by_role('doctor')
            elif choice == '3':
                staff_list = self.service.get_staff_by_role('pharmacist')
            elif choice == '4':
                staff_list = self.service.get_staff_by_role('labtech')
            elif choice == '5':
                staff_list = self.service.get_staff_by_role('receptionist')
            elif choice == '6':
                return
            else:
                print("Invalid choice.")
                return

            if not staff_list:
                print("No staff records found for this category.")
            else:
                for s in staff_list:
                    print(f"ID: {s.get_staff_id()}, Name: {s.get_name()}, Role: {s.get_role()}, Contact: {s.get_contact()}, Spec: {s.get_specialization()}")
        except Exception as e:
            print(f"Error fetching staff: {e}")

    def update_staff_menu(self):
        """
        Purpose: UI to update any staff member's details or remove/deactivate them.
        Context: Called from display() option 3.
        Calls: AdminService.get_staff_by_role (to list options), AdminService.update_staff, AdminService.delete_staff
        """
        print("\n--- Update/Remove Staff ---")
        print("Select Role to Update:")
        print("1. Doctors")
        print("2. Pharmacists")
        print("3. Lab Technicians")
        print("4. Receptionists")
        print("5. Back")
        
        choice = input("Select Role: ").strip()
        role_filter = ""
        if choice == '1': role_filter = 'doctor'
        elif choice == '2': role_filter = 'pharmacist'
        elif choice == '3': role_filter = 'labtech'
        elif choice == '4': role_filter = 'receptionist'
        elif choice == '5': return
        else:
            print("Invalid choice.")
            return

        # Show list for convenience
        try:
            staff_list = self.service.get_staff_by_role(role_filter)
            print(f"\n--- {role_filter.capitalize()} List ---")
            for s in staff_list:
                    print(f"ID: {s.get_staff_id()}, Name: {s.get_name()}")
        except Exception as e:
            print(f"Error listing staff: {e}")
            return

        staff_id = input("\nEnter Staff ID to update/remove: ").strip()
        if not staff_id: return

        try:
            staff = self.service.get_staff_by_id(staff_id)
            if not staff:
                print("Staff not found.")
                return
            
            # Additional check to ensure we aren't editing a pharmacist when we selected Doctor menu (though ID is unique)
            if staff.get_role().lower() != role_filter:
                print(f"Warning: This staff member is a {staff.get_role()}, not a {role_filter}.")
                confirm = input("Continue anyway? (y/n): ").lower()
                if confirm != 'y': return

            print("\nActions:")
            print("1. Update Details")
            print("2. Remove/Deactivate")
            action = input("Choice: ").strip()

            if action == '1':
                print(f"Editing {staff.get_role()}: {staff.get_name()}")
                print("Leave blank to keep current value.")
                
                name = input(f"Name ({staff.get_name()}): ").strip() or staff.get_name()
                contact = input(f"Contact ({staff.get_contact()}): ").strip() or staff.get_contact()
                spec = input(f"Specialization ({staff.get_specialization()}): ").strip() or staff.get_specialization()
                
                s_start = input(f"Shift Start ({staff.get_shift_start()}): ").strip() or staff.get_shift_start()
                s_end = input(f"Shift End ({staff.get_shift_end()}): ").strip() or staff.get_shift_end()
                
                staff.set_name(name)
                staff.set_contact(contact)
                staff.set_specialization(spec)
                staff.set_shift_start(s_start)
                staff.set_shift_end(s_end)
                
                self.service.update_staff(staff)
                print("Staff information updated.")

            elif action == '2':
               sub = input("Deactivate (D) or Remove (R)? ").strip().upper()
               if sub == 'D':
                   self.service.deactivate_staff(staff_id)
                   print("Staff deactivated.")
               elif sub == 'R':
                   sure = input("Permanently delete? (y/n): ").lower()
                   if sure == 'y':
                       self.service.delete_staff(staff_id)
                       print("Staff deleted.")
            else:
                print("Invalid action.")

        except Exception as e:
            print(f"Error: {e}")
