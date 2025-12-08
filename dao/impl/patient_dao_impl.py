from dao.base.patient_dao import PatientDAO
from DbConnection.db_singleton import DbConnection
from models.patient import Patient

class PatientDAOImpl(PatientDAO):
    def __init__(self):
        self.db_connection = DbConnection()

    def create_patient(self, patient):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO patients (name, age, gender, contact) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (patient.get_name(), patient.get_age(), patient.get_gender(), patient.get_contact()))
                patient.set_patient_id(cursor.lastrowid)
                return patient
        except Exception as e:
            raise e

    def get_patient_by_id(self, patient_id):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM patients WHERE patient_id = %s"
                cursor.execute(sql, (patient_id,))
                result = cursor.fetchone()
                if result:
                    return Patient(
                        patient_id=result['patient_id'],
                        name=result['name'],
                        age=result['age'],
                        gender=result['gender'],
                        contact=result['contact']
                    )
                return None
        except Exception as e:
            raise e

    def get_all_patients(self):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM patients"
                cursor.execute(sql)
                results = cursor.fetchall()
                patients = []
                for row in results:
                    patients.append(Patient(
                        patient_id=row['patient_id'],
                        name=row['name'],
                        age=row['age'],
                        gender=row['gender'],
                        contact=row['contact']
                    ))
                return patients
        except Exception as e:
            raise e

    def update_patient(self, patient):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE patients SET name=%s, age=%s, gender=%s, contact=%s WHERE patient_id=%s"
                cursor.execute(sql, (patient.get_name(), patient.get_age(), patient.get_gender(), patient.get_contact(), patient.get_patient_id()))
        except Exception as e:
            raise e
