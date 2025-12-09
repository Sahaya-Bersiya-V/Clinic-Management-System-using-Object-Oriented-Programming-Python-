from dao.impl.staff_dao_impl import StaffDAOImpl
from dao.impl.user_dao_impl import UserDAOImpl
from models.staff import Staff
from models.user import User
from validation.validators import Validators

class AdminService:
    def __init__(self):
        self.staff_dao = StaffDAOImpl()
        self.user_dao = UserDAOImpl()

    def add_staff(self, name, role, contact, username, password, specialization, shift_start, shift_end):
        # Validate
        err = Validators.validate_name(name)
        if err: raise ValueError(err)
        err = Validators.validate_phone(contact)
        if err: raise ValueError(err)
        err = Validators.validate_username(username)
        if err: raise ValueError(err)
        err = Validators.validate_password(password)
        if err: raise ValueError(err)
        
        # Create User first
        user = User(username=username, password=password, role=role)
        created_user = self.user_dao.create_user(user)
        
        # Create Staff
        staff = Staff(
            name=name, 
            role=role, 
            contact=contact, 
            user_id=created_user.get_user_id(),
            specialization=specialization,
            shift_start=shift_start,
            shift_end=shift_end
        )
        return self.staff_dao.create_staff(staff)

    def get_all_staff(self):
        return self.staff_dao.get_all_staff()

    def delete_staff(self, staff_id):
        return self.staff_dao.delete_staff(staff_id)

    def deactivate_staff(self, staff_id):
        return self.staff_dao.deactivate_staff(staff_id)

    def update_staff(self, staff):
        return self.staff_dao.update_staff(staff)

    def get_staff_by_role(self, role):
        return self.staff_dao.get_staff_by_role(role)

    def get_staff_by_id(self, staff_id):
        return self.staff_dao.get_staff_by_id(staff_id)

