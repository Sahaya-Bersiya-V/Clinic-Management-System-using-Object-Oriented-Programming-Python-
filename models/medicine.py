class Medicine:
    def __init__(self, medicine_id=None, name=None, price=None, quantity=None, expiry_date=None, batch_no=None, min_stock_level=10):
        self.__medicine_id = medicine_id
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__expiry_date = expiry_date
        self.__batch_no = batch_no
        self.__min_stock_level = min_stock_level

    def get_medicine_id(self): return self.__medicine_id
    def set_medicine_id(self, medicine_id): self.__medicine_id = medicine_id
    def get_name(self): return self.__name
    def set_name(self, name): self.__name = name
    def get_price(self): return self.__price
    def set_price(self, price): self.__price = price
    def get_quantity(self): return self.__quantity
    def set_quantity(self, quantity): self.__quantity = quantity
    def get_expiry_date(self): return self.__expiry_date
    def set_expiry_date(self, expiry_date): self.__expiry_date = expiry_date
    def get_batch_no(self): return self.__batch_no
    def set_batch_no(self, batch_no): self.__batch_no = batch_no
    def get_min_stock_level(self): return self.__min_stock_level
    def set_min_stock_level(self, min_stock_level): self.__min_stock_level = min_stock_level
