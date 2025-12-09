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
    
    import os
    # Get current dir of this script (tests/) then go up to root and down to sql_scripts
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sql_path = os.path.join(base_dir, 'sql_scripts', 'hms_schema_update.sql')
    
    with open(sql_path, 'r') as f:
        sql_script = f.read()
        
    statements = sql_script.split(';')
    
    with conn.cursor() as cursor:
        for statement in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                    print(f"Executed: {statement[:50]}...")
                except pymysql.err.OperationalError as e:
                    if e.args[0] == 1060:
                        print(f"Skipped (Column already exists): {statement[:50]}...")
                    else:
                        print(f"Skipped/Error: {e}")
                except Exception as e:
                    print(f"Skipped/Error: {e}")
                    
    conn.close()
    print("Schema update completed.")

if __name__ == "__main__":
    run_update()
