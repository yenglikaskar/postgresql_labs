
import os
import sys
import csv
import psycopg2

DB_CONFIG = {
    'host':     'localhost',
    'port':     5432,
    'dbname':   'last',
    'user':     'postgres',
    'password': 'AsEn2006p.',
    'options': '-c client_encoding=UTF8'

}

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'info.csv')

def load_csv(path):
    if not os.path.exists(path):
        print(f" CSV not found: {path}")
        sys.exit(1)

    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn, conn.cursor() as cur:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or len(row) < 2:
                        continue

                    name, phone = row[0].strip(), row[1].strip()
                    if not name or not phone:
                        continue

                    cur.execute("CALL sp_upsert_user(%s, %s);", (name, phone))

        print(f" Loaded data from {os.path.basename(path)}")

    except Exception as e:
        print(f" Error loading CSV: {e}")
        sys.exit(1)

    finally:
        conn.close()


if __name__ == "__main__":
    load_csv(CSV_FILE)
