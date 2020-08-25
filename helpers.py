import os

# API Dependencies
import requests

# Login_required Dependencies
from flask import redirect, session
from functools import wraps

KEY = os.getenv("API_KEY")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def get_data(isbn):
    try:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": KEY, "isbns": isbn})
        res.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:

        response = res.json()
        response = response.get('books')[0]
        return response
    except (KeyError, TypeError, ValueError, AttributeError):
        return None

