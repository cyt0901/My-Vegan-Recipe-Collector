"""Vegan Recipes"""


from jinja2 import StrictUndefined

# from flask import Flask, render_template, redirect, request, flash, session
from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

# from model import connect_to_db, db
from model import *

import json


app = Flask(__name__)

app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("home.html")


@app.route('/register-form')
def register_form():
    """Show registration form."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Handle registration form."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    if User.query.filter_by(username=username).one():
        flash("Unavailable username")
        return redirect('/registration')

    new_user = User(username=username, password=password)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/login')


@app.route('/login-form')
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Login the user."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).one()

    # Query database to see if username exists
    if not user:
        flash("No such user")
        return redirect("/login-form")

    # Query database to see if password is correct
    if user.password != password:
        flash("Incorrect password")
        return redirect("/login-form")

    # Add user to the session to be logged in
    session["user_id"] = user.user_id

    flash("Logged in.")
    return redirect('/profile')


@app.route('/logout')
def logout():
    """Log out the user."""

    # Remove user from the session to be logged out
    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/profile')
def show_profile():
    """Show user profile."""

    return render_template("profile.html")


@app.route('/search')
def show_search_form():
    """Show search form."""

    recipe_preview_info = json.loads(open("data/search.json"))
    print type(recipe_preview_info)

    print recipe_preview_info

    return render_template("search.html")


@app.route('/results', methods=["POST"])
def show_search_results():
    """Display the search results."""

    return render_template("results.html")


@app.route('/recipe/<int:recipe_id>')
def show_recipe(recipe_id):
    """Show detailed recipe page."""

    return render_template("recipe.html")


@app.route('/save_recipe', methods=["POST"])
def add_recipe_to_box():
    """Save the recipe to a user recipe box."""

    # Add to database

    return render_template("add_to_box.html")


# @app.route('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
