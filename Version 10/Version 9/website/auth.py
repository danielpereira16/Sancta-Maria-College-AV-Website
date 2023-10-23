"""Import all neccessary features and functions."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
# imports features from downloaded flask library
from . import db  # imports db from the directory
from .models import User  # imports User from models folder
from flask_login import login_user, logout_user, login_required, current_user
# imports features from flask_login
from werkzeug.security import generate_password_hash, check_password_hash
# imports password security features from werkzeug.security library
from .forms import RegistrationForm  # imports RegistrationForm from forms folder


auth = Blueprint("auth", __name__)  # defining blueprint called auth that associates with current module


@auth.route("/login", methods=['GET', 'POST'])  # creates route for the login page specifies methods for the page
def login():  # defines login function
    """Get email and password from user through forms.

    Log them in if email and password are in the databse.

    Return url to bring them to home.html.
    """
    if request.method == 'POST':  # checks that the request is a POST request
        email = request.form.get("email")  # requests users email through a form
        password = request.form.get("password")  # requests users password through a form

        user = User.query.filter_by(email=email).first()
        # checks database for 1st user that matches entered email
        if user:
            if check_password_hash(user.password, password):
                # checks if users password matches hashed password in database
                flash("Logged in!", category='success')  # flashes a message
                login_user(user, remember=True)  # logs the user in
                return redirect(url_for('views.home'))  # brings user to the home page
            else:
                flash('Password is incorrect.', category='error')  # flashses an error message
        else:
            flash('Email does not exist.', category='error')  # flasges an error message

    return render_template("login.html", user=current_user)  # renders the login page for the current user


@auth.route("/sign_up", methods=['GET', 'POST'])  # creates a route for the signup page
def sign_up():  # defines a function for signing up
    """Get user to fill forms, save data from from into database."""
    if current_user.is_authenticated:  # checks if user already exists
        return redirect(url_for('home'))  # brings the user to the home page
    form = RegistrationForm()  # defines form as RegistrationForm
    if form.validate_on_submit():  # checks if the form data has been validated
        hashed_password = generate_password_hash(
            (form.password.data), method='sha256')
        # hashes the password using sha256
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        # defines the user's username, email as data submitted on form and password as the hashed password
        db.session.add(user)  # adds user session to databse
        db.session.commit()  # commits session to database
        flash('Your account has been created! You can now login', 'success')  # flashes a message
        return redirect(url_for('auth.login'))  # brings user to login page
    return render_template('signup.html', form=form, user=current_user)  # renders the sign up page template


@auth.route("/logout")  # creates a route for logging out
@login_required  # restricts this route for those who aren't logged in
def logout():  # defines a function for logging out
    """Log the user out and bring them to home page."""
    logout_user()  # logs out the user
    return redirect(url_for("views.home"))  # brings user to the home page
