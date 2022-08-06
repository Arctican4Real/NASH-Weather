from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import requests
import googlemaps



# Geocoding an address







app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '%f43A9Uo4'
app.config['MYSQL_DB'] = 'weather_db'
app.config['SECRET_KEY'] = '422434344re5ttrhttyyty'

mysql = MySQL(app)
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about-team')
def about_team():
    return render_template('about-team.html')
@app.route('/thank-you')
def thankyou():


        return render_template('thankyou.html')



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
            session['city'] = account['city']
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

@app.route('/in_out', methods=['GET', 'POST'])
def in_out():
    day_answer = ""
    date_answer = ""
    user_places = ""
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE city = %s', (session['username'],))
        city_name = cursor.fetchone()
        if request.method == 'POST' and 'activities' in request.form:
            API_KEY = 'AIzaSyBAUMU9qR_LunUtnYBjGvGCnUQiskMSM6s'
            gmaps = googlemaps.Client(key=API_KEY)

            user_active = request.form['activities']
            api_key = "8776f806b932063c168f0b4c30df78fd"

            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'

            req = requests.get(url)
            data = req.json()

            name = data['name']
            lon = data['coord']['lon']
            lat = data['coord']['lat']

            exclude = "hourly,minutely,current,alerts"
            url2 = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=%s&appid=%s&units=metric" % (
                lat, lon, exclude, api_key)
            print(url2)

            req2 = requests.get(url2)
            data2 = req2.json()

            temp = []
            clouds = []
            date = []

            for index in range(1, 4):
                temp.append(data2["daily"][index]["temp"]["day"])
                clouds.append(data2['daily'][index]['clouds'])

                date.append(data2['daily'][index]['dt'])

            weather = []
            temper = []
            for i in clouds:
                if 0 <= i <= 25:
                    weather.append('high intensity')
                elif 25 < i <= 84:
                    weather.append('medium intensity')
                elif 84 < i <= 100:
                    weather.append('low intensity')
            for j in temp:
                if 0 <= j <= 10:
                    temper.append('low intensity')
                elif 10 < j <= 22:
                    temper.append('medium intensity')
                elif j > 22:
                    temper.append('high intensity')

            level1, level2, level3 = weather
            level4, level5, level6 = temper

            high_string = 'high'
            medium_string = 'medium'

            temp_intense = []

            if high_string in level1 or level4:
                temp_intense.append('high int')
            elif medium_string in level1 or level4:
                temp_intense.append('med int')
            else:
                temp_intense.append('low int')

            if high_string in level5:
                temp_intense.append('high int')
            elif high_string in level2:
                temp_intense.append('high int')
            elif medium_string in level5:
                temp_intense.append('medium int')
            elif medium_string in level5:
                temp_intense.append('medium int')
            else:
                temp_intense.append("low int")

            if high_string in level6:
                temp_intense.append('high int')
            elif high_string in level3:
                temp_intense.append('high int')
            elif medium_string in level6:
                temp_intense.append('medium int')
            elif medium_string in level3:
                temp_intense.append('medium int')
            else:
                temp_intense.append("low int")

            int1, int2, int3 = temp_intense

            activities = ['Football', 'Tennis', 'Baseball', 'Basketball', 'Running', 'Hurdling'
                                                                                     'Amusement Park', 'Cycling',
                          'Boating',
                          'Camping', 'Hiking', 'Beach',
                          'Bowling', 'Shopping', 'Eating Out', 'Indoor Swimming', 'Museums', 'Gym']

            high_int = []
            medium_int = []
            low_int = []

            for active in activities:
                if user_active == active:
                    if active == 'Football' or active == 'Tennis' or active == 'Baseball' or active == 'Basketball' or active == 'Running' or active == 'Hurdling':
                        low_int.append(active)
                    elif active == 'Amusement Park' or active == 'Beach' or active == 'Cycling' or active == 'Boating' or active == 'Camping' or active == 'Hiking':
                        medium_int.append(active)
                    elif active == 'Bowling' or active == 'Shopping' or active == 'Eating Out' or active == 'Indoor Swimming' or active == 'Museums' or active == 'Gym':
                        high_int.append(active)

            day_answer = ""
            date_answer = ""

            for high_value in high_int:
                if level4 == 'high intensity' and level5 == 'high intensity':
                    day_answer = temp[0]

                    date_answer = date[0]

                elif level5 == 'high intensity' and level6 == 'high intensity':
                    day_answer = temp[1]

                    date_answer = date[1]

                elif level6 == 'high intensity' and level4 == 'high intensity':
                    day_answer = temp[2]

                    date_answer = date[2]

                elif level4 == 'high intensity':

                    day_answer = temp[0]

                    date_answer = date[0]

                elif level5 == 'high intensity':

                    day_answer = temp[1]

                    date_answer = date[1]

                elif level6 == 'high intensity':

                    day_answer = temp[2]

                    date_answer = date[2]

                else:
                    day_answer = "NO GOOD DAY FOR ACTIVITY"

            for medium_value in medium_int:
                if level4 == 'medium intensity' and level5 == 'medium intensity':
                    day_answer = temp[0]

                    date_answer = date[0]

                elif level5 == 'medium intensity' and level6 == 'medium intensity':
                    day_answer = temp[1]

                    date_answer = date[1]

                elif level6 == 'medium intensity' and level4 == 'medium intensity':
                    day_answer = temp[2]

                    date_answer = date[2]

                elif level4 == 'medium intensity':

                    day_answer = temp[0]

                    date_answer = date[0]

                elif level5 == 'medium intensity':

                    day_answer = temp[1]

                    date_answer = date[1]

                elif level6 == 'medium intensity':

                    day_answer = temp[2]

                    date_answer = date[2]

                else:
                    print('NO DAY GOOD FOR YOUR ACTIVITY')

            for low_value in low_int:
                if level4 == 'low intensity' and 5 == 'low intensity':

                    day_answer = temp[0]

                    date_answer = date[0]
                    print(date_answer)
                elif level5 == 'low intensity' and level6 == 'low intensity':

                    day_answer = temp[1]

                    date_answer = date[1]

                elif level6 == 'low intensity' and level4 == 'low intensity':

                    day_answer = temp[2]

                    date_answer = date[2]

                elif level4 == 'low intensity':

                    day_answer = temp[0]

                    date_answer = date[0]

                elif level5 == 'low intensity':

                    day_answer = temp[1]

                    date_answer = date[1]

                elif level6 == 'low intensity':

                    day_answer = temp[2]

                    date_answer = date[2]

                else:
                    day_answer = "NO GOOD DAY FOR ACTIVITY"

                placese = gmaps.places_nearby(location=f'{lat},{lon}', radius=40000, open_now=False,
                                              type='point_of_interest', keyword=f'{user_active}')
                user_places = ""
                for index in range(1):
                    user_places = (placese["results"][index]["name"])

        return render_template('in-out.html', day_answer=day_answer, date_answer=date_answer, user_places=user_places,
                               city_name=session['city'])