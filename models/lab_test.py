class LabTest:
    def __init__(self, test_id=None, test_name=None, cost=0.0, normal_range=None):
        self.__test_id = test_id
        self.__test_name = test_name
        self.__cost = cost
        self.__normal_range = normal_range

    def get_test_id(self): return self.__test_id
    def set_test_id(self, test_id): self.__test_id = test_id
    def get_test_name(self): return self.__test_name
    def set_test_name(self, test_name): self.__test_name = test_name
    def get_cost(self): return self.__cost
    def set_cost(self, cost): self.__cost = cost
    def get_normal_range(self): return self.__normal_range
    def set_normal_range(self, normal_range): self.__normal_range = normal_range
