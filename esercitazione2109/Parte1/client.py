import socket
import time

serverAddress = ("0.0.0.0", 22222)
buffer = 4096
udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

nick = input("Inserisci il tuo nickname --> ")

HELLO = f"nickname:{nick}"
bytesToSend = str.encode(HELLO)
udpSocket.sendto(bytesToSend, serverAddress)

msgFromServer = udpSocket.recvfrom(buffer)

msgPrint = "Server Status --> {}".format(msgFromServer[0])
print(msgPrint)

udpSocket.close()