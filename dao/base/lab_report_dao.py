from abc import ABC, abstractmethod
from models.lab_report import LabReport

class LabReportDAO(ABC):
    @abstractmethod
    def create_report(self, report):
        pass

    @abstractmethod
    def get_reports_by_patient(self, patient_id):
        pass

    @abstractmethod
    def add_lab_test(self, test_name, cost):
        pass

    @abstractmethod
    def get_pending_requests(self):
        pass

    @abstractmethod
    def update_request_status(self, request_id, status):
        pass

    @abstractmethod
    def update_test_result(self, request_id, result):
        pass
