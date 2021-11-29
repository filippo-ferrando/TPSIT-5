import socket
import threading as thr
import time

server=("localhost", 12000)

class Receiver(thr.Thread):
    def __init__(self, s):
        thr.Thread.__init__(self)
        self.running = True
        self.s = s

    def stop_run(self):
        self.running = False

    def run(self):
        while self.running:#il funzionamento del client è banale, manda un input al server che a sua volta risponde e printa la risposta
            str = input("Inserisci i dati come (dato1);(dato2): ")
            self.s.sendall(str.encode())
            answ = self.s.recv(4096)
            print(answ)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server)

    print("CE --> Cerca esistenza nome \n NF --> Numero frammenti id un file \n HOF --> (nome e n.frammento) cerca l'indirizzo ip dove rimane il frammento \n FSH --> lista di ip dove è presente un frammento del file scelto \n")

    ricev = Receiver(s)
    ricev.start()


    while True:
        time.sleep(0.2)
        if ricev.running == False:
            ricev.join()
            s.close()
            break

if __name__ == "__main__":
    main()