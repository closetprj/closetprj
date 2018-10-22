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
conn.commit()
conn.close()