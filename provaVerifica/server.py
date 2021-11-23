import threading as thr
import os
import time
import socket as sck
import sqlite3

CLIENT=('localhost',12001)
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
    list = []
    cur = conn.cursor()
    cur.execute(f"SELECT operation FROM operations Where client = {client_num}")

    rows = cur.fetchall()

    for row in rows:
        list.append((row[-1]))

    return list

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
            operation_list = operation_selecter(db, self.num_client)
            db.close()
            for element in operation_list:
                self.connection.sendall(element.encode())
                answ = self.connection.recv(4096).decode()
                print(f"client: {self.num_client} answered: {element} --> answer: {answ}")
            self.connection.sendall("exit".encode())
            self.stop_run()
            


class Thread_remover(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self)
        self.running = True

    def run(self):
        while self.running:
            for i in threads:
                if not i.ret_run():
                    i.join()
                    threads.remove(i)
            

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(CLIENT)
    s.listen()

    thread_stopper = Thread_remover()
    thread_stopper.start()

    client_counter = 0

    while True:
        connection, addr = s.accept()
        client_counter += 1
    
        client = Client_Class(connection, addr, client_counter)

        threads.append(client)
        client.start()
        time.sleep(0.2)

        #print(client_counter)
        if client_counter >= 2:
            break
        

    for k in threads:
        k.stop_run()

    s.close()

if __name__ == "__main__":
    main()