from dao.base.appointment_dao import AppointmentDAO
from DbConnection.db_singleton import DbConnection
from models.appointment import Appointment

class AppointmentDAOImpl(AppointmentDAO):
    def __init__(self):
        self.db_connection = DbConnection()

    def create_appointment(self, appointment):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO appointments (patient_id, doctor_id, date, status) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (appointment.get_patient_id(), appointment.get_doctor_id(), appointment.get_date(), appointment.get_status()))
                appointment.set_appointment_id(cursor.lastrowid)
                return appointment
        except Exception as e:
            raise e

    def get_appointments_by_doctor(self, doctor_id):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM appointments WHERE doctor_id = %s"
                cursor.execute(sql, (doctor_id,))
                results = cursor.fetchall()
                appointments = []
                for row in results:
                    appointments.append(Appointment(
                        appointment_id=row['appointment_id'],
                        patient_id=row['patient_id'],
                        doctor_id=row['doctor_id'],
                        date=row['date'],
                        status=row['status'],
                        diagnosis=row['diagnosis'],
                        prescription=row['prescription']
                    ))
                return appointments
        except Exception as e:
            raise e

    def get_appointment_by_id(self, appointment_id):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM appointments WHERE appointment_id = %s"
                cursor.execute(sql, (appointment_id,))
                result = cursor.fetchone()
                if result:
                    return Appointment(
                        appointment_id=result['appointment_id'],
                        patient_id=result['patient_id'],
                        doctor_id=result['doctor_id'],
                        date=result['date'],
                        status=result['status'],
                        diagnosis=result['diagnosis'],
                        prescription=result['prescription']
                    )
                return None
        except Exception as e:
            raise e

    def get_all_appointments(self):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM appointments"
                cursor.execute(sql)
                results = cursor.fetchall()
                appointments = []
                for row in results:
                    appointments.append(Appointment(
                        appointment_id=row['appointment_id'],
                        patient_id=row['patient_id'],
                        doctor_id=row['doctor_id'],
                        date=row['date'],
                        status=row['status'],
                        diagnosis=row['diagnosis'],
                        prescription=row['prescription']
                    ))
                return appointments
        except Exception as e:
            raise e
    
    def update_appointment(self, appointment):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE appointments SET status=%s, diagnosis=%s, prescription=%s WHERE appointment_id=%s"
                cursor.execute(sql, (appointment.get_status(), appointment.get_diagnosis(), appointment.get_prescription(), appointment.get_appointment_id()))
        except Exception as e:
            raise e
