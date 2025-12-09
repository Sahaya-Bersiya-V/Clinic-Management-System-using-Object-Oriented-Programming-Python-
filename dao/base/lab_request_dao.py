from abc import ABC, abstractmethod

class LabRequestDAO(ABC):
    @abstractmethod
    def create_request(self, request):
        pass

    @abstractmethod
    def get_request_by_id(self, request_id):
        pass

    @abstractmethod
    def update_request(self, request):
        pass
