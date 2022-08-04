from flask import Flask
app = Flask(__name__)
from flask_mysqldb import MySQL
from market import routes

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '%f43A9Uo4'
app.config['MYSQL_DB'] = 'User'
app.config['SECRET_KEY'] = 'GDtfDCFYryy'

mysql = MySQL(app)
