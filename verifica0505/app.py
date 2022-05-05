import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, redirect, url_for, make_response
import time, random, string
from datetime import datetime
from flask import jsonify

app = Flask(__name__)

def create_connection(db_file): #funzione per connettere il database allo script
    conn = None
    try:
        conn = sqlite3.connect(db_file) #attiva connessione al db
    except Error as e: #gestione dell'errore
        print(e)

    return conn

def select_velox_by_id(id):   #returna w.1 oppure w.1;s.3 in base alla query scritta sul db
    conn = create_connection("velox.db")
    cur = conn.cursor()         #in pratica questo serve solamente a fare le query per fare il retrive della lista di comandi
    cur.execute(f"SELECT via, citta, prov FROM VELOX WHERE id = '{str(id)}'") #esecuzione della query
    rows = cur.fetchall()
    l = []
    for row in rows:
        l.append((row[0], row[1], row[2]))

    return l

    conn.close()

def add_record(targa, velocita, data, ora, idVelox):   #aggiunge un record al db sulla tabella REGISTRO
    conn = create_connection("velox.db")
    cur = conn.cursor()  
    cur.execute(f"INSERT INTO REGISTRO (targa, velocita, data, ora, idVelox) VALUES ('{targa}', '{velocita}', '{data}', '{ora}', '{idVelox}')") #esecuzione della query
    cur.execute("commit")
    conn.close()

def select_targa_by_vel(idVelox, vLimite):   #Cerca una targa in base all'autovelox e se ha superato una certa velocità
    conn = create_connection("velox.db")
    cur = conn.cursor()         
    cur.execute(f"SELECT targa FROM REGISTRO Where idVelox = '{idVelox}' AND velocita >= {vLimite}") #esecuzione della query
    rows = cur.fetchall()

    for row in rows:
        return row[0]

    conn.close()


# ENDPOINT

@app.route('/api/v1/research', methods=['GET'])
def searchInd():
    diz = request.args.to_dict() # argomenti dalle request
    l = []
    try:
        l = select_velox_by_id(diz['id'])
        dati = "".join(str(l) for l in l) #conversione da lista a stringa
        return dati
    except:
        return "errore"

@app.route('/api/v1/addR', methods=['GET'])
def operazioneClient():
    diz = request.args.to_dict()
    try:
        add_record(diz['targa'], diz['velocita'], diz['data'], diz['ora'], diz['idVelox'])
        return "added record"
    except:
        return "errore"

@app.route('/api/v1/researchTV', methods=['GET'])
def searchTarga():
    diz = request.args.to_dict()
    try:
        targa = select_targa_by_vel(diz['idVelox'], diz['vLimite'])
        if targa == None:
            targa = "non trovato"
        return targa
    except:
        return "errore"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')