from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

DB = 'sqli.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT);")
    c.execute("DELETE FROM users;")
    c.execute("INSERT INTO users(username,password) VALUES ('alice','alicepass'), ('bob','bobpass');")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
    <h2>Login</h2>
    <form method="GET" action="/login">
      Username: <input name="username"><br>
      Password: <input name="password"><br>
      <input type="submit" value="Login">
    </form>
    '''

@app.route('/login')
def login():
    uname = request.args.get('username','')
    pwd = request.args.get('password','')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # VULN: concatenation SQL non parameterisée
    query = f"SELECT username FROM users WHERE username = '{uname}' AND password = '{pwd}';"
    try:
        c.execute(query)
        row = c.fetchone()
        if row:
            return f"Welcome, {row[0]}!"
        else:
            return "Invalid credentials"
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()

@app.route('/flag')
def flag():
    # endpoint qui retourne le flag si on parvient à bypasser l'auth
    return open('flag.txt').read()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
