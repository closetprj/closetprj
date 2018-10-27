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

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

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

def get_user_watchlists_id(watchlistname):
    db = get_db()
    auth_user = session.get("username")

    cur = db.execute(
        'select * from user_watchlists where user_watchlists.username = ? and user_watchlists.watchlist_name = ?',[auth_user,watchlistname])
    watchlistsid = cur.fetchall()
    return watchlistsid

def delete_watchlist_method(username,watchlistname,watchlistid):
    db = get_db()
    print(username,watchlistname,watchlistid)
    cur = db.execute(
        'DELETE FROM user_watchlists and kart where kart.username=? and kart.user_watchlist_id=? and watchlists.username=? and user_watchlists.firstName =?  and user_watchlists.watchlist_id =?',
        [username,watchlistid,username,watchlistname,watchlistid])
    db.commit()
    cur.fetchall()
    cur.close()

@app.route("/productDescription")
def productDescription():
    meg = request.args.get("name").split("_")
    watchlistname = meg[0]
    watchlistid = meg[1]
    productId = meg[3]
    with sqlite3.connect('user.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ' + productId)
        productData = cur.fetchone()
    conn.close()
    noOfItems=getnum(watchlistid)
    return render_template("productDescription.html", data=productData, loggedIn = True, firstName = watchlistname,noOfItems=noOfItems, watchlistid=watchlistid,productId=productId,watchlistname=watchlistname)
@app.route("/account/profile")
def profileHome():
    meg = request.args.get("name").split("_")
    watchlistname = meg[0]
    watchlistid = meg[1]
    return render_template("profileHome.html", watchlistname=watchlistname,watchlistid = watchlistid,loggedIn=True, firstName=watchlistname)

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

@app.route("/addToCart")
def addToCart():
        auth_user = session.get("username")
        meg = request.args.get("name").split("_")
        watchlistname = meg[0]
        watchlistid = meg[1]
        productId = meg[3]

        with sqlite3.connect('user.db') as conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO kart (watchlist_id,username, productId) VALUES (?,?,?)", (watchlistid,auth_user, productId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
            cur = conn.cursor()
        conn.close()
        noOfItems = getnum(watchlistid)
        [teplow, tephigh, itemData, categoryDataM, categoryDataF] = pushclo(auth_user, watchlistid)
        itemData = parse(itemData)
        return render_template('shoppingpage.html', watchlistname=watchlistname, watchlistid=watchlistid, loggedIn=True,
                               firstName=watchlistname, noOfItems=noOfItems, categoryDataM=categoryDataM,
                               categoryDataF=categoryDataF, itemData=itemData, tephigh=tephigh,
                               teplow=teplow)
@app.route("/search", methods=["GET", "POST"])
def search():
    meg = request.args.getlist("aa")[0].split('_')
    watchlistname = meg[0]
    watchlistid = meg[1]
    keyword=request.args.getlist("keyword")[0]
    keyword=str(keyword)
    with sqlite3.connect('user.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products WHERE products.name like '%"+keyword+"%' or products.description like '%"+keyword+"%'")
        data = cur.fetchall()
        print(data)
        print(1)
        if not data:
            cur.execute(
                "SELECT categories.type,categories.categoryId FROM categories WHERE  categories.type like '%"+keyword+"%'")
            cate = cur.fetchall()
            print(cate)
            for row in cate:
                print(row[1])
                cur.execute(
                 "SELECT products.productId, products.name, products.price, products.image FROM products WHERE products.categoryId= ? ",(str(row[1])))
                data = data+cur.fetchall()
    conn.close()
    data = parse(data)
    num = getnum(watchlistid)
    return render_template('search.html', data=data, loggedIn=True, firstName=watchlistname, noOfItems=num,

                           searchName=keyword, watchlistid=watchlistid, watchlistname=watchlistname)

@app.route("/account/profile/edit")
def editProfile():
    with sqlite3.connect('user.db') as conn:
        meg = request.args.get("name").split("_")
        watchlistname = meg[0]
        watchlistid = meg[1]
        print(watchlistname,watchlistid)
        cur = conn.cursor()
        cur.execute("SELECT email, firstName, lastName, address1,postcode, city,  phone FROM user_watchlists WHERE watchlist_id = ?",[watchlistid])
        profileData = cur.fetchone()
    # cur.execute("SELECT count(productId) FROM kart WHERE watchlist_id = " + str(profileData.watchlist_id))
    # noOfItems = cur.fetchone()[0]
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=True, firstName=watchlistname,watchlistname=watchlistname,watchlistid=watchlistid)



@app.route("/cart")
def cart():
    auth_user = session.get("username")
    meg = request.args.get("name").split("_")
    watchlistname = meg[0]
    watchlistid = meg[1]
    noOfItems = getnum(watchlistid)
    with sqlite3.connect('user.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT products.productId, products.name, products.price, products.image,kart.items_id FROM products, kart WHERE products.productId = kart.productId AND kart.watchlist_id = ? and kart.username=? ',[watchlistid,auth_user])
        products = cur.fetchall()
    totalPrice = 0
    conn.close()
    for row in products:
        totalPrice += row[2]
    return render_template("shopcart.html", products = products, totalPrice=totalPrice, loggedIn=True, firstName=watchlistname, noOfItems=noOfItems,watchlistname=watchlistname,watchlistid=watchlistid)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    auth_user = session.get("username")
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('user.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT password FROM users WHERE username = ? ",[auth_user])
            password = cur.fetchone()[0]
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE users SET password = ? WHERE username = ?", (newPassword, auth_user))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")

@app.route("/account/profile")
def profileHome():
    meg = request.args.get("name").split("_")
    watchlistname = meg[0]
    watchlistid = meg[1]
    # loggedIn, firstName, noOfItems = getuserDetails(watchlistname,watchlistid)
    return render_template("profileHome.html", watchlistname=watchlistname,watchlistid = watchlistid,loggedIn=True, firstName=watchlistname)

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

app.route('/deletewatchlist', methods=['GET', 'POST'])
def delete_watchlist():
    if not session['logged_in']:
        abort(401)
    meg = request.args.get("name").split("_")
    watchlistname=meg[0]
    watchlistid=meg[1]
    delete_watchlist_method(session['username'], watchlistname,watchlistid)
    flash("delete watch list Success!")
    watchlistsname = get_user_watchlistsname()
    return render_template("dashboard.html",showwatch=1, watchlistsname=watchlistsname)

@app.route('/shutdown')
def shutdown():
    if app.environment == 'test':
        shutdown_server()
    return "Server shutdown"

@app.route("/registerationForm")
def registrationForm():
        return render_template("add_user.html")

@app.route("/eshopping")
def eshopping():
    meg = request.args.get("name").split("_")
    watchlistname = meg[0]
    watchlistid= meg[1]
    with sqlite3.connect('user.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        itemData = cur.fetchall()
        cur.execute('SELECT categoryId, type FROM categories')
        categoryData = cur.fetchall()
    itemData = parse(itemData)
    noOfItems=getnum(watchlistid)
    weather=weather_get()
    print(noOfItems)
    return render_template('shoppingpage.html',watchlistname=watchlistname,watchlistid=watchlistid,loggedIn=True, firstName=watchlistname, noOfItems=noOfItems,categoryData=categoryData,itemData=itemData,weather=weather)


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


