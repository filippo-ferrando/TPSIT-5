import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def allName(conn):
    list = []
    cur = conn.cursor()
    cur.execute(f"SELECT nome,tot_frammenti,host,n_frammento FROM files,frammenti WHERE files.id_file = frammenti.id_file")
    rows = cur.fetchall()
    for row in rows:
        list.append((row))

    return list

def main():
    db = create_connection("./file.db")
    print(allName(db)[0][3])

main()