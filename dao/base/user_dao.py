from abc import ABC, abstractmethod
from models.user import User

class UserDAO(ABC):
    @abstractmethod
    def get_user_by_username(self, username):
        pass

    @abstractmethod
    def create_user(self, user):
        pass

    @abstractmethod
    def update_user_status(self, user_id, is_active):
        pass

