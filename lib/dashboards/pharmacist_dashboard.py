from lib.services.pharmacist_service import PharmacistService

class PharmacistDashboard:
    def __init__(self, user):
        self.user = user
        self.service = PharmacistService()

    def display(self):
        while True:
            print(f"\n--- Pharmacist Dashboard ({self.user.get_username()}) ---")
            print("1. Add Medicine")
            print("2. View Medicines")
            print("3. Generate Bill")
            print("4. Search Medicine")
            print("5. Update Medicine Inventory")
            print("6. Check Low Stock")
            print("7. Check Expiry Tracking")
            print("8. View Prescriptions")
            print("9. Logout")
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.add_medicine()
            elif choice == '2':
                self.view_medicines()
            elif choice == '3':
                self.generate_bill()
            elif choice == '4':
                self.search_medicines_ui()
            elif choice == '5':
                self.update_medicine_ui()
            elif choice == '6':
                self.check_low_stock_ui()
            elif choice == '7':
                self.check_expiry_ui()
            elif choice == '8':
                self.view_prescriptions_ui()
            elif choice == '9':
                break
            else:
                print("Invalid choice.")

    def add_medicine(self):
        print("\n--- Add Medicine ---")
        name = input("Name: ").strip()
        price = input("Price: ").strip()
        quantity = input("Quantity: ").strip()
        expiry_date = input("Expiry Date (YYYY-MM-DD): ").strip()
        batch_no = input("Batch No: ").strip()
        
        try:
            self.service.add_medicine(name, price, quantity, expiry_date, batch_no)
            print("Medicine added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def view_medicines(self):
        print("\n--- Medicine List ---")
        try:
            meds = self.service.view_medicines()
            for m in meds:
                print(f"ID: {m.get_medicine_id()}, Name: {m.get_name()}, Price: {m.get_price()}, Qty: {m.get_quantity()}, Expiry: {m.get_expiry_date()}, Batch: {m.get_batch_no()}")
        except Exception as e:
            print(f"Error: {e}")

    def search_medicines_ui(self):
        query = input("Enter search term (Name or Batch No): ").strip()
        try:
            meds = self.service.search_medicines(query)
            print(f"\nFound {len(meds)} matches:")
            for m in meds:
                print(f"ID: {m.get_medicine_id()}, Name: {m.get_name()}, Batch: {m.get_batch_no()}, Qty: {m.get_quantity()}")
        except Exception as e:
            print(f"Error: {e}")

    def update_medicine_ui(self):
        print("\n--- Update Medicine ---")
        med_id = input("Medicine ID to update: ").strip()
        # ideally retrieve it first, but for simplicity ask for all details
        name = input("New Name: ").strip()
        price = input("New Price: ").strip()
        quantity = input("New Quantity: ").strip()
        expiry_date = input("New Expiry Date (YYYY-MM-DD): ").strip()
        batch_no = input("New Batch No: ").strip()
        
        try:
            self.service.update_medicine(med_id, name, price, quantity, expiry_date, batch_no)
            print("Medicine updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def check_low_stock_ui(self):
        print("\n--- Low Stock Alert ---")
        try:
            meds = self.service.check_low_stock()
            if not meds:
                print("No medicines are low on stock.")
            else:
                for m in meds:
                     print(f"[ALERT] ID: {m.get_medicine_id()}, Name: {m.get_name()}, Qty: {m.get_quantity()}")
        except Exception as e:
            print(f"Error: {e}")

    def check_expiry_ui(self):
        print("\n--- Expiry Tracking (Next 30 Days) ---")
        try:
            meds = self.service.check_expiry()
            if not meds:
                print("No medicines expiring soon.")
            else:
                 for m in meds:
                     print(f"[ALERT] ID: {m.get_medicine_id()}, Name: {m.get_name()}, Expiry: {m.get_expiry_date()}")
        except Exception as e:
            print(f"Error: {e}")

    def view_prescriptions_ui(self):
        pid = input("Enter Patient ID: ").strip()
        try:
            prescriptions = self.service.view_prescriptions(pid)
            if not prescriptions:
                print("No prescriptions found for this patient.")
            else:
                for p in prescriptions:
                    print(f"Date: {p['date']}, Doctor: {p['doctor']}, Prescription: {p['prescription']}")
        except Exception as e:
            print(f"Error: {e}")

    def generate_bill(self):
        print("\n--- Generate Bill ---")
        patient_id = input("Patient ID: ").strip()
        
        # Check for returning patient
        try:
            is_returning = self.service.is_returning_patient(patient_id)
            if is_returning:
                print("\n*** Returning Patient Detected! ***")
                print("Consider applying a discount.")
        except Exception:
            pass # ignore if patient id invalid for this check, service will catch later

        appointment_id = input("Appointment ID (Optional, press Enter to skip): ").strip()
        med_id = input("Medicine ID: ").strip()
        qty = input("Quantity: ").strip()
        discount = input("Discount (0 if none): ").strip()
        status = input("Status (Paid/Unpaid): ").strip()
        # Date is auto-set to today
        
        try:
            bill = self.service.generate_bill(med_id, qty, patient_id, appointment_id, discount, status)
            print(f"Bill Generated Successfully.")
            print(f"Bill ID: {bill.get_bill_id()}")
            print(f"Total Amount: {bill.get_total_amount()}")
            print(f"Discount: {bill.get_discount()}")
            print(f"Final Amount: {bill.get_final_amount()}")
        except Exception as e:
            print(f"Error: {e}")
