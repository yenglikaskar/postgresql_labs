import os
import sys
import psycopg2
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILE = os.path.join(BASE_DIR, 'phonebook.sql')

DB_CONFIG = {
    'host':     'localhost',
    'port':     5432,
    'dbname':   'last',
    'user':     'postgres',
    'password': 'AsEn2006p.',
    'options': '-c client_encoding=UTF8'

}

def run_sql_file(path: str):
    if not os.path.exists(path):
        print(f" SQL file not found: {path}")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        script = f.read()

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            cur.execute(script)
            print(f" Executed {path}")
    except Exception as e:
        print(f" Error executing {path}: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    run_sql_file(SQL_FILE)
