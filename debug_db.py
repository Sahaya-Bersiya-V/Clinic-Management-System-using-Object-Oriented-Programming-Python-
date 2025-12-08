import pymysql
import configparser
import sys

def test_connection(host, user, password, port, database):
    print(f"Testing connection to {host}:{port} as {user}...")
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("SUCCESS: Connected!")
        conn.close()
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False

def main():
    config = configparser.ConfigParser()
    config.read('db_config.ini')
    
    try:
        db_config = config['database']
        user = db_config.get('user')
        password = db_config.get('password')
        database = db_config.get('database')
        port = int(db_config.get('port', 3306))
        
        # Test 1: Configured host (localhost)
        print("\n--- Test 1: Configured Host ---")
        test_connection(db_config.get('host'), user, password, port, database)
        
    except Exception as e:
        print(f"Error reading config: {e}")

if __name__ == "__main__":
    main()
