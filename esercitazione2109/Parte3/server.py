import socket as sck
import threading as thr
import time

CLIENT=('localhost', 5000)
lista_client = {}
threads = []

class Clients_class(thr.Thread):
    def __init__(self, connessione, addr):
        thr.Thread.__init__(self)   #costruttore super (java)
        self.addr = addr
        self.connessione = connessione
        self.running = True

    def stop_run(self):
        self.running = False

    def ret_run(self):
        return self.running

    def run(self):
        while self.running:
            messaggio = (self.connessione.recv(4096)).decode()
            messaggio = messaggio.split(":")

            if 'exit' in messaggio:
                self.running = False
                self.connessione.close()
                lista_client.pop(messaggio[0])
                print(f"{messaggio[0]} si è disconnesso.")
            
            elif '!LIST' in messaggio:
                print(f"{messaggio[0]} ha usato il comando '!LIST'.")
                clients = ""
                for k in lista_client.keys():
                    clients += k + "\n"

                lista_client[messaggio[1]].sendall(clients.encode())
                
            else:
                if messaggio[0].lower() == "nickname":
                    print(f"Nuova iscrizione: {messaggio[1]}")
                    lista_client[messaggio[1]] = self.connessione
                    self.connessione.sendall("OK".encode())

                else:
                    trovato = False
                    for k in lista_client.keys():
                        if messaggio[1] == k:
                            trovato = True
                            lista_client[messaggio[1]].sendall((messaggio[0] + ":" + messaggio[2]).encode())
                            print(f"{messaggio[0]} manda a {messaggio[1]}: {messaggio[2]}")

                    if trovato == False:
                        lista_client[messaggio[0]].sendall("Il destinatario da lei cercato non esiste.".encode())
                            



class Thread_remover(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self)
        self.running = True

    def run(self):
        global lista_client

        while self.running:
            for i in threads:
                if not i.ret_run():
                    i.join()
                    threads.remove(i)



def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(CLIENT)
    s.listen()

    stop_thread = Thread_remover()
    stop_thread.start()


    while True:
        connection, address = s.accept()
        client = Clients_class(connection, address)

        threads.append(client)
        client.start()
        time.sleep(0.1)

    
    #chiusura di tutti i client con running = False
    for k in threads:
        k.stop_run()

    s.close()

if __name__ == "__main__":
    main()