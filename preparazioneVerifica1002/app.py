import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, redirect, url_for, make_response
import time, random, string
from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from datetime import datetime

x = symbols('x')

app = Flask(__name__)
token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

def create_connection(db_file): #funzione per connettere il database allo script
    conn = None
    try:
        conn = sqlite3.connect(db_file) #ettiva connessione al db
    except Error as e: #gestione dell'errore
        print(e)

    return conn

def history(user, operation, estMin, estMax, solution):
    conn = create_connection("db.db")
    cur = conn.cursor()         #in pratica questo serve solamente a fare le query per fare il retrive della lista di comandi
    cur.execute(f"INSERT INTO OPERATIONLOGGING (USERNAME, OPERATION, EstMin, EstMax, SOLUTION) VALUES ('{user}', '{operation}', '{estMin}', '{estMax}', '{solution}')") #esecuzione della query
    cur.execute("commit")
    conn.close()

def logUser(user):
    conn = create_connection("db.db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO USERLOG (USERNAME, DATE) VALUES ('{user}', '{datetime.today()}')")
    cur.execute("commit")
    conn.close()

def validate(username, password):
    completion = False
    con = sqlite3.connect('./db.db')
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    con.close()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            resp = make_response(redirect(url_for('secret')))
            resp.set_cookie('username', username)
            logUser(username)
            return resp
    return render_template('login.html', error=error)

@app.route(f'/{token}', methods=['GET', 'POST'])
def secret():
    if request.method == 'POST':
        username = request.cookies.get('username')
        print(username)
        if request.form['estMax'] == "" and request.form['estMin'] == "":
            operation = parse_expr(request.form['operation'])
            print(operation)
            solution = integrate(operation, x)
            history(username, operation, "", "", solution)
            print(solution)
        else:
            operation = parse_expr(request.form['operation'])
            print(operation)
            eMin = request.form['estMin']
            eMax = request.form['estMax']
            solution = integrate(operation, (x, eMin, eMax))
            history(username, operation, eMin, eMax, solution)
            print(solution)

    elif request.method == 'GET':
        username = request.cookies.get('username')
        resp = make_response(render_template('calcolo.html'))
        resp.set_cookie('username', username)
        return resp


    resp = make_response(render_template("calcolo.html", solution=solution))
    resp.set_cookie('username', username)
    return resp

if __name__== "__main__":
    app.run(debug=True)

        

    

if __name__== "__main__":
    app.run(debug=True)
