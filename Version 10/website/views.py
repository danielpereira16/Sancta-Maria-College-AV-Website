"""Import all necessary files, features and functions."""
from flask import Blueprint, render_template, request
from flask import flash, redirect, url_for, jsonify, abort
# imports several features from flask library
from flask_login import login_required, current_user
# imports login_required and current_user from flask_login library
from .models import Post, User, Comment, Like, Hire, ContactUs
# imports Post, User, Comment, Like, Hire, ContactUs from models folder
from .forms import UpdateAccountForm, PostForm, HireForm, ContactUsForm
# imports UpdateAccountForm, PostForm, ContactUsForm and HireForm from forms folder
from . import db  # imports db from directory

views = Blueprint("views", __name__)  # defines a blueprint for views


@views.route("/")  # creates a route with / as URL path
@views.route("/home")  # creates a route with /home as URL path
def home():  # defines a function for home
    """Create a route for home.html."""
    posts = Post.query.all()  # queries the databse for all posts
    return render_template("home.html", user=current_user, posts=posts)
    # renders the home.html page


@views.route("/blog")  # creates a route with /blog as the URL path
@login_required  # restricts route for unauthenticated users
def blog():  # defines a function for blog
    """Create a route for blog.html."""
    page = request.args.get('page', 1, type=int)
    # request how many pages there are as an integer
    posts = Post.query.order_by(
        Post.date_created.desc()).paginate(page=page, per_page=4)
    # creates a new page every 5th post and orders them by date/time created
    return render_template("blog.html", user=current_user, posts=posts)
    # renders blog.html page

@views.route("/add_product")
def add_product():
    return render_template("add_product.html", user=current_user)

@views.route("/create-post", methods=['GET', 'POST'])
# creates a route with /create-post as URL path, specifies GET and POST as methods
@login_required  # restricts route for unauthorized users
def create_post():  # defines a function for creating posts
    """Create a route and function for creating posts."""
    form = PostForm()  # defines form as PostForm
    if form.validate_on_submit():  # validates the form
        title = form.title.data  # checks if title is equal to data in the title form
        text = form.text.data  # checks if text is equal to data in text form
        post = Post(title=title, text=text, author=current_user.id)
        # confirms title, text and author
        db.session.add(post)  # adds session to the database
        db.session.commit()  # commits the session to the database
        flash('Post Created!', category='success')  # flashes a success message
        return redirect(url_for('views.blog'))  # brings the user to blog page

    return render_template('create_post.html', form=form,  user=current_user)
    # renders the create post page


@views.route("/delete-post/<id>")  # creates a route with delete-post as URL path
@login_required  # restricts route for unauthorized users
def delete_post(id):  # defines a function for deleting posts
    """Create a route and function for deleting posts."""
    post = Post.query.filter_by(id=id).first()
    # queries Post database for the post id
    if not post:  # creates an if statement
        flash("Post does not exist.", category='error')  # flashes an error message
    elif post.author != current_user.id:  # checks if the post belongs to the user
        flash('You do not have permission to delete this post.',
              category='error')
        # flashes an error message
    else:
        db.session.delete(post)  # deletes session from database
        db.session.commit()  # commits session
        flash('Post deleted.', category='success')  # flashes success message

    return redirect(url_for('views.blog'))  # brings user to blog page


@views.route("/posts/<username>")  # creates a route for posts
@login_required  # restricts route for unauthorized users
def posts(username):  # defines a function for posts
    """Create a route for posts belonging to a user."""
    user = User.query.filter_by(username=username).first()
    # checks the User database if the username matches
    if not user:
        flash('No user with that username exists.', category='error')
        # flahses an error message
        return redirect(url_for('views.home'))  # brings user to home page

    posts = user.posts  # defines posts as the posts of a user
    return render_template("posts.html",
                           user=current_user, posts=posts, username=username)
    # renders the posts.html template


def not_blank(comment):
    valid = False  # defines valid as a false input
    while not valid:  # When not valid loop
        text = comment.strip()  # Remove leading and trailing whitspace
        if text !="":  # Test if text to whitespace
            return text  # Return text
        else:   # if valid input
            break  # Break loop


@views.route("/create-comment/<post_id>", methods=['POST'])
# creates a route for creating comments, specifies method as POST
@login_required  # restricts route for unauthorized users
def create_comment(post_id):  # defines a function for creating comments
    """Create route and function for commenting."""
    comment = request.form.get('text')
    # defines text as a request form that gets texts
    text = not_blank(comment)  # defines text as using not blank to ensure comment not empty
    if not text:
        flash('Comment cannot be empty.', category='error')
        # flashses an error message
    else:
        post = Post.query.filter_by(id=post_id)
        # queries the Post database for an id that matches post_id
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            # defines comment as Comment
            db.session.add(comment)  # adds the session into Comment database
            db.session.commit()  # commits the session into the database
        else:
            flash('Post does not exist.', category='error')  # flahses an error message

    return redirect(url_for('views.blog'))  # brings user to blog page


