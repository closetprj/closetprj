import sqlite3

#Open database
conn = sqlite3.connect('user.db')

conn.execute('''drop table if exists users;''')
conn.execute('''create table users (
  username text primary key,
  password text not null
)''')
conn.execute('''drop table if exists user_watchlists;''')
conn.execute('''create table user_watchlists(
  watchlist_id integer primary key AUTOINCREMENT,
  username text,
  email TEXT,
  gender text,
  firstName TEXT,
  lastName TEXT,
  address1 TEXT,
		postcode TEXT,
		city TEXT,
		phone TEXT,
  foreign key(username) references users(username)
)''')

conn.execute('''drop table if exists products;''')
conn.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY,
		name TEXT,
		price REAL,
		gender text,
		description TEXT,
		image TEXT,
		stock INTEGER,
		categoryId INTEGER,
		state text,
		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
		)''')

conn.execute('''drop table if exists categories;''')
conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		type TEXT,
		gender text
		)''')

conn.execute('''CREATE TABLE kart
    (watchlist_id integer,
    items_id integer PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    productId INTEGER,
    FOREIGN KEY(watchlist_id) REFERENCES user_watchlists(watchlist_id),
    FOREIGN KEY(username) REFERENCES users(username),
    FOREIGN KEY(productId) REFERENCES products(productId)
    )''')
conn.execute('''drop table if exists ordernum;''')
conn.execute('''CREATE TABLE ordernum(
    watchlist_id integer,
    order_id integer PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    status text,
    FOREIGN KEY(watchlist_id) REFERENCES user_watchlists(watchlist_id),
    FOREIGN KEY(username) REFERENCES users(username)
    )''')

conn.execute('''drop table if exists state;''')
conn.execute('''CREATE TABLE state
    (watchlist_id integer,
    username TEXT,
    order_id integer,
    productId INTEGER,
    FOREIGN KEY(watchlist_id) REFERENCES user_watchlists(watchlist_id),
    FOREIGN KEY(username) REFERENCES users(username),
    FOREIGN KEY(productId) REFERENCES products(productId),
    FOREIGN KEY(order_id) REFERENCES ordernum(order_id)
    )''')
conn.commit()
conn.close()