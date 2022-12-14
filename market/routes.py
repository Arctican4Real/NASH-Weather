from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '%f43A9Uo4'
app.config['MYSQL_DB'] = 'weather_db'
app.config['SECRET_KEY'] = 'GDtfDCFYryy'

mysql = MySQL(app)

@app.route('/')
@app.route('/about-team')
def about_team():
    return render_template('about-team.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    global username
    global password
    # Output message if something goes wrong...

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
    # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
    # Fetch one record and return result
    account = cursor.fetchone()
    # If account exists in accounts table in out database
    if account:
        # Create session data, we can access this data in other routes
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
        # Redirect to home page
        return 'Logged in successfully!'
    else:
        # Account doesnt exist or username/password incorrect
        msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    global username
    global password
    global email_address

    msg = ''

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access

        username = request.form['username']
        password = request.form['password']
        email_address = request.form['email']
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'


    # Show registration form with message (if any)
        # Check if account exists using MySQL


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
    account = cursor.fetchone()
    # If account exists show error and validation checks
    if account:
        msg = 'Account already exists!'
    elif not re.match(r'[^@]+@[^@]+\.[^@]+'):
        msg = 'Invalid email address!'
    elif not re.match(r'[A-Za-z0-9]+', username):
        msg = 'Username must contain only characters and numbers!'
    elif not username or not password or not email_address:
        msg = 'Please fill out the form!'
    else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
        cursor.execute("INSERT INTO user (user_id,username,city,email_address,country,password) VALUES ( %s, %s, %s, %s)",
                       (username, 'Tokyo', email_address,'Japan',password))
        mysql.connection.commit()
        msg = 'You have successfully registered!'







