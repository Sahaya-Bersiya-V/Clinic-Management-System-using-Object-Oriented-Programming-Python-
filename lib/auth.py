from dao.impl.user_dao_impl import UserDAOImpl
from validation.validators import Validators

class AuthService:
    def __init__(self):
        self.user_dao = UserDAOImpl()

    def login(self, username, password):
        # Validate input
        val_user = Validators.validate_username(username)
        if val_user:
            raise ValueError(val_user)
        
        val_pass = Validators.validate_password(password)
        if val_pass:
            raise ValueError(val_pass)

        # DAO call
        user = self.user_dao.get_user_by_username(username)
        
        if not user:
            raise ValueError("Invalid username or password.")
        
        if user.get_password() != password:
            raise ValueError("Invalid username or password.")
            
        if not user.get_is_active():
            raise ValueError("Account is deactivated. Contact Admin.")
            
        return user
