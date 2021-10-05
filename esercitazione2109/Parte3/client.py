import socket
import threading as thr
import time

registered = False
nickname = ""

SERVER=("192.168.0.100", 5000)

class Receiver(thr.Thread):
    def __init__(self, s): 
        thr.Thread.__init__(self)
        self.running = True 
        self.s = s

    def stop_run(self):
        self.running = False

    def run(self):
        global registered

        while self.running:
            data = self.s.recv(4096).decode()
            
            if data == "OK":
                registered = True
                print(f"\nConnection Accepted...Entering chat mode --> ")
            
            else:
                print(f"\n{data}")

def main():
    global registered
    global nickname
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER)

    ricev = Receiver(s)
    ricev.start()

    while True:
        time.sleep(0.2)

        if not registered:
            nickname = input("insert nickname -->")

            mex = "Nickname:" + nickname
            registered = True

        else:
            destinatario = input("insert desitnation nick -->")

            text = input("insert message -->")
            mex = nickname + ":" + destinatario + ":" + text

        s.sendall(mex.encode())

        if 'exit' in mex.split(":"):
            ricev.stop_run()
            print("Exiting...")
            break

    ricev.join()
    s.close()

if __name__ == "__main__":
    main()