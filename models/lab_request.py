class LabRequest:
    def __init__(self, request_id=None, appointment_id=None, patient_id=None, test_id=None, technician_id=None, status='Pending', result=None, report_date=None):
        self.__request_id = request_id
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__test_id = test_id
        self.__technician_id = technician_id
        self.__status = status
        self.__result = result
        self.__report_date = report_date

    def get_request_id(self): return self.__request_id
    def set_request_id(self, request_id): self.__request_id = request_id
    def get_appointment_id(self): return self.__appointment_id
    def set_appointment_id(self, appointment_id): self.__appointment_id = appointment_id
    def get_patient_id(self): return self.__patient_id
    def set_patient_id(self, patient_id): self.__patient_id = patient_id
    def get_test_id(self): return self.__test_id
    def set_test_id(self, test_id): self.__test_id = test_id
    def get_technician_id(self): return self.__technician_id
    def set_technician_id(self, technician_id): self.__technician_id = technician_id
    def get_status(self): return self.__status
    def set_status(self, status): self.__status = status
    def get_result(self): return self.__result
    def set_result(self, result): self.__result = result
    def get_report_date(self): return self.__report_date
    def set_report_date(self, report_date): self.__report_date = report_date
