import threading as thr
import time
import socket as sck
import sqlite3

CLIENT=('localhost',12000)
threads = []
global nomeFrammento #lista di contenimento dei dati importanti del database
nomeFrammento = []


def create_connection(db_file): #funzione per la connessione al server
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def allName(conn):  #funzione di selezionamento dei dati, attraverso la query mi restituisce un lista con i dati interessati
    list = []
    cur = conn.cursor()
    cur.execute(f"SELECT nome,tot_frammenti,host,n_frammento FROM files,frammenti WHERE files.id_file = frammenti.id_file") #questo fa la join del db
    rows = cur.fetchall()
    for row in rows:
        list.append((row))

    return list

def listCharger(): #funzione iniziale che apre il db e carica la lista poi chiude il db
    global nomeFrammento
    db = create_connection("./file.db")
    nomeFrammento = allName(db)
    db.close()

class Client_Class(thr.Thread):
    def __init__(self, connection, addr):
        thr.Thread.__init__(self)
        self.addr = addr
        self.connection = connection
        self.running = True

    def stop_run(self):
        self.running = False

    def ret_run(self):
        return self.running
    
    def run(self):
        global nomeFrammento
        while self.running:
            query = self.connection.recv(4096).decode()
            print(query.split(";")[-1])
            if query.split(";")[-1] == "CE":        #prima funzione, controlla se il nome è presente nella lista
                for element in nomeFrammento:
                    if query.split(";")[0] == element[0]:
                        self.connection.sendall(f"Il nome e presente".encode())
                        print("nome trovato")
                        break
                    #else:
                        #self.connection.sendall(f"Il nome non e presente".encode())
                        #print("nome non trovato")

            if query.split(";")[-1] == "NF":        #seconda funzione, controllail nome e restituisce il numero di frammenti
                for element in nomeFrammento:
                    if query.split(";")[0] == element[0]:
                        self.connection.sendall(f"n Frammenti --> {element[1]}".encode())
                        print("mandati frammenti richiesti")
                        break
                    #else:
                        #self.connection.sendall(f"File non trovato".encode())
                        #print("file non trovato (NF)")

            if query.split(";")[-1] == "HOF":   #controlla il nome e dopo il numero del frammento passato dal client per poi restituire l'indirizzo ip dell'host dove il frammento è stato trovato
                for element in nomeFrammento:
                    if query.split(";")[0] == element[0]:
                        if query.split(";")[1] == element[3]:
                            self.connection.sendall(f"Frammento trovato --> ip: {element[2]}".encode())
                            print("ip trovato")
                            break
                        else:
                            self.connection.sendall(f"file non trovato".encode())
                            print("ip non trovato")
            
            if query.split(";")[-1] == "FSH":       #restituisce una lista con tutti gli ip dove risiede un frammento del film passato
                listaIP = []
                for element in nomeFrammento:
                    if query.split(";")[0] == element[0]:
                        listaIP.append(element[2])
                self.connection.sendall(f"lista host --> {listaIP}".encode())

class Thread_remover(thr.Thread):   #thread per chiudere ed eliminare dalla lista i thread finiti
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

    while True:
        connection, addr = s.accept()
    
        client = Client_Class(connection, addr)

        threads.append(client)
        client.start()
        time.sleep(0.2)
        

    for k in threads:
        k.stop_run()

    s.close()

if __name__ == "__main__":
    listCharger()
    main()