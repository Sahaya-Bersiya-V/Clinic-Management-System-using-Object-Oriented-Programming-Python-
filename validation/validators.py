import re

class Validators:
    @staticmethod
    def validate_username(username):
        if not username or not username.strip():
            return "Username cannot be empty."
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return "Username must be 3-20 characters, alphanumeric or underscore."
        return None

    @staticmethod
    def validate_password(password):
        if not password or not password.strip():
            return "Password cannot be empty."
        if len(password) < 6:
            return "Password must be at least 6 characters long."
        return None

    @staticmethod
    def validate_name(name):
        if not name or not name.strip():
            return "Name cannot be empty."
        if not re.match(r'^[a-zA-Z\s]{2,50}$', name):
            return "Name must be 2-50 characters, letters only."
        return None

    @staticmethod
    def validate_phone(phone):
        if not phone or not phone.strip():
            return "Phone number cannot be empty."
        if not re.match(r'^\d{10}$', phone):
            return "Phone number must be exactly 10 digits."
        return None

    @staticmethod
    def validate_id(id_val):
        if not str(id_val).isdigit():
            return "ID must be a number."
        return None

    @staticmethod
    def validate_non_empty(value, field_name):
        if not value or not str(value).strip():
            return f"{field_name} cannot be empty."
        return None
