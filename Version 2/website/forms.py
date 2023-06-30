from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField

class RegistrationForm(FlaskForm):
    username = StringField()