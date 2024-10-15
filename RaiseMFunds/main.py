from flask import Flask, render_template, jsonify, request, make_response, redirect
import sqlite3 as s3

app = Flask('app')

conn = s3.connect("main.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  place_of_origin TEXT NOT NULL,
  story TEXT NOT NULL,
  amount_raised REAL NOT NULL
)
""")

def add_user(username, password):
    try:
        conn = s3.connect("main.db")
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, password))
        conn.commit()
        conn.close()
        print(f"user '{username}' added successfully.")
        return True
    except s3.IntegrityError:
        print(f"Error: Username '{username}' already exists")
        return False

def list_users():
    conn = s3.connect("main.db")
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM users
    ''')
    users = cursor.fetchall()
    conn.close()
    return users

def login_user(username, password):
    conn = s3.connect("main.db")
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE username = ?
    ''', (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        stored_password = user[2]
        if password == stored_password:
            print(f"User '{username}' logged in successfully")
            return True
        else:
            print("Error: Incorrect password.")
            return False
    else:
        print("Error: Username not found")
        return False

def search_post(query, page, per_page):
    offset = (page - 1) * per_page
    conn = s3.connect("main.db")
    cursor = conn.cursor()
    cursor.execute('''
                    SELECT name, place_of_origin, story, amount_raised FROM posts
                    WHERE name LIKE ? OR story LIKE ? OR place_of_origin LIKE ?
                    ORDER BY id DESC
                    LIMIT ? OFFSET ?
                   ''', (f"%{query}%", f"%{query}%", f"%{query}%", per_page, offset))
    results = cursor.fetchall()
    cursor.execute('''
                    SELECT COUNT(*) FROM posts 
                    WHERE name LIKE ? OR story LIKE ? OR place_of_origin LIKE ?
                   ''', (f"%{query}%", f"%{query}%", f"%{query}%"))
    total_results = cursor.fetchone()[0]
    conn.close()
    return results, total_results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registerUser', methods=["POST"])
def register_user():
    data = request.get_json()
    user = data.get('email')
    pwd = data.get('password')
    if add_user(user, pwd):
        return jsonify({"message": "User registered successfully."}), 201
    else:
        return jsonify({"error": "Email already exists."}), 400

@app.route('/checkLogin', methods=['POST'])
def check_login():
    data = request.get_json()
    user = data.get('email')
    pwd = data.get("password")
    if login_user(user, pwd):
        response = make_response(redirect("/explore"))
        response.set_cookie("email", user)
        return response
    else:
        return jsonify({"error": "Parameters not met"}), 401

@app.route('/explore')
def explore():
    return render_template('explore.html')

if __name__ == '__main__':
    app.run()
