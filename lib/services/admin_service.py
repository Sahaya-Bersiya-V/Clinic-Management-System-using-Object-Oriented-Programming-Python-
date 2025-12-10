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
        """
        Purpose: Creates a new Staff member and their associated User account.
        Context: Called by AdminDashboard.add_staff.
        Calls: UserDAOImpl.create_user, StaffDAOImpl.create_staff, Validators.*
        """
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
        """
        Purpose: Retrieves all staff members.
        Context: Called by AdminDashboard.view_staff.
        Calls: StaffDAOImpl.get_all_staff
        """
        return self.staff_dao.get_all_staff()

    def delete_staff(self, staff_id):
        """
        Purpose: Permanently removes a staff member (and conceptually their user).
        Context: Called by AdminDashboard (if implemented/needed).
        Calls: StaffDAOImpl.delete_staff
        """
        return self.staff_dao.delete_staff(staff_id)

    def deactivate_staff(self, staff_id):
        """
        Purpose: Deactivates a staff member's user account, preventing login.
        Context: Called by AdminDashboard.remove_staff (Soft Delete logic).
        Calls: StaffDAOImpl.deactivate_staff
        """
        return self.staff_dao.deactivate_staff(staff_id)

    def update_staff(self, staff):
        """
        Purpose: Updates details of an existing staff member.
        Context: Called by AdminDashboard.update_doctor.
        Calls: StaffDAOImpl.update_staff
        """
        return self.staff_dao.update_staff(staff)

    def get_staff_by_role(self, role):
        """
        Purpose: Retrieves staff members filtered by role (e.g., 'Doctor').
        Context: Called by AdminDashboard.view_doctor_list.
        Calls: StaffDAOImpl.get_staff_by_role
        """
        return self.staff_dao.get_staff_by_role(role)

    def get_staff_by_id(self, staff_id):
        """
        Purpose: Retrieves a specific staff member's details.
        Context: Called by AdminDashboard to fetch details before update.
        Calls: StaffDAOImpl.get_staff_by_id
        """
        return self.staff_dao.get_staff_by_id(staff_id)

    def get_current_staff_profile(self, user_id):
        return self.staff_dao.get_staff_by_user_id(user_id)

