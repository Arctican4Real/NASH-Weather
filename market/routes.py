from market import app
from flask import render_template


@app.route('/')
@app.route('/about-team')
def about_team():
    return render_template('about-team.html')

