# all the imports
import hashlib
import os
import sqlite3
import re
import time

import urllib.parse
import urllib.request
import json
from time import strftime

import requests
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

os.environ['FLASK_APP'] = 'closet'

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , closet.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path,'user.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('closet_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db(schema='schema.sql'):
    db = get_db()
    with app.open_resource(schema, mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def add_watchlistname(gender,email,firstName,lastName,address1,postcode,city,phone):
    auth_user = session.get("username")
    if not session['logged_in']:
        abort(401)
    db=get_db()
    db.execute("insert into user_watchlists(username,gender,email,firstName,lastName,address1,postcode,city,phone) values (?,?,?,?,?,?,?,?,?)", [auth_user, gender,email,firstName,lastName,address1,postcode,city,phone])
    db.commit()

def get_user_watchlistsname():
    db = get_db()
    auth_user = session.get("username")
    cur = db.execute(
        'select * from user_watchlists where user_watchlists.username = "%s"' % auth_user)
    watchlistsname = cur.fetchall()
    return watchlistsname

def getnum(watchlistid):
    auth_user = session.get("username")
    with sqlite3.connect('user.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT count(productId) FROM kart WHERE watchlist_id = ? and username= ?', [watchlistid,auth_user])
        noOfItems = cur.fetchone()[0]
    conn.close()
    return noOfItems

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        if user and passw:
            db = get_db()
            cur = db.execute("select *  from users where username =? and password=?", [user, passw])
            rows = cur.fetchone()
            cur2 = db.execute("select username  from users")
            rows2 = cur2.fetchone()
            if rows:
                session['logged_in'] = True
                session['username'] = user
                flash("Login Success!")
                watchlistsname = get_user_watchlistsname()
                return render_template('dashboard.html',showwatch=1,watchlistsname=watchlistsname)
            elif user not in rows2:
              error = 'User not registered'
            else:
              error = 'Incorrect username or password'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    time.sleep(1)
    return redirect(url_for('show_watchlists'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    users = [dict(username=row[0], password=row[1]) for row in get_db().execute('select username, password from users order by username desc').fetchall()]
    registeredmembers=[]
    for i in users:
        registeredmembers.append(i['username'])
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']

        cfm_passw = request.form['cfm_password']
        if user in registeredmembers:
            error = 'User already registered'
        elif passw != cfm_passw:
            error = 'Passwords do not match'
        elif len(passw) < 8:
            error = 'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number'
        elif not re.search("[0-9]", passw):
            error = 'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number'
        elif not re.search("[A-Z]", passw):
            error = 'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number'
        else:
            get_db().execute('insert into users (username, password) values (?, ?)', [user, passw])
            get_db().commit()
            flash('You were successfully registered')
            return redirect("login")
    return render_template('register.html', error=error)

@app.route('/addwatchlist', methods=['GET', 'POST'])
def add_watchlist():
    addwatchlist=1
    if not session['logged_in']:
        abort(401)
    else:
        if request.method == 'POST':
            gender=request.form['gender']
            email = request.form['email']
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            address1 = request.form['address1']
            postcode = request.form['postcode']
            city = request.form['city']
            phone = request.form['phone']
            #addwatchlist = None
            add_watchlistname(gender, email, firstName, lastName, address1, postcode, city, phone)
            flash("add charactor succseess")

    watchlistsname = get_user_watchlistsname()
    print(watchlistsname)
    return render_template('dashboard.html',showwatch=1,watchlistsname=watchlistsname, addwathlist=addwatchlist)


@app.route('/shutdown')
def shutdown():
    if app.environment == 'test':
        shutdown_server()
    return "Server shutdown"

@app.route("/registerationForm")
def registrationForm():
        return render_template("add_user.html")

@app.cli.command('start')

def start():
    app.config.from_object(__name__) # load config from this file

    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'uese.db'),
        SECRET_KEY='Production key',
    ))
    app.config.from_envvar('closet_SETTINGS',  silent=True)
    app.run(port=5003)


def test_server():
    ### Setup for integration testing
    app.config.from_object(__name__) # load config from this file

    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'user.db'),
        SECRET_KEY='Test key',
        SERVER_NAME='localhost:5000',
        # DEBUG=True, # does not work from behave
    ))
    app.config.from_envvar('closet_TEST_SETTINGS',  silent=True)
    app.environment = 'test'
    with app.app_context():
        init_db('test_schema.sql')
    app.run()


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running with Werkzeug server")
    if app.environment == 'test':
        func()
        os.unlink(app.config['DATABASE'])

if __name__ == '__main__':
    app.run()


