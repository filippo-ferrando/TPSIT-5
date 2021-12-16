import time
import socket

def main():
    target = "www.google.com"
    port = 80

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target, port))

    request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % target
    client.send(request.encode())

    response = client.recv(4096)
    http_response = response

    print(http_response)

if __name__ == "__main__":
    main()
