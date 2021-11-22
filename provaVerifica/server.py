import threading as thr
import os
import time
import socket as sck

client=('localhost',12000)
lista_client = {}
threads = []

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def operation_selecter(conn, client_num):
    cur = conn.cursor()
    cur.execute(f"SELECT operation FROM operations Where client = {client_num}")

    rows = cur.fetchall()

    for row in rows:
        return(row[0])

class Client_Class(thr.Thread):
    def __init__(self, connection, addr, num_client):
        thr.Thread.__init__(self)
        self.addr = addr
        self.connection = connection
        self.running = True
        self.num_client = num_client

    def stop_run(self):
        self.running = False

    def ret_run(self):
        return self.running
    
    def run(self):
        while self.running:
            db = create_connection("./operations.db")
            operation_list = operation_selecter(db, num_client)
            for element in operation_list:
                

            

