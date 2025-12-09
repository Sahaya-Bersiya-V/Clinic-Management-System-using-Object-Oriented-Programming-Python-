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
    def get_all_tests(self):
        pass
