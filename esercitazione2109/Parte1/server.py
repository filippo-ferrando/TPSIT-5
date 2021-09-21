import socket

ip = "0.0.0.0"
port = 22222
buffer = 4096

#msg = "Messsage from the UDP Server!"
#bytesToSend = str.encode(msg)

db = {}

udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

udpSocket.bind((ip, port))

OK = "OK"
k = 0 # ! contatore guest


print("UDP SERVER STARTED")

while True:
    bytesAddressPair = udpSocket.recvfrom(buffer)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    if(message.decode().split(":")[-1] == ""):
        nickname = f"guest{k}"
        k += 1
    else:
        nickname = message.decode().split(":")[-1]

    db[nickname] = address

    clientMsg = "Message from Client --> {}".format(message)

    print(clientMsg)
    print(db)


    msg = format(OK)
    #msg = str(msg)

    bytesToSend = str.encode(msg)

    udpSocket.sendto(bytesToSend, address)