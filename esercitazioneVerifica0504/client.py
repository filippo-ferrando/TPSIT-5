import requests
import time

def main():
    id = input("Inserisci id: ")
    oper = requests.get(f"http://localhost:5000/api/v1/operation?id={id}")
    print(oper.json())

    for key, value in oper.json().items():
        #print(key, value)
        result = requests.get(f"http://localhost:5000/api/v1/result?id={key}&result={eval(value)}")

def delete():
    id = input("inserisci id da cancellare: ")
    deletion = requests.get(f"http://localhost:5000/api/v1/delete?id={id}")
    print("Deletion complete")

def add():
    id = input("inserisci id del client assegnato: ")
    op = input("inserisci operazione: ")
    addition = requests.get(f"http://localhost:5000/api/v1/add?id={id}&op={op}")
    print("addition complete")

if __name__ == '__main__':
    s = input("resolve op: 1 | delete op: 2 | add op: 3 --> ")
    if s == "1":
        main()
    elif s == "2":
        delete()
    else:
        add()