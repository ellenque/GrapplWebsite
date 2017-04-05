import os
from flask import Flask, render_template, request, session, redirect, url_for, escape, send_file
from flask_bootstrap import Bootstrap
import sqlite3

name = "App Name"

# Create SQL database and user table
conn = sqlite3.connect('website.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (email text, name text, password text)')
conn.commit()

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.urandom(24)

@app.route("/")
def home():
  if 'username' in session:
    return render_template('index.html', user=session['username'], notifications=session['notifications'])
  return render_template('index.html')

@app.route("/register", methods=['GET','POST'])
def register():
  if request.method == 'POST':
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    register_user(email, username, password)
    return render_template('registeraccept.html')
  return render_template('register.html')

@app.route("/login", methods=['GET','POST'])
def login():
  if request.method == 'POST':
    session['username'] = request.form['email']
    session['notifications'] = 1
    print(session['username'] + " has logged in")
    result = authenticate(session['username'], request.form['password'])
    if result:
      return redirect(url_for('home'))
    return redirect(url_for('login'))

  return render_template('login.html')

@app.route("/logout")
def logout():
  session.pop('username', None)
  return redirect(url_for('home'))

@app.route("/profile")
def profile():
  if 'username' in session:
    session['notifications'] = 0
    return render_template('profile.html', user=session['username'])
  return redirect(url_for('login'))

@app.route("/upgrade")
def upgrade():
  if 'username' in session:
    return render_template('upgrade.html', user=session['username'], notifications=session['notifications'])
  return redirect(url_for('login'))

@app.route("/download")
def filedat():
  return send_file('static/file.dat', mimetype='application/jar', attachment_filename='file.jar', as_attachment=True)

@app.route("/admin")
def admin():
  if 'username' in session:
    if session['username'] == "admin":
      return render_template('admin.html')
    return 'Nope!'
  return 'Nope!'

@app.route("/privpolicy")
def privacypolicy():
  if 'username' in session:
    return render_template('privpolicy.html', user=session['username'], notifications=session['notifications'])
  return render_template('privpolicy.html')

def register_user(email, name, password):
  print("Registering user: " + name)
  cur.execute("INSERT INTO users VALUES ('"+email+"', '"+name+"', '"+password+"')")
  conn.commit()

def authenticate(email, password):
  cur.execute("SELECT * FROM users WHERE email='"+email+"'")
  inp = cur.fetchall() 
  if len(inp) == 0:
    return False
  userdat = inp[0]
  if userdat[2] == password:
    return True
  return False

def exists(email):
  cur.execute("SELECT * FROM users WHERE email='"+emails+"'")
  return len(cur.fetchall()) > 0

if __name__ == "__main__":
  app.run()
