from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField(label='username')
    email_address = StringField(label='email')
    password = PasswordField(label='password')
    confirm_pass = PasswordField(label='confirm_pass')
    submit = SubmitField(label='submit')
