import psycopg2
import os

DB_CONFIG = {
    'host':     'localhost',
    'port':     5432,
    'dbname':   'last',
    'user':     'postgres',
    'password': 'AsEn2006p.',
    'options': '-c client_encoding=UTF8'

}

def search(pattern):
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM fn_search_phonebook(%s);", (pattern,))
        rows = cur.fetchall()

    if not rows:
        print(" Нет совпадений.")
    else:
        print(f" Найдено {len(rows)}:")
        for id_, name, phone in rows:
            print(f"   {id_:>3} │ {name:<20} │ {phone}")

def upsert(name, phone):
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("CALL sp_upsert_user(%s, %s);", (name, phone))
        print(f"→ Записан: {name} → {phone}")

def delete(name, phone):
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("CALL sp_delete_phonebook(%s, %s);", (name or None, phone or None))
        print(f"→ Удалено записи, где name={name!r} и phone={phone!r}")

def main():
    print("Команды:")
    print("  s — поиск")
    print("  u — добавить/обновить")
    print("  d — удалить")
    print("  q — выход\n")

    while True:
        cmd = input("Введите команду (s/u/d/q): ").strip().lower()
        if cmd == 'q':
            print("Выход.")
            break
        elif cmd == 's':
            pat = input("Шаблон для поиска: ").strip()
            search(pat)
        elif cmd == 'u':
            name = input("Имя: ").strip()
            phone = input("Телефон: ").strip()
            upsert(name, phone)
        elif cmd == 'd':
            name = input("Имя (оставьте пустым, чтобы не фильтровать по имени): ").strip()
            phone = input("Телефон (оставьте пустым, чтобы не фильтровать по телефону): ").strip()
            if not name and not phone:
                print(" Нужно хотя бы имя или телефон для удаления.")
                continue
            delete(name, phone)
        else:
            print("Неверная команда. Введите одну из: s, u, d, q.")

if __name__ == "__main__":
    main()
