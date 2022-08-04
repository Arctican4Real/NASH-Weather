from market import app
from flask import render_template


@app.route('/')
@app.route('/about-team')
def about_team():
    return render_template('about-team.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login_Page():
    return render_template('loginPage.html')
