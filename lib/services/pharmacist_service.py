from dao.impl.medicine_dao_impl import MedicineDAOImpl
from dao.impl.bill_dao_impl import BillDAOImpl
from dao.impl.appointment_dao_impl import AppointmentDAOImpl
from dao.impl.patient_dao_impl import PatientDAOImpl
from dao.impl.staff_dao_impl import StaffDAOImpl
from models.medicine import Medicine
from models.bill import Bill
from validation.validators import Validators
import datetime

class PharmacistService:
    def __init__(self):
        self.medicine_dao = MedicineDAOImpl()
        self.bill_dao = BillDAOImpl()
        self.appointment_dao = AppointmentDAOImpl()
        self.patient_dao = PatientDAOImpl()
        self.staff_dao = StaffDAOImpl()

    def add_medicine(self, name, price, quantity, expiry_date, batch_no):
        err = Validators.validate_non_empty(name, "Medicine Name")
        if err: raise ValueError(err)
        if float(price) <= 0: raise ValueError("Price must be positive")
        if int(quantity) < 0: raise ValueError("Quantity cannot be negative")
        if not expiry_date: raise ValueError("Expiry Date is required")
        err = Validators.validate_future_date(expiry_date)
        if err: raise ValueError(f"Expiry Date Error: {err}")
        if not batch_no: raise ValueError("Batch No is required")

        medicine = Medicine(name=name, price=price, quantity=quantity, expiry_date=expiry_date, batch_no=batch_no)
        return self.medicine_dao.create_medicine(medicine)

    def update_medicine(self, medicine_id, name, price, quantity, expiry_date, batch_no):
        medicine = self.medicine_dao.get_medicine_by_id(medicine_id)
        if not medicine: raise ValueError("Medicine not found")

        if name and name.strip(): medicine.set_name(name)
        if price and str(price).strip():
             if float(price) <= 0: raise ValueError("Price must be positive")
             medicine.set_price(price)
        if quantity and str(quantity).strip():
             if int(quantity) < 0: raise ValueError("Quantity cannot be negative")
             medicine.set_quantity(quantity)
        if expiry_date and str(expiry_date).strip():
             err = Validators.validate_future_date(expiry_date)
             if err: raise ValueError(f"Expiry Date Error: {err}")
             medicine.set_expiry_date(expiry_date)
        if batch_no and str(batch_no).strip():
             medicine.set_batch_no(batch_no)

        self.medicine_dao.update_medicine(medicine)

    def view_medicines(self):
        return self.medicine_dao.get_all_medicines()

    def search_medicines(self, query):
        return self.medicine_dao.search_medicines(query)

    def check_low_stock(self):
        return self.medicine_dao.get_low_stock_medicines()

    def check_expiry(self, days_threshold=30):
        target_date = datetime.date.today() + datetime.timedelta(days=days_threshold)
        return self.medicine_dao.get_expiring_medicines(target_date)

    def view_prescriptions(self, patient_id):
        # We assume prescriptions are part of Appointment details
        appointments = self.appointment_dao.get_appointments_by_patient(patient_id)
        # Filter appointments that have a prescription
        prescriptions = []
        for appt in appointments:
            if appt.get_prescription():
                prescriptions.append({
                    "appointment_id": appt.get_appointment_id(),
                    "date": appt.get_date(),
                    "doctor": appt.get_doctor_id(), # Ideally fetch name
                    "prescription": appt.get_prescription()
                })
        return prescriptions

    def is_returning_patient(self, patient_id):
        appointments = self.appointment_dao.get_appointments_by_patient(patient_id)
        return len(appointments) > 1

    def generate_bill(self, medicine_id, quantity, patient_id, appointment_id, discount, status):
        # Validate patient existence
        if not self.patient_dao.get_patient_by_id(patient_id):
            raise ValueError(f"Patient with ID {patient_id} not found.")
        
        # Validate appointment existence if provided
        if appointment_id:
            if not self.appointment_dao.get_appointment_by_id(appointment_id):
                raise ValueError(f"Appointment with ID {appointment_id} not found.")

        # Validate status
        if status not in ['Paid', 'Unpaid']:
            raise ValueError("Status must be 'Paid' or 'Unpaid'.")

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
        
        final_discount = float(discount or 0)
        # Auto-apply discount if returning patient and no manual discount provided? 
        # Or just trust the input. The prompt says "Apply Discount for Old/Returning Patient".
        # Let's assume the Dashboard handles the decision to apply it, or we apply a default if none is given.
        # Im implementing a check in Dashboard to suggest it. Here we just take the value.
        
        final_amount = total_amount - final_discount
        
        # Handle optional appointment_id
        app_id = int(appointment_id) if appointment_id else None

        bill = Bill(
            patient_id=int(patient_id),
            appointment_id=app_id,
            total_amount=total_amount,
            discount=final_discount,
            final_amount=final_amount,
            status=status or 'Unpaid',
            date=str(datetime.date.today())
        )
        return self.bill_dao.create_bill(bill)

    def get_current_staff_profile(self, user_id):
        return self.staff_dao.get_staff_by_user_id(user_id)

    def get_all_patients(self):
        return self.patient_dao.get_all_patients()
