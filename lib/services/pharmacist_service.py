from dao.impl.medicine_dao_impl import MedicineDAOImpl
from dao.impl.bill_dao_impl import BillDAOImpl
from models.medicine import Medicine
from models.bill import Bill
from validation.validators import Validators

class PharmacistService:
    def __init__(self):
        self.medicine_dao = MedicineDAOImpl()
        self.bill_dao = BillDAOImpl()

    def add_medicine(self, name, price, quantity, expiry_date, batch_no):
        err = Validators.validate_non_empty(name, "Medicine Name")
        if err: raise ValueError(err)
        if float(price) <= 0: raise ValueError("Price must be positive")
        if int(quantity) < 0: raise ValueError("Quantity cannot be negative")
        if not expiry_date: raise ValueError("Expiry Date is required")
        if not batch_no: raise ValueError("Batch No is required")

        medicine = Medicine(name=name, price=price, quantity=quantity, expiry_date=expiry_date, batch_no=batch_no)
        return self.medicine_dao.create_medicine(medicine)

    def view_medicines(self):
        return self.medicine_dao.get_all_medicines()

    def generate_bill(self, medicine_id, quantity, patient_id, appointment_id, discount, status, date):
        medicines = self.medicine_dao.get_all_medicines()
        target_med = None
        for med in medicines:
            if str(med.get_medicine_id()) == str(medicine_id):
                target_med = med
                break
        
        if not target_med:
            raise ValueError("Medicine not found")
        
        if target_med.get_quantity() < int(quantity):
            raise ValueError("Insufficient stock")
            
        self.medicine_dao.update_medicine_stock(medicine_id, quantity)
        total_amount = float(target_med.get_price()) * int(quantity)
        final_amount = total_amount - float(discount or 0)
        
        # Handle optional appointment_id
        app_id = int(appointment_id) if appointment_id else None

        bill = Bill(
            patient_id=int(patient_id),
            appointment_id=app_id,
            total_amount=total_amount,
            discount=float(discount or 0),
            final_amount=final_amount,
            status=status or 'Unpaid',
            date=date
        )
        return self.bill_dao.create_bill(bill)
