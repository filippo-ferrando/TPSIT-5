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

def select_op_id(id):   #returna w.1 oppure w.1;s.3 in base alla query scritta sul db
    conn = create_connection("operation.db")
    cur = conn.cursor()         #in pratica questo serve solamente a fare le query per fare il retrive della lista di comandi
    cur.execute(f"SELECT idOperazione, operazione FROM CALCOLI Where idClientAsseg = {id}") #esecuzione della query
    rows = cur.fetchall()

    opDict = {}

    for row in rows:
        opDict[int(row[0])] = row[1]

    conn.close()

    return jsonify(opDict)

def update_op_id(id, result):   #returna w.1 oppure w.1;s.3 in base alla query scritta sul db
    conn = create_connection("operation.db")
    cur = conn.cursor()         #in pratica questo serve solamente a fare le query per fare il retrive della lista di comandi
    cur.execute(f"UPDATE CALCOLI SET risultato = {result} Where idOperazione = {id}") #esecuzione della query
    cur.execute("commit")
    conn.close()

def del_op_id(id):   #returna w.1 oppure w.1;s.3 in base alla query scritta sul db
    conn = create_connection("operation.db")
    cur = conn.cursor()         #in pratica questo serve solamente a fare le query per fare il retrive della lista di comandi
    cur.execute(f"DELETE FROM CALCOLI Where idOperazione = {id}") #esecuzione della query
    cur.execute("commit")
    conn.close()

def add_op_id(op, idC):   #returna w.1 oppure w.1;s.3 in base alla query scritta sul db
    conn = create_connection("operation.db")
    cur = conn.cursor()         #in pratica questo serve solamente a fare le query per fare il retrive della lista di comandi
    cur.execute(f"INSERT INTO CALCOLI (operazione, idClientAsseg) VALUES ('{op}', '{idC}')") #esecuzione della query
    cur.execute("commit")
    conn.close()

@app.route('/api/v1/operation', methods=['GET'])
def operazioneClient():
    diz = request.args.to_dict()
    op = select_op_id(diz['id'])
    print(op)
    return op

@app.route('/api/v1/result', methods=['GET'])
def updateRes():
    diz = request.args.to_dict()
    try:
        update_op_id(diz['id'], diz['result'])
    except:
        print("Errore")
    return str(diz['result'])

@app.route('/api/v1/delete', methods=['GET'])
def delOP():
    diz = request.args.to_dict()
    try:
        del_op_id(diz['id'])
    except:
        print("Errore")
    return "deleted"

@app.route('/api/v1/add', methods=['GET'])
def addOP():
    diz = request.args.to_dict()
    try:
        add_op_id(diz['op'], diz['id'])
    except:
        print("Errore")
    return "added"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')