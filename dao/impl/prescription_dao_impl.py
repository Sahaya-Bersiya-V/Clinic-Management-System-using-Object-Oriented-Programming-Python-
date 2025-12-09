from dao.base.prescription_dao import PrescriptionDAO
from DbConnection.db_singleton import DbConnection
from models.prescription import Prescription

class PrescriptionDAOImpl(PrescriptionDAO):
    def __init__(self):
        self.db_connection = DbConnection()

    def create_prescription(self, prescription):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO prescriptions (appointment_id, medicine_id, dosage, duration, quantity) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (prescription.get_appointment_id(), prescription.get_medicine_id(), prescription.get_dosage(), prescription.get_duration(), prescription.get_quantity()))
                prescription.set_prescription_id(cursor.lastrowid)
                return prescription
        except Exception as e:
            raise e

    def get_prescriptions_by_appointment(self, appointment_id):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT p.prescription_id, p.appointment_id, p.medicine_id, m.name as medicine_name, p.dosage, p.duration, p.quantity
                    FROM prescriptions p
                    JOIN medicines m ON p.medicine_id = m.medicine_id
                    WHERE p.appointment_id = %s
                """
                cursor.execute(sql, (appointment_id,))
                results = cursor.fetchall()
                # Return list of dicts for easier display or Prescription objects? 
                # Objects are better but loose info like medicine_name unless I extend model or assume logic elsewhere.
                # I will return dicts including medicine name for UI convenience.
                prescriptions = []
                for row in results:
                    prescriptions.append({
                        "prescription_id": row['prescription_id'],
                        "medicine_name": row['medicine_name'],
                        "dosage": row['dosage'],
                        "duration": row['duration'],
                        "quantity": row['quantity']
                    })
                return prescriptions
        except Exception as e:
            raise e
