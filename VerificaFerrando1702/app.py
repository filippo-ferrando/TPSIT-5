import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, redirect, url_for, make_response
import time, random, string
from datetime import datetime
import semaforo

s = semaforo.semaforo()

'''
FUNZIONAMENTO
Il semaforo parte da una situazione si spegnimento totale (stato, prevstato = false)
la prima istruzione che si manda sarà quindi da mandare con il pulsante di accensione (accendi)
dopodichè le altre modifiche A SEMAFORO ACCESO andranno inviate con il pulsante send
quando vorremo spegnere il semaforo inseriremo i dati per la durata del semaforo giallo e per la durata delle luci spente per poi invialo con il pulsante accendi
per riaccendere il semaforo basterà premere nuovamente il pulsante accendi con inserita nei form la configurazione desiderata
'''

app = Flask(__name__)
token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

def create_connection(db_file): #funzione per connettere il database allo script
    conn = None
    try:
        conn = sqlite3.connect(db_file) #ettiva connessione al db
    except Error as e: #gestione dell'errore
        print(e)

    return conn

def history(user, operation):
    conn = create_connection("db.db")
    cur = conn.cursor()         #Funzione per scrivere una riga sulla tabella dedicata allo spegnimento e riaccesione del semaforo, questa inserisce utente, stato e data
    cur.execute(f"INSERT INTO UOLOGGING (USER, OPERAZIONE, DATA) VALUES ('{user}', '{operation}', '{datetime.today()}')") #esecuzione della query
    cur.execute("commit")   
    conn.close()

def validate(username, password):
    completion = False
    con = sqlite3.connect('./db.db') #creo la connessione al database
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM USERS") #seleziono tutti i dati della tabella user
    rows = cur.fetchall()
    con.close()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username: #confronte le credenziali inserite con quelle nel DB
            completion=check_password(dbPass, password)
    return completion #returna True o False in base alla correttezza della password

def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username'] #richiedo l'username
        password = request.form['password'] #richiedo la password
        completion = validate(username, password) #controllo la password
        if completion ==False:
            error = 'Invalid Credentials. Please try again.' #password errata
        else:
            resp = make_response(redirect(url_for('secret'))) #se la password è giusta creo la risposta per i client settando l'username di questo come cookie
            resp.set_cookie('username', username)
            return resp
    return render_template('login.html', error=error)

global STATO, PREVSTATO #variabili globali per il controllo dell'accensione / spegnimento
STATO = False
PREVSTATO = False


@app.route(f'/{token}', methods=['GET', 'POST'])
def secret():
    global STATO, PREVSTATO

    if request.method == 'POST':
        username = request.cookies.get('username') #richiedo l'username (servirà per settare i cookie nella risposta della pagina)

        if request.form.get("acceso") == "accendi": #il tasto accendi serve sia ad accendere il semaforo che a spegnerlo
            PREVSTATO = STATO
            STATO = not (STATO)
        else:
            pass

        #print(STATO)
        #print(PREVSTATO)
            
        if STATO == True and PREVSTATO == True: #normale funzionamento acceso (mandando i comandi dal pulsante send i dati vengono modificati da qui)
            verdeT = int(request.form["Dverde"])
            gialloTA = int(request.form["Dgiallo"])
            rossoT = int(request.form["Drosso"])

            s.rosso(rossoT)
            s.giallo(gialloTA)
            s.verde(verdeT)

        elif STATO == True and PREVSTATO == False: # quando viene premuto il tasto accendi dopo uno spegnimento questo riaccende il semaforo con i parametri passati
            verdeT = int(request.form["Dverde"])
            gialloTA = int(request.form["Dgiallo"])
            rossoT = int(request.form["Drosso"])
            s.rosso(rossoT)
            s.giallo(gialloTA)
            s.verde(verdeT)
            history(username, "ri-attivato")
            PREVSTATO = True

        elif STATO == False: # quando viene premuto il tasto accendi al semaforo acceso, a questo bisogna passare il tempo della luce gialla e quello delle luci spente
            gialloTS = int(request.form["Dgiallo"])
            lsT = int(request.form["Dls"])

            s.giallo(gialloTS)
            s.luci_spente(lsT)
            history(username, "spento")
            PREVSTATO = False


    elif request.method == 'GET':
        username = request.cookies.get('username')
        resp = make_response(render_template('index.html'))
        resp.set_cookie('username', username)
        return resp


    resp = make_response(render_template("index.html"))
    resp.set_cookie('username', username)
    return resp

if __name__== "__main__":
    app.run(debug=True)

