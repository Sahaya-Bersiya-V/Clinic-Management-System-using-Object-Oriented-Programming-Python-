from dao.base.bill_dao import BillDAO
from DbConnection.db_singleton import DbConnection
from models.bill import Bill

class BillDAOImpl(BillDAO):
    def __init__(self):
        self.db_connection = DbConnection()

    def create_bill(self, bill):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO bills (patient_id, appointment_id, total_amount, discount, final_amount, status, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (
                    bill.get_patient_id(),
                    bill.get_appointment_id(),
                    bill.get_total_amount(),
                    bill.get_discount(),
                    bill.get_final_amount(),
                    bill.get_status(),
                    bill.get_date()
                ))
                bill.set_bill_id(cursor.lastrowid)
                return bill
        except Exception as e:
            raise e

    def get_bill_by_id(self, bill_id):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM bills WHERE bill_id = %s"
                cursor.execute(sql, (bill_id,))
                result = cursor.fetchone()
                if result:
                    return Bill(
                        bill_id=result['bill_id'],
                        patient_id=result['patient_id'],
                        appointment_id=result['appointment_id'],
                        total_amount=result['total_amount'],
                        discount=result['discount'],
                        final_amount=result['final_amount'],
                        status=result['status'],
                        date=result['date']
                    )
                return None
        except Exception as e:
            raise e
