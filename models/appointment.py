class Appointment:
    def __init__(self, appointment_id=None, patient_id=None, doctor_id=None, date=None, status=None, diagnosis=None, prescription=None):
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__date = date
        self.__status = status
        self.__diagnosis = diagnosis
        self.__prescription = prescription

    def get_appointment_id(self):
        return self.__appointment_id

    def set_appointment_id(self, appointment_id):
        self.__appointment_id = appointment_id

    def get_patient_id(self):
        return self.__patient_id

    def set_patient_id(self, patient_id):
        self.__patient_id = patient_id

    def get_doctor_id(self):
        return self.__doctor_id

    def set_doctor_id(self, doctor_id):
        self.__doctor_id = doctor_id

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_diagnosis(self):
        return self.__diagnosis

    def set_diagnosis(self, diagnosis):
        self.__diagnosis = diagnosis

    def get_prescription(self):
        return self.__prescription

    def set_prescription(self, prescription):
        self.__prescription = prescription
