from dao.base.medicine_dao import MedicineDAO
from DbConnection.db_singleton import DbConnection
from models.medicine import Medicine

class MedicineDAOImpl(MedicineDAO):
    def __init__(self):
        self.db_connection = DbConnection()

    def create_medicine(self, medicine):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO medicines (name, price, quantity, expiry_date, batch_no) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (medicine.get_name(), medicine.get_price(), medicine.get_quantity(), medicine.get_expiry_date(), medicine.get_batch_no()))
                medicine.set_medicine_id(cursor.lastrowid)
                return medicine
        except Exception as e:
            raise e

    def get_all_medicines(self):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM medicines"
                cursor.execute(sql)
                results = cursor.fetchall()
                medicines = []
                for row in results:
                    medicines.append(Medicine(
                        medicine_id=row['medicine_id'],
                        name=row['name'],
                        price=row['price'],
                        quantity=row['quantity'],
                        expiry_date=row['expiry_date'],
                        batch_no=row['batch_no']
                    ))
                return medicines
        except Exception as e:
            raise e

    def update_medicine_stock(self, medicine_id, quantity):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE medicines SET quantity = quantity - %s WHERE medicine_id = %s"
                cursor.execute(sql, (quantity, medicine_id))
        except Exception as e:
            raise e
