from dao.impl.appointment_dao_impl import AppointmentDAOImpl

def dump_appts():
    dao = AppointmentDAOImpl()
    appts = dao.get_all_appointments()
    print(f"Total Appts: {len(appts)}")
    for a in appts:
        print(f"ID: {a.get_appointment_id()}, Date: {a.get_date()}, Diag: {a.get_diagnosis()}, Rx: {a.get_prescription()}")

if __name__ == "__main__":
    dump_appts()
