class Bill:
    def __init__(self, bill_id=None, patient_id=None, appointment_id=None, total_amount=0.0, discount=0.0, final_amount=0.0, status='Unpaid', date=None):
        self.__bill_id = bill_id
        self.__patient_id = patient_id
        self.__appointment_id = appointment_id
        self.__total_amount = total_amount
        self.__discount = discount
        self.__final_amount = final_amount
        self.__status = status
        self.__date = date

    def get_bill_id(self): return self.__bill_id
    def set_bill_id(self, bill_id): self.__bill_id = bill_id
    def get_patient_id(self): return self.__patient_id
    def set_patient_id(self, patient_id): self.__patient_id = patient_id
    def get_appointment_id(self): return self.__appointment_id
    def set_appointment_id(self, appointment_id): self.__appointment_id = appointment_id
    def get_total_amount(self): return self.__total_amount
    def set_total_amount(self, total_amount): self.__total_amount = total_amount
    def get_discount(self): return self.__discount
    def set_discount(self, discount): self.__discount = discount
    def get_final_amount(self): return self.__final_amount
    def set_final_amount(self, final_amount): self.__final_amount = final_amount
    def get_status(self): return self.__status
    def set_status(self, status): self.__status = status
    def get_date(self): return self.__date
    def set_date(self, date): self.__date = date
