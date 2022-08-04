from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired
from wtforms.validators import email_validator
class RegisterForm(FlaskForm):
    username = StringField(label='User Name', validators=[Length( max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    confirm_pass = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    country = StringField(label='Your Country?', validators=[Length(min=2, max=56), DataRequired()])
    city =  StringField(label='Your City?', validators=[Length(min=2, max=50), DataRequired()])
    submit = SubmitField(label='Create Your Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

