"""Import all necessary files to run the program."""
from flask import Flask  # imports flask from downloaded flask library
from flask_sqlalchemy import SQLAlchemy  # imports SQLAlchemy from flask_sqlalchemy
from os import path  # imports path from os
from flask_login import LoginManager  # imports LoginManager from flask_login


db = SQLAlchemy()  # defines the database as SQLAlchemy
DB_NAME = "database.db"  # Makes database.db the database name


def create_app():  # Function that creates the app
    """Create the app and configure the database and secret key."""
    app = Flask(__name__)  # Creates an instance of flask application
    app.config['SECRET_KEY'] = "099B13E7A5306F040CCC4FF35C38B5CDD9ED1C66C82D17C31B9A6D58C8EBBB26"
    # configures the secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # configures the database
    db.init_app(app)
    # allows interactions between database and flask app

    from .views import views  # imports views from views folder
    from .auth import auth  # imports auth from auth folder

    app.register_blueprint(views, url_prefix="/")  # registers a blueprint for views
    app.register_blueprint(auth, url_prefix="/")  # registers a blueprint for auth

    from .models import User  # imports User from models folder

    create_database(app)  # creates the databse

    login_manager = LoginManager()  # handles user authentication, sessions and login data
    login_manager.login_view = "auth.login"  # makes user login to access certain routes
    login_manager.init_app(app)  # integrates flask login extension with flask application

    @login_manager.user_loader  # loads user data if it is stored in database
    def load_user(id):  # defines a function load_user(id)
        return User.query.get(int(id))  # queuries database to find id as an integer

    return app  # returns the app


def create_database(app):  # defines function create_databse(app)
    """Create the database."""
    if not path.exists('website/' + DB_NAME):  # checks if the databse exists
        with app.app_context():  # uses context manager to create database without issues
            db.create_all()  # creates database models
        print('Created Database!')  # prints a message if database is created
