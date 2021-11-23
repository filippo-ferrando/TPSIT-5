import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def operation_selecter(conn, client_num):
    list = []
    cur = conn.cursor()
    cur.execute(f"SELECT operation FROM operations Where client = {client_num}")

    rows = cur.fetchall()

    for row in rows:
        list.append((row[-1]))

    return list

def contatore(conn):
    cur = conn.cursor()
    cur.execute(f"SELECT max(client) FROM operations")

    rows = cur.fetchall()

    for row in rows:
       print(row[-1])

def main():
    db = create_connection("./operations.db")
    op_list = operation_selecter(db, 1)
    contatore(db)
    db.close()

    #print(op_list)

    

    for element in op_list:
        print(eval(element))

if __name__ == "__main__":
    main()