from lib.auth import AuthService
from lib.dashboards.admin_dashboard import AdminDashboard
from lib.dashboards.receptionist_dashboard import ReceptionistDashboard
from lib.dashboards.doctor_dashboard import DoctorDashboard
from lib.dashboards.pharmacist_dashboard import PharmacistDashboard
from lib.dashboards.lab_tech_dashboard import LabTechDashboard
import sys

def main():
    auth_service = AuthService()

    while True:
        print("\n=========== Clinic Management System ===========")
        print()
        print("1. Login")
        print("2. Exit")
        print("="*25)
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            print()
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            try:
                user = auth_service.login(username, password)
                role = user.get_role().lower()
                
                if role == 'admin':
                    dashboard = AdminDashboard(user)
                elif role == 'receptionist':
                    dashboard = ReceptionistDashboard(user)
                elif role == 'doctor':
                    dashboard = DoctorDashboard(user)
                elif role == 'pharmacist':
                    dashboard = PharmacistDashboard(user)
                elif role == 'labtech':
                    dashboard = LabTechDashboard(user)
                else:
                    print("Unknown role.")
                    continue
                
                dashboard.display()
                
            except Exception as e:
                print(f"Login Failed: {e}")
                
        elif choice == '2':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
