from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '%f43A9Uo4'
app.config['MYSQL_DB'] = 'weather_db'
app.config['SECRET_KEY'] = '422434344re5ttrhttyyty'

mysql = MySQL(app)
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about-team')
def about_team():
    return render_template('about-team.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username1 = request.form['username']
        password1= request.form['password']

    # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username1, password1,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['username'] = account['username']
            # Redirect to home page
            print("logged in ")
            msg = 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access

        username = request.form['username']
        password = request.form['password']
        email_address = request.form['email']
        city = request.form['city']
        country = request.form['country']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_address):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email_address:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute("INSERT INTO user (username,city,email_address,country,password) VALUES (%s, %s, %s, %s, %s)", (username, city, email_address, country,password ,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'



    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    # Check if account exists using MySQL
    return render_template('register.html', msg=msg)

#cursor.execute("INSERT INTO user (user_id,username,city,email_address,country,password) VALUES ( %s, %s, %s, %s)",(username, 'Tokyo', email_address,'Japan',password))
# cursor.execute('SELECT * FROM user WHERE username = %s', (username,))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('country', None)
    session.pop('city', None)
    # Redirect to login page
    return redirect(url_for('index'))