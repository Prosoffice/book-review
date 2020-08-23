import os
import csv

# Flask Dependencies
from flask import Flask, flash, redirect, render_template, session
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


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search_input = form.search.data
        all_books = db.execute("SELECT isbn, title, author FROM books")

    return render_template("index.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        password = form.password.data

        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO USERS(full_name, email, password) VALUES (:full_name, :email, :password)",
                   {'full_name': full_name, 'email': email, 'password':password_hash})
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
    app.run(debug=True)
