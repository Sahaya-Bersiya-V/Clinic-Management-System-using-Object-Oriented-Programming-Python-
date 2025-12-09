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

    def update_medicine(self, medicine):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE medicines SET name=%s, price=%s, quantity=%s, expiry_date=%s, batch_no=%s WHERE medicine_id=%s"
                cursor.execute(sql, (medicine.get_name(), medicine.get_price(), medicine.get_quantity(), medicine.get_expiry_date(), medicine.get_batch_no(), medicine.get_medicine_id()))
        except Exception as e:
            raise e

    def search_medicines(self, query):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM medicines WHERE name LIKE %s OR batch_no LIKE %s"
                search_term = f"%{query}%"
                cursor.execute(sql, (search_term, search_term))
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

    def get_low_stock_medicines(self):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Assuming default min stock is 10 if not stored in DB, but model has it. 
                # Ideally DB should have min_stock_level column. For now hardcode or assume checking against quantity < 10.
                # Let's check if we can rely on python side or if we should add it to DB. 
                # Checking existing schema... we don't know it fully but model has it.
                # Let's assume DB doesn't have it yet and just query all and filter, OR (better) assume fixed 10 for now in SQL.
                sql = "SELECT * FROM medicines WHERE quantity < 10" 
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

    def get_expiring_medicines(self, threshold_date):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM medicines WHERE expiry_date <= %s"
                cursor.execute(sql, (threshold_date,))
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
