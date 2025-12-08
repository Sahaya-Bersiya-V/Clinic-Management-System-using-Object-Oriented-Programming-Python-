import pymysql
import configparser
import os

class DbConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DbConnection, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db_config.ini')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
            
        config.read(config_path)
        
        try:
            db_config = config['database']
            self._connection = pymysql.connect(
                host=db_config.get('host'),
                user=db_config.get('user'),
                password=db_config.get('password'),
                database=db_config.get('database'),
                port=int(db_config.get('port', 3306)),
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {str(e)}")

    def get_connection(self):
        if self._connection is None or not self._connection.open:
            self._connect()
        return self._connection

    def close_connection(self):
        if self._connection and self._connection.open:
            self._connection.close()
