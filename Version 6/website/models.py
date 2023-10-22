"""Import necessary files and functions."""
from . import db  # imports db from the directory
from flask_login import UserMixin  # imports UserMixin from flask_login library
from sqlalchemy.sql import func  # imports func from sqlalchemy.sql


class User(db.Model, UserMixin):  # defines class as User and inherits from db.Model and UserMixin
    """Create database model for users."""

    id = db.Column(db.Integer, primary_key=True)
    # defines id as a database column and specifies it as an integer that is unique
    email = db.Column(db.String(150), unique=True)
    # defines email as a database column, specifies it as a string that has to be unique
    username = db.Column(db.String(150), unique=True)
    # defines email as a database column, specifies it as a string that has to be unique
    password = db.Column(db.String(150))
    # defines password as a database column that is a string with a maximum of 150 characters
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # defines date_created as a database column that stores the date and time a user was created
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    # defines post as a database relationship with the Post model, provides a backref to user
    # and passively deletes any posts made by the user if the user is ever deleted.
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    # defines post as a database relationship with the Comment model, provides a backref to user
    # and passively deletes any comments made by the user if the user is ever deleted.
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    # defines post as a database relationship with the Like model, provides a backref to user
    # and passively deletes any likes made by the user if the user is ever deleted.


class Post(db.Model):  # defines class as Post that inherits from db.Model
    """Create database model for posts."""

    id = db.Column(db.Integer, primary_key=True)
    # defines id as a database column and specifies it as an integer that is unique
    title = db.Column(db.String(100), nullable=False)
    # defines title as a database column that is a string that cannot be empty
    text = db.Column(db.Text, nullable=False)
    # defines text as a database column that is a text that cannot be empty
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # defines date_created as a database column that shows the date and time that a post is created
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    # defines author as a database column specifies it as an integer that cannot be empty
    # specifies the foreign key as the user id, if user delete cascade deletion will occur
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    # defines post as a database relationship with the Comment model, provides a backref to user
    # and passively deletes any comments made by the user if the post is ever deleted.
    likes = db.relationship('Like', backref='post', passive_deletes=True)
    # defines post as a database relationship with the Like model, provides a backref to user
    # and passively deletes any likes made by the user if the post is ever deleted.


class Comment(db.Model):  # defines class as Comment that inherits from db.Model
    """Create databse model for comments."""

    id = db.Column(db.Integer, primary_key=True)
    # defines id as a database column and specifies it as an integer that is unique
    text = db.Column(db.String(200), nullable=False)
    # defines text as a database column that is a text that cannot be empty
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # defines date_created as a database column that shows the date and time that a post is created
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    # defines author as a database column specifies it as an integer that cannot be empty
    # specifies the foreign key as the user id, if user is deleted cascade deletion will occur
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)
    # defines post_id as a database column specifies it as an integer that cannot be empty
    # specifies the foreign key as post.id, if user is deleted cascade deletion will occur


class Like(db.Model):  # defines class as Like that inherits from db.Model
    """Create database model for likes."""

    id = db.Column(db.Integer, primary_key=True)
    # defines id as a database column and specifies it as an integer that is unique
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # defines date_created as a database column that shows the date and time that a post is created
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    # defines author as a database column specifies it as an integer that cannot be empty
    # specifies the foreign key as the user id, if user is deleted cascade deletion will occur
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)
    # defines post_id as a database column specifies it as an integer that cannot be empty
    # specifies the foreign key as post.id, if user is deleted cascade deletion will occur
