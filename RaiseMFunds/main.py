from flask import Flask, render_template
from datetime import datetime
import sqlite3 as s3

conn = s3.connect("main.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
          password TEXT NOT NULL
)
 ''')

def add_user(username, password):
    try:
        cursor.execute('''
        INSERT INTO users (username,password) VALUES (?,?)
        ''', (username, password))
        conn.commit()
        print(f"user '{username} added succesfully.")
    except s3.IntegrityError:
        print(f"Error: Username '{username}' already exists")
def list_users():
    cursor.execute('''
    SELECT * FROM users 
    ''',(username))
    user = conn.fetchall()
    return list_users
def login_user(username,password):
    cursor.execute('''
    SELECT * FROM users WHERE username = ?
    ''', (username))
    user = y.fetchone()
    if user:
        stored_password = user[2]
        if password == stored_password:
            print(f"User '{username}' logged in succesfully")
            return True
        else:
            print("Error: Incorrect password.")
            return False
    else:
        print("Error: Username not found")
        return False



app = Flask('app')

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login')
def Susan():
    return render_template('login.html')
app.run()




