from flask import Flask, render_template, redirect, url_for, request
import sqlite3
from sqlite3 import Error
import socket

app = Flask(__name__)

def create_connection(db_file): #funzione per connettere il database allo script
    conn = None
    try:
        conn = sqlite3.connect(db_file) #ettiva connessione al db
    except Error as e: #gestione dell'errore
        print(e)

    return conn

def insert_record_ip(ip):
    conn = create_connection("db.db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO INDIRIZZI (IP) VALUES ('{ip}')")
    cur.execute("commit")
    conn.close()

def insert_record_port(idP, port, active):
    conn = create_connection("db.db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO PORTE (ID_IP, PORT, STATUS) VALUES ('{idP}', '{port}', '{active}')")
    cur.execute("commit")
    conn.close()

def find_ip_id(ip):
    conn = create_connection("db.db")
    cur = conn.cursor()
    cur.execute(f"SELECT ID FROM INDIRIZZI WHERE IP = '{ip}'")
    rows = cur.fetchall()
    #print(rows)
    conn.close()
    return(rows[-1][0])
    

def port_scan(ip, portS, portF):
    insert_record_ip(ip)
    for port in range(portS, portF):  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            insert_record_port(find_ip_id(ip),port, result)
            print(f"scanned: {port}, {result}")
            sock.close()

@app.route(f'/', methods=['GET', 'POST'])
def index():
    msg = ""
    if request.method == 'POST':
        msg = ""
        address = request.form['indirizzo']
        ip, port0, port1 = address.split(",")
        port_scan(ip, int(port0), int(port1))
        msg = "Finished Scan"

    return render_template('index.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')