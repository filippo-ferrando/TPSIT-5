import threading as thr
import socket as sck


indirizzo = ("127.0.0.1",5007)
s = sck.socket(sck.AF_INET,sck.SOCK_DGRAM)
s.bind(indirizzo)

messaggi = []
utenti = {}
collegamenti = {}

class gestoreClient(thr.Thread):
    def __init__(self,s):
        thr.Thread.__init__(self, daemon=True)
        self.nMessaggioAnalizzato = 0
        self.s = s


    def run(self):
        global messaggi,collegamenti
        while True:
            if len(messaggi) > self.nMessaggioAnalizzato:
                ''' LEGGI MESSAGGI
                messaggio = messaggi[self.nMessaggioAnalizzato][0][len(messaggi[self.nMessaggioAnalizzato][1])+1:]
                collegamenti[messaggi[self.nMessaggioAnalizzato][1]] = messaggio
                print(messaggio)
                self.nMessaggioAnalizzato +=1

                '''

def main():
    global messaggi,utenti,s
    gestore = gestoreClient(s) 
    gestore.start()

    while True:
        messaggio,indirizzo = s.recvfrom(4098)
        messaggio = messaggio.decode()
        print(messaggio)
        if("NICKNAME: " in messaggio):
            nome = (messaggio.split("NICKNAME: "))[1]
            utenti[nome] = indirizzo
            print(f'aggiunto {utenti[nome][0]}, {indirizzo}')

        else:
            messaggioScomposto = messaggio.split(":")
            if messaggioScomposto[1] in utenti:
                s.sendto((f"\nda {messaggioScomposto[0]}: {messaggioScomposto[2]}").encode(),utenti[messaggioScomposto[1]])
                print(f"da {messaggioScomposto[0]} a {messaggioScomposto[1]}: {messaggioScomposto[2]}")
            messaggi.append((nome,indirizzo))


if __name__ == '__main__':
    main()