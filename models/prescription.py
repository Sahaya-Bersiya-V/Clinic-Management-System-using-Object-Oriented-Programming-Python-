class Prescription:
    def __init__(self, prescription_id=None, appointment_id=None, medicine_id=None, dosage=None, duration=None, quantity=None):
        self.__prescription_id = prescription_id
        self.__appointment_id = appointment_id
        self.__medicine_id = medicine_id
        self.__dosage = dosage
        self.__duration = duration
        self.__quantity = quantity

    def get_prescription_id(self): return self.__prescription_id
    def set_prescription_id(self, prescription_id): self.__prescription_id = prescription_id
    def get_appointment_id(self): return self.__appointment_id
    def set_appointment_id(self, appointment_id): self.__appointment_id = appointment_id
    def get_medicine_id(self): return self.__medicine_id
    def set_medicine_id(self, medicine_id): self.__medicine_id = medicine_id
    def get_dosage(self): return self.__dosage
    def set_dosage(self, dosage): self.__dosage = dosage
    def get_duration(self): return self.__duration
    def set_duration(self, duration): self.__duration = duration
    def get_quantity(self): return self.__quantity
    def set_quantity(self, quantity): self.__quantity = quantity
