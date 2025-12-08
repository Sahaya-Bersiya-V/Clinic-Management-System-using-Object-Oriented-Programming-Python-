import pymysql
import configparser

def run_update():
    config = configparser.ConfigParser()
    config.read('db_config.ini')
    db_config = config['database']
    
    conn = pymysql.connect(
        host=db_config.get('host'),
        user=db_config.get('user'),
        password=db_config.get('password'),
        database=db_config.get('database'),
        port=int(db_config.get('port', 3306)),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    
    with open('hms_schema_update.sql', 'r') as f:
        sql_script = f.read()
        
    statements = sql_script.split(';')
    
    with conn.cursor() as cursor:
        for statement in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                    print(f"Executed: {statement[:50]}...")
                except Exception as e:
                    print(f"Skipped/Error: {e}")
                    
    conn.close()
    print("Schema update completed.")

if __name__ == "__main__":
    run_update()
