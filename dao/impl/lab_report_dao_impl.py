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
                
                # Also insert into lab_reports table as requested
                sql_report = "INSERT INTO lab_reports (patient_id, test_name, result, date) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_report, (report.get_patient_id(), report.get_test_name(), report.get_result(), report.get_date()))
                
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
                cursor.execute("SELECT test_id, test_name, cost FROM lab_tests")
                results = cursor.fetchall()
                # Return list of dicts
                return results
        except Exception as e:
            raise e

    def add_lab_test(self, test_name, cost):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO lab_tests (test_name, cost) VALUES (%s, %s)"
                cursor.execute(sql, (test_name, cost))
        except Exception as e:
            raise e

    def get_pending_requests(self):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT lr.request_id, lr.patient_id, lt.test_name, lr.status, lr.report_date
                    FROM lab_requests lr
                    JOIN lab_tests lt ON lr.test_id = lt.test_id
                    WHERE lr.status = 'Pending' OR lr.status = 'Processing'
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                # Return list of specialized objects or dicts using existing models if possible.
                # LabReport fits best for result view, LabRequest for status view. 
                # Let's return list of dicts or loose objects for simplicity if Model doesn't perfectly fit or LabRequest is better.
                # Using LabRequest but we need to fetch all fields to be pure. 
                # Let's return dicts for now to be flexible or LabReport with status.
                
                # Using a dict representation for Dashboard display
                requests = []
                for row in results:
                    requests.append({
                        "request_id": row['request_id'],
                        "patient_id": row['patient_id'],
                        "test_name": row['test_name'],
                        "status": row['status'],
                        "date": row['report_date']
                    })
                return requests
        except Exception as e:
            raise e

    def update_request_status(self, request_id, status):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE lab_requests SET status = %s WHERE request_id = %s"
                cursor.execute(sql, (status, request_id))
        except Exception as e:
            raise e

    def update_test_result(self, request_id, result):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Also set date to today when correcting/uploading result? Yes.
                import datetime
                today = datetime.date.today()
                
                # Update request
                sql = "UPDATE lab_requests SET result = %s, report_date = %s, status = 'Completed' WHERE request_id = %s"
                cursor.execute(sql, (result, today, request_id))
                
                # Fetch details to insert into lab_reports
                sql_get = """
                    SELECT lr.patient_id, lt.test_name 
                    FROM lab_requests lr
                    JOIN lab_tests lt ON lr.test_id = lt.test_id
                    WHERE lr.request_id = %s
                """
                cursor.execute(sql_get, (request_id,))
                row = cursor.fetchone()
                
                if row:
                     sql_report = "INSERT INTO lab_reports (patient_id, test_name, result, date) VALUES (%s, %s, %s, %s)"
                     cursor.execute(sql_report, (row['patient_id'], row['test_name'], result, today))
        except Exception as e:
            raise e
