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
                # Get test_id from test_name
                cursor.execute("SELECT test_id FROM lab_tests WHERE test_name = %s", (report.get_test_name(),))
                test_row = cursor.fetchone()
                if not test_row:
                    raise ValueError(f"Test '{report.get_test_name()}' not found in catalog.")
                test_id = test_row['test_id']

                sql = "INSERT INTO lab_requests (patient_id, test_id, result, report_date, status) VALUES (%s, %s, %s, %s, 'Completed')"
                cursor.execute(sql, (report.get_patient_id(), test_id, report.get_result(), report.get_date()))
                report.set_report_id(cursor.lastrowid)
                return report
        except Exception as e:
            raise e

    def get_reports_by_patient(self, patient_id):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT lr.request_id, lr.patient_id, lt.test_name, lr.result, lr.report_date
                    FROM lab_requests lr
                    JOIN lab_tests lt ON lr.test_id = lt.test_id
                    WHERE lr.patient_id = %s AND lr.status = 'Completed'
                """
                cursor.execute(sql, (patient_id,))
                results = cursor.fetchall()
                reports = []
                for row in results:
                    reports.append(LabReport(
                        report_id=row['request_id'],
                        patient_id=row['patient_id'],
                        test_name=row['test_name'],
                        result=row['result'],
                        date=row['report_date']
                    ))
                return reports
        except Exception as e:
            raise e

    def get_all_tests(self):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT test_name FROM lab_tests")
                results = cursor.fetchall()
                return [row['test_name'] for row in results]
        except Exception as e:
            raise e
