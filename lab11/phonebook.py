import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'last',
    'user': 'postgres',
    'password': 'AsEn2006p.'
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def search(pattern):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, phone FROM fn_search_phonebook(%s);",
            (pattern,)
        )
        return cur.fetchall()

def upsert(name, phone):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("CALL sp_upsert_user(%s, %s);", (name, phone))
        conn.commit()

def delete(name=None, phone=None):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("CALL sp_delete_phonebook(%s, %s);", (name, phone))
        conn.commit()
