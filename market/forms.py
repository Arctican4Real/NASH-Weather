from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired


class RegisterForm(FlaskForm):
    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    confirm_pass = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Your Account')
