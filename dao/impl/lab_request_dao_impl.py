from dao.base.lab_request_dao import LabRequestDAO
from DbConnection.db_singleton import DbConnection
from models.lab_request import LabRequest

class LabRequestDAOImpl(LabRequestDAO):
    def __init__(self):
        self.db_connection = DbConnection()

    def create_request(self, request):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO lab_requests (appointment_id, patient_id, test_id, technician_id, status, result, report_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (
                    request.get_appointment_id(),
                    request.get_patient_id(),
                    request.get_test_id(),
                    request.get_technician_id(),
                    request.get_status(),
                    request.get_result(),
                    request.get_report_date()
                ))
                request.set_request_id(cursor.lastrowid)
                return request
        except Exception as e:
            raise e

    def get_request_by_id(self, request_id):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM lab_requests WHERE request_id = %s"
                cursor.execute(sql, (request_id,))
                result = cursor.fetchone()
                if result:
                    return LabRequest(
                        request_id=result['request_id'],
                        appointment_id=result['appointment_id'],
                        patient_id=result['patient_id'],
                        test_id=result['test_id'],
                        technician_id=result['technician_id'],
                        status=result['status'],
                        result=result['result'],
                        report_date=result['report_date']
                    )
                return None
        except Exception as e:
            raise e

    def update_request(self, request):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE lab_requests SET status=%s, result=%s, report_date=%s WHERE request_id=%s"
                cursor.execute(sql, (request.get_status(), request.get_result(), request.get_report_date(), request.get_request_id()))
        except Exception as e:
            raise e
