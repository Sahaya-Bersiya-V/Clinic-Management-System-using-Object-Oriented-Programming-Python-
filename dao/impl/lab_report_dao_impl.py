from dao.base.lab_report_dao import LabReportDAO
from DbConnection.db_singleton import DbConnection
from models.lab_report import LabReport

class LabReportDAOImpl(LabReportDAO):
    def __init__(self):
        self.db_connection = DbConnection()

    def create_report(self, report):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO lab_reports (patient_id, test_name, result, date) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (report.get_patient_id(), report.get_test_name(), report.get_result(), report.get_date()))
                report.set_report_id(cursor.lastrowid)
                return report
        except Exception as e:
            raise e

    def get_reports_by_patient(self, patient_id):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM lab_reports WHERE patient_id = %s"
                cursor.execute(sql, (patient_id,))
                results = cursor.fetchall()
                reports = []
                for row in results:
                    reports.append(LabReport(
                        report_id=row['report_id'],
                        patient_id=row['patient_id'],
                        test_name=row['test_name'],
                        result=row['result'],
                        date=row['date']
                    ))
                return reports
        except Exception as e:
            raise e
