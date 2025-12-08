from dao.base.staff_dao import StaffDAO
from DbConnection.db_singleton import DbConnection
from models.staff import Staff

class StaffDAOImpl(StaffDAO):
    def __init__(self):
        self.db_connection = DbConnection()

    def create_staff(self, staff):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO staff (name, role, contact, user_id, specialization, shift_start, shift_end) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (staff.get_name(), staff.get_role(), staff.get_contact(), staff.get_user_id(), staff.get_specialization(), staff.get_shift_start(), staff.get_shift_end()))
                staff.set_staff_id(cursor.lastrowid)
                return staff
        except Exception as e:
            raise e

    def get_all_staff(self):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM staff"
                cursor.execute(sql)
                results = cursor.fetchall()
                staff_list = []
                for row in results:
                    staff_list.append(Staff(
                        staff_id=row['staff_id'],
                        name=row['name'],
                        role=row['role'],
                        contact=row['contact'],
                        user_id=row['user_id'],
                        specialization=row.get('specialization'),
                        shift_start=row.get('shift_start'),
                        shift_end=row.get('shift_end')
                    ))
                return staff_list
        except Exception as e:
            raise e

    def get_staff_by_id(self, staff_id):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM staff WHERE staff_id = %s"
                cursor.execute(sql, (staff_id,))
                result = cursor.fetchone()
                if result:
                    return Staff(
                        staff_id=result['staff_id'],
                        name=result['name'],
                        role=result['role'],
                        contact=result['contact'],
                        user_id=result['user_id'],
                        specialization=result.get('specialization'),
                        shift_start=result.get('shift_start'),
                        shift_end=result.get('shift_end')
                    )
                return None
        except Exception as e:
            raise e

    def update_staff(self, staff):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE staff SET name=%s, role=%s, contact=%s, specialization=%s, shift_start=%s, shift_end=%s WHERE staff_id=%s"
                cursor.execute(sql, (staff.get_name(), staff.get_role(), staff.get_contact(), staff.get_specialization(), staff.get_shift_start(), staff.get_shift_end(), staff.get_staff_id()))
        except Exception as e:
            raise e

    def delete_staff(self, staff_id):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM staff WHERE staff_id = %s"
                cursor.execute(sql, (staff_id,))
        except Exception as e:
            raise e
