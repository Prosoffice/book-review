import os
import csv

# Flask Dependencies
from flask import Flask, flash, redirect, render_template, session, url_for
from flask_session import Session

# Database Dependencies
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Utilities
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from helpers import login_required
from forms import *

app = Flask(__name__)

# Check for the database url
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL not set")

# Check for the api
if not os.getenv("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure flask session to use file system instead of signed cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SECRET_KEY"] = 'prosper-dino-uche-focus-wisdom-pascal-collins'

Session(app)

# Create the engine variable then use the engine variable to make a scoped session and store it in a variable db
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# csrf token and bootstrap
csrf = CSRFProtect(app)
Bootstrap(app)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Setting up app context for Interactive programming on Terminal
@app.shell_context_processor
def make_shell_context():
    return {'db': db}


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search_input = form.search.data.lower()

        try:
            result = db.execute("SELECT isbn, title, author, year FROM books WHERE LOWER(isbn) ILIKE :isbn OR LOWER(title) "
                                "ILIKE :title OR "
                                "LOWER(author) ILIKE :author OR year = :year",
                                {'isbn':  '%' + search_input + "%", 'title':  '%' + search_input + "%", 'author':  '%' + search_input + "%", 'year': search_input})
            if result.rowcount == 0:
                return "NO such book"
            return render_template("test.html", result=result)
        except ValueError:
            return render_template("error.html")

    return render_template("index.html", form=form)


@app.route("/<isbn>", methods=['GET', 'POST'])
@login_required
def book_detail(isbn):
    form = ReviewForm()
    if form.validate_on_submit():
        #Check if user have left a review before
        all_post_review_id = db.execute("SELECT user_id FROM reviews WHERE isbn = :isbn", {'isbn': isbn}).fetchall()
        current_user = session['user_id']

        user_present = db.execute("SELECT COUNT(*) FROM reviews WHERE user_id = :user_id AND isbn = :isbn" , {'user_id': current_user, 'isbn':isbn}).fetchone()
        user_present = user_present[0]
        print(user_present)
        if int(user_present) == 0:
            rating = form.rating.data
            feedback = form.feedback.data
            db.execute("INSERT INTO reviews(ratings, feedbacks, isbn, user_id) VALUES(:rating, :feedback, :isbn, "
                       ":user_id)", {'rating': rating, 'feedback': feedback, 'isbn': isbn, 'user_id': current_user})
            db.commit()
            return redirect(url_for("book_detail", isbn=isbn))
        else:
            return "Sorry, you can only submit one review per post."
    row = db.execute("SELECT title, author, year FROM books WHERE isbn = :isbn", {'isbn': isbn}).fetchone()
    reviews = db.execute("SELECT ratings, feedbacks FROM reviews")
    title = row[0]
    author = row[1]
    year = row[2]
    isbn = isbn
    return  render_template("book-detail.html", title=title, author=author, year=year, isbn=isbn, form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        password = form.password.data

        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users(full_name, email, password) VALUES (:full_name, :email, :password)",
                   {'full_name': full_name, 'email': email, 'password': password_hash})
        db.commit()
        flash("Successfully Registered")
        print(f"New Successful registration {full_name}")
        return redirect("/login")
    return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Confirm user credentials
        users = db.execute("SELECT id, email, password FROM users").fetchall()
        user_confirmed = False
        user_id = ""
        for user in users:
            if email in user.email and check_password_hash(user.password, password):
                user_confirmed = True
                user_id = user.id
                break

        if user_confirmed:
            session['user_id'] = user_id
            return redirect("/")

    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


if __name__ == '__main__':
    app.run()
