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
            print("4. Logout")
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.add_medicine()
            elif choice == '2':
                self.view_medicines()
            elif choice == '3':
                self.generate_bill()
            elif choice == '4':
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

    def generate_bill(self):
        print("\n--- Generate Bill ---")
        med_id = input("Medicine ID: ").strip()
        qty = input("Quantity: ").strip()
        
        try:
            total = self.service.generate_bill(med_id, qty)
            print(f"Bill Generated. Total Amount: {total}")
        except Exception as e:
            print(f"Error: {e}")
