import requests
import time

def add():
    print("Inserisci i campi necessari: \n")
    targa = input("Inserisci la targa: ")
    velocita = input("Inserisci velocità: ")
    data = input("Inserisci la data: ")
    ora = input("Inserisci l'ora: ")
    idVelox = input("Inserisci id velox: ")

    add = requests.get(f"http://localhost:5000/api/v1/addR?targa={targa}&velocita={velocita}&data={data}&ora={ora}&idVelox={idVelox}")
    print(add.text)

def searchInd():
    id = input("Inserisci id velox: ")
    velox = requests.get(f"http://localhost:5000/api/v1/research?id={id}")
    print(velox.text)

def searchTarga(): 
    idVelox = input("Inserisci id velox: ")
    vLimite = input("inserisci velocità limite: ")
    sTarga = requests.get(f"http://localhost:5000/api/v1/researchTV?idVelox={idVelox}&vLimite={vLimite}")
    print(sTarga.text)

def main(): #menu scelta operazione
    c = input("aggiungi record: 1 | cerca velox: 2 | cerca targa: 3 --> ")
    if c == "1":
        add()
    elif c == "2":
        searchInd()
    elif c == "3":
        searchTarga()
    else:
        print("opzione non riconosciuta")

if __name__ == "__main__":
    main()