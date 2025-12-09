import pymysql
import configparser

def check_schema():
    config = configparser.ConfigParser()
    config.read('db_config.ini')
    db_config = config['database']
    
    conn = pymysql.connect(
        host=db_config.get('host'),
        user=db_config.get('user'),
        password=db_config.get('password'),
        database=db_config.get('database'),
        port=int(db_config.get('port', 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )
    
    with conn.cursor() as cursor:
        print("--- Checking Users Table ---")
        cursor.execute("DESCRIBE users")
        for row in cursor.fetchall():
            print(f"Column: {row['Field']}, Type: {row['Type']}")
            
    conn.close()

if __name__ == "__main__":
    check_schema()
