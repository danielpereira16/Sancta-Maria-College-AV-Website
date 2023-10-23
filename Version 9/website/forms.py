"""Import all necessary files and functions."""
from flask_wtf import FlaskForm  # imports FlaskForm from flask_wtf library
from flask_wtf.file import FileField, FileAllowed  # imports FileField and FileAllowed from flask_wtf.file
from flask_login import current_user  # imports current_user from flask_login
from wtforms import StringField, PasswordField, SelectField, DateTimeLocalField
from wtforms import SubmitField, TextAreaField, EmailField
# imports different fields from wtforms
from wtforms.validators import DataRequired, Length, Email
from wtforms.validators import EqualTo, ValidationError
# imports different validators from wtforms.validators
from .models import User  # imports user from models folder


class RegistrationForm(FlaskForm):  # defines class as RegistrationForm that inherits from FlaskForm
    """Create registration form."""

    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20)])
    # defines a form field username and specifies validators
    email = StringField('Email', validators=[DataRequired(), Email()])
    # defines form field email with specific validators
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    # defines form field password with specific validators
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    # defines form field confirm password with specific validators
    submit = SubmitField('Sign Up')  # defines submit field

    def validate_username(self, username):  # defines a function for validating username
        """Check if username already exists."""
        user = User.query.filter_by(username=username.data).first()
        # checks database if username already exists
        if user:
            raise ValidationError('That username is taken, please choose a different one')
            # shows an error message

    def validate_email(self, email):  # defines function for validating emails
        """Check if email already exists."""
        user = User.query.filter_by(email=email.data).first()  # checks database if the email already exists
        if user:
            raise ValidationError('That email is taken, please choose a different one')
            # shows an error message


class UpdateAccountForm(FlaskForm):  # defines class as UpdateAccountForm that inherits from FlaskForm
    """Create update account form."""

    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20)])
    # defines form field username password with specific validators
    email = StringField('Email', validators=[DataRequired(), Email()])
    # defines form field email password with specific validators
    submit = SubmitField('Update')  # defines submit form field

    def validate_username(self, username):  # defines a function for validating usernames
        """Check if username already exists."""
        if username.data != current_user.username:  # checks if username data is the same as current username
            user = User.query.filter_by(username=username.data).first()  # checks databse if username already exists
            if user:
                raise ValidationError('That username is taken, please choose a different one')
            # shows an error message

    def validate_email(self, email):  # defines a function for validating emails
        """Check if email already exists."""
        if email.data != current_user.email:  # checks if email data is the same as current email
            user = User.query.filter_by(email=email.data).first() # checks if email already exists
            if user:
                raise ValidationError('That email is taken, please choose a different one')
            # shows an error message


class PostForm (FlaskForm):  # defines class as PostForm that inherits form FlaskForm
    """Create post form."""

    title = StringField('Title', validators=[DataRequired()])
    # defines form field as title and specifies validators
    text = TextAreaField('Text', validators=[DataRequired()])
    # defines form field as text and specifies validators
    submit = SubmitField('Create Post')
    # defines submit button

class HireForm(FlaskForm):
    EventName = StringField('Please enter the event name', validators=[DataRequired()])
    text = SelectField(u'Please enter product name', choices = ['Speaker', 'Mic'], validators=[DataRequired()])
    EventDay = DateTimeLocalField('Please enter date of event', format="%Y-%m-%dT%H:%M")
    amount = StringField('Please enter amount of specified product', validators=[DataRequired()])
    submit = SubmitField('Hire')

class ContactUsForm(FlaskForm):
    Name = StringField('Please enter your name', validators=[DataRequired()])
    PhoneNumber = StringField('Please enter your phone number', validators=[DataRequired(), Length(min=8, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    info = TextAreaField('Please add a message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit')