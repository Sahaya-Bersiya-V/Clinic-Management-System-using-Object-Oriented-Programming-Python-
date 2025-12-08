class LabReport:
    def __init__(self, report_id=None, patient_id=None, test_name=None, result=None, date=None):
        self.__report_id = report_id
        self.__patient_id = patient_id
        self.__test_name = test_name
        self.__result = result
        self.__date = date

    def get_report_id(self):
        return self.__report_id

    def set_report_id(self, report_id):
        self.__report_id = report_id

    def get_patient_id(self):
        return self.__patient_id

    def set_patient_id(self, patient_id):
        self.__patient_id = patient_id

    def get_test_name(self):
        return self.__test_name

    def set_test_name(self, test_name):
        self.__test_name = test_name

    def get_result(self):
        return self.__result

    def set_result(self, result):
        self.__result = result

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date
