class Staff:
    def __init__(self, staff_id=None, name=None, role=None, contact=None, user_id=None, specialization=None, shift_start=None, shift_end=None):
        self.__staff_id = staff_id
        self.__name = name
        self.__role = role
        self.__contact = contact
        self.__user_id = user_id
        self.__specialization = specialization
        self.__shift_start = shift_start
        self.__shift_end = shift_end

    def get_staff_id(self): return self.__staff_id
    def set_staff_id(self, staff_id): self.__staff_id = staff_id
    def get_name(self): return self.__name
    def set_name(self, name): self.__name = name
    def get_role(self): return self.__role
    def set_role(self, role): self.__role = role
    def get_contact(self): return self.__contact
    def set_contact(self, contact): self.__contact = contact
    def get_user_id(self): return self.__user_id
    def set_user_id(self, user_id): self.__user_id = user_id
    def get_specialization(self): return self.__specialization
    def set_specialization(self, specialization): self.__specialization = specialization
    def get_shift_start(self): return self.__shift_start
    def set_shift_start(self, shift_start): self.__shift_start = shift_start
    def get_shift_end(self): return self.__shift_end
    def set_shift_end(self, shift_end): self.__shift_end = shift_end
