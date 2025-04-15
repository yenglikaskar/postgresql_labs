import psycopg2
import csv

def upload_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    print("done CSV dates!")

# connecting to db
conn = psycopg2.connect(
    dbname="labdb",
    user="postgres",
    password="AsEn2006p.", 
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# input console
def insert_from_console():
    name = input("Enter username: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("done")

# searching
def search():
    keyword = input("Enter search word: ")
    cur.execute("SELECT * FROM phonebook WHERE username ILIKE %s OR phone ILIKE %s", (f'%{keyword}%', f'%{keyword}%'))
    for row in cur.fetchall():
        print(row)
# menu
print("1 - add\n2 - search\n3 - upload csv")
choice = input("choose: ")
if choice == "1":
    insert_from_console()
elif choice == "2":
    search()
elif choice == "3":
    upload_from_csv("info.csv")
cur.close()
conn.close()
