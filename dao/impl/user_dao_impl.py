from dao.base.user_dao import UserDAO
from DbConnection.db_singleton import DbConnection
from models.user import User

class UserDAOImpl(UserDAO):
    def __init__(self):
        self.db_connection = DbConnection()

    def get_user_by_username(self, username):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                if result:
                    return User(
                        user_id=result['user_id'],
                        username=result['username'],
                        password=result['password'],
                        role=result['role'],
                        is_active=result.get('is_active', 1) # Default to 1 if column missing during migration
                    )
                return None
        except Exception as e:
            raise e

    def create_user(self, user):
        connection = self.db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (username, password, role, is_active) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (user.get_username(), user.get_password(), user.get_role(), user.get_is_active()))
                user.set_user_id(cursor.lastrowid)
                return user
        except Exception as e:
            raise e
