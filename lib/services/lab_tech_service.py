from dao.impl.lab_report_dao_impl import LabReportDAOImpl
from models.lab_report import LabReport
from validation.validators import Validators
import datetime

class LabTechService:
    def __init__(self):
        self.lab_report_dao = LabReportDAOImpl()

    def add_test_result(self, patient_id, test_name, result):
        err = Validators.validate_id(patient_id)
        if err: raise ValueError(err)
        err = Validators.validate_non_empty(test_name, "Test Name")
        if err: raise ValueError(err)
        err = Validators.validate_non_empty(result, "Result")
        if err: raise ValueError(err)

        report = LabReport(patient_id=patient_id, test_name=test_name, result=result, date=datetime.date.today())
        return self.lab_report_dao.create_report(report)

    def view_patient_reports(self, patient_id):
        return self.lab_report_dao.get_reports_by_patient(patient_id)

    def get_available_tests(self):
        return self.lab_report_dao.get_all_tests()

    def add_new_test(self, test_name, cost):
        err = Validators.validate_non_empty(test_name, "Test Name")
        if err: raise ValueError(err)
        if float(cost) < 0: raise ValueError("Cost must be positive")
        self.lab_report_dao.add_lab_test(test_name, cost)

    def get_pending_lab_requests(self):
        return self.lab_report_dao.get_pending_requests()

    def update_request_status(self, request_id, status):
        # Notify Doctor functionality is implicit via status update.
        if status not in ['Pending', 'Processing', 'Completed']:
            raise ValueError("Invalid Status")
        self.lab_report_dao.update_request_status(request_id, status)

    def update_lab_report(self, request_id, result):
        # Re-upload or Correct Lab Test Report
        err = Validators.validate_non_empty(result, "Result")
        if err: raise ValueError(err)
        self.lab_report_dao.update_test_result(request_id, result)
