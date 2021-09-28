import threading as thr
import socket as sck

#inviare  = f"{nick_mittente} : {nick_dest} : {messaggio}"

indirizzo = ('192.168.0.126',5000)
global s
s = sck.socket(sck.AF_INET,sck.SOCK_DGRAM)

class ClientUDP(thr.Thread):
    def __init__(self, s):
        thr.Thread.__init__(self,daemon=True)
        self.s = s

    def run(self):
        while True:
            messaggio,indirizzo = self.s.recvfrom(4096)
            print(messaggio.decode())


def main():
    global s
    client = ClientUDP(s)
    client.start()

    nome = input("inserire nome...")
    s.sendto(f"NICKNAME\n{nome}".encode(),indirizzo)
    while True:
        messaggio = str(input("inserire messaggio: "))
        destinatario = str(input("inserire destinatario: "))

        s.sendto(f"{nome}\n{destinatario}\n{messaggio}".encode(),indirizzo)



if __name__ == '__main__':
    main()  