@views.route("/like-post/<post_id>", methods=['POST'])
@login_required  # restricts route for unauthorized users
def like(post_id):  # defines a function for liking posts
    """Create route and function for liking posts."""
    post = Post.query.filter_by(id=post_id).first()
    # defines post as the first id that matches the post id
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()
    # defines like by first authhor that matches current user id and post id that matches post id
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    # shows an error message
    elif like:
        db.session.delete(like)  # deletes like from database
        db.session.commit()  # commits session to database
    else:
        like = Like(author=current_user.id, post_id=post_id)
        # defines like as Like specifiying that the author is the current user and that post id is post id
        db.session.add(like)  # adds like to database
        db.session.commit()  # commits session to database

    return jsonify({"likes": len(post.likes),
                    "liked": current_user.id in map(lambda x:
                                                    x.author, post.likes)})
    # checks it the current user has liked the post

@views.route("/account", methods=['GET', 'POST'])
# creates a route with /account as URL path, specifies POST and GET as methods
@login_required  # restricts route for unauthorized users
def account():  # defines a function for updating account info
    """Create route and function for updating account information."""
    form = UpdateAccountForm()  # defines form as UpdateAccountForm
    if form.validate_on_submit():  # validates the form
        current_user.username = form.username.data
        # makes the users username the username in the form
        current_user.email = form.email.data
        # makes the users email the email in the form
        db.session.commit()  # commits session into database
        flash('Your account has been updated')  # flashes a success message
        return redirect(url_for('views.account'))  # brings user to account page
    elif request.method == 'GET':  # if the reuqest method is GET
        form.username.data = current_user.username
        # auto fills the form with the users username
        form.email.data = current_user.email
        # auto fills the form with the users email
    return render_template('account.html', user=current_user, form=form)
    # renders the account.html page

@views.route("/update-post/<id>", methods=['GET', 'POST'])
# creates a route for updating posts, specifiying GET and POST as the methods
@login_required  # restricts route for unauthorized users
def update_post(id):  # defines a function for updating posts
    """Create route and function for updating posts."""
    post = Post.query.filter_by(id=id).first()
    # defines post as the first id that matches id
    if post.author != current_user.id:
        abort(403)
    # if the post author does not match current user id then abort

    form = PostForm()  # defines form as PostForm
    if form.validate_on_submit():  # validates the form
        post.title = form.title.data  # makes the title of the post the data that was in the form field
        post.text = form.text.data  # makes the text in the post the data that was in form field
        db.session.commit()  # commits the session into the database
        flash('Post Updated!', category='success')  # flashes a success message
        page = request.args.get('page', 1, type=int)  # requests the number of pages as an integer
        posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
        # creates a new page every 5th post and orders them by date/time created
        return render_template("blog.html", user=current_user, posts=posts)
    # renders the blog.html page
    elif request.method == 'GET':  # if the request method is GET
        form.title.data = post.title  # autofills the title form field as the current title
        form.text.data = post.text  # autofills the text as the current text
        # saves the image file into profile_pics folder
    return render_template('update_post.html', form=form,
                           user=current_user, post=post)
    # renders the update_post page

@views.route("/hire", methods=['GET', 'POST'])
@login_required
def hire_product():
    """Create route and function for hiring products."""
    # Create a form instance for hiring a product
    form = HireForm()
    if form.validate_on_submit():
        # If the form is submitted and valid, create a 'Hire' object and save it to the database
        hire = Hire(
            text=form.text.data,
            amount=form.amount.data,
            EventDay=form.EventDay.data,
            EventName=form.EventName.data,
            author=current_user.id,
            email=current_user.email
        )
        db.session.add(hire)  # Add the hire record to the database
        db.session.commit()  # Commit the changes
        flash('Hire Products Complete', category='success')  # Show a success message
        return redirect(url_for('views.add_product'))  # Redirect to the 'add_product' view
    # Render the 'hiring_page.html' template with the form and the current user
    return render_template('hiring_page.html', form=form, user=current_user)
    # renders the hiring page

@views.route("/contact-us", methods=['GET', 'POST'])
def contact_us():
    """Create route and function for contact us forms and page."""
    # Create a form instance for contacting us
    form = ContactUsForm()
    if form.validate_on_submit():
        # If the form is submitted and valid, create a 'ContactUs' object and save it to the database
        contactus = ContactUs(
            Name=form.Name.data,
            PhoneNumber=form.PhoneNumber.data,
            email=form.email.data,
            info=form.info.data
        )
        db.session.add(contactus)  # Add the contactus record to the database
        db.session.commit()  # Commit the changes
        flash('Thanks for your message, we will be in touch shortly', category='success')  # Show a success message
        return redirect(url_for('views.home'))  # Redirect to the 'home' view
    # Render the 'contact_us.html' template with the form and the current user
    return render_template('contact_us.html', form=form, user=current_user)
    # renders the contact_us page

@views.route("/products")
def products():
    """Create route and function for accessing products page."""
    # Render the 'products.html' template with the current user
    return render_template("products.html", user=current_user)
    # renders the products page
