class Patient:
    def __init__(self, patient_id=None, name=None, age=None, gender=None, contact=None, blood_group=None, address=None):
        self.__patient_id = patient_id
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__contact = contact
        self.__blood_group = blood_group
        self.__address = address

    def get_patient_id(self): return self.__patient_id
    def set_patient_id(self, patient_id): self.__patient_id = patient_id
    def get_name(self): return self.__name
    def set_name(self, name): self.__name = name
    def get_age(self): return self.__age
    def set_age(self, age): self.__age = age
    def get_gender(self): return self.__gender
    def set_gender(self, gender): self.__gender = gender
    def get_contact(self): return self.__contact
    def set_contact(self, contact): self.__contact = contact
    def get_blood_group(self): return self.__blood_group
    def set_blood_group(self, blood_group): self.__blood_group = blood_group
    def get_address(self): return self.__address
    def set_address(self, address): self.__address = address
