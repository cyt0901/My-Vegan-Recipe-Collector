"""Vegan Recipes"""


from jinja2 import StrictUndefined

# from flask import Flask, render_template, redirect, request, flash, session
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension

# from sqlalchemy import func, distinct

from model import connect_to_db, db
from model import Recipe, Serving, Course, Website, Measurement, Ingredient, Instruction, RecipeIngredient, IngredientMeasure, RecipeServing, RecipeCourse, User, IngredientType

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


@app.route('/register')
def register_form():
    """Show registration form."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Handle registration form."""

    # Get form variables
    username = request.form.get("username")
    password = request.form.get("password")

    # Check database to see if username is available for use
    if User.query.filter_by(username=username).all():
        flash("Unavailable username")
        return redirect("/register")

    # Add new user to database
    new_user = User(username=username, password=password)
    db.session.add(new_user)

    db.session.commit()

    return redirect("/login")


@app.route('/login')
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Login the user."""

    # Get form variables
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    # Query database to see if username exists
    if not user:
        flash("No such user")
        return redirect("/login")

    # Query database to see if password is correct
    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    # Add user to the session to be logged in
    session["user_id"] = user.user_id
    flash("Logged in.")
    return redirect("/profile")


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

    all_courses = Course.query.all()
    all_types = IngredientType.query.order_by(IngredientType.type_name).all()

    return render_template("search.html",
                           all_types=all_types,
                           all_courses=all_courses)


@app.route('/results')
def show_search_results():
    """Display the search results."""

    all_ingredients = request.args.getlist("ingredient")
    all_courses = request.args.getlist("course")
    max_time = request.args.get("time")
    search_term = request.args.get("search-term")

    search_parameters = filter(None, all_ingredients + all_courses + [max_time] + [search_term])

    recipe_count = {}
    # MATCH INGREDIENTS
    if all_ingredients:
        find_ingredients = Ingredient.query.filter(Ingredient.ingredient_name.in_(all_ingredients)).all()

        for ingredient in find_ingredients:
            # for ANY ingredients
            find_recipes = ingredient.recipes
            # create a counter with a dictionary
            for recipe in find_recipes:
                recipe_count[recipe] = recipe_count.get(recipe, 0) + 1

        # for ALL ingredients
        if search_term == "all":
            for item, count in recipe_count.items():
                # if the count does not match the length of the ingredients chosen, remove that key/value pair from the dictionary
                if count != len(all_ingredients):
                    del recipe_count[item]

        # list of all recipe objects for ANY or ALL ingredients
        find_recipes = recipe_count.keys()

    # MATCH COURSES
    if all_courses:
        find_courses = Course.query.filter(Course.course_name.in_(all_courses)).all()

        course_count = {}

        for course in find_courses:
            find_courses = course.recipes
            for recipe in find_courses:
                if recipe_count.get(recipe):
                    course_count[recipe] = course_count.get(recipe, 0) + 1

        # for ALL courses
        if search_term == "all":
            for item, count in course_count.items():
                if count != len(all_courses):
                    del course_count[item]

            find_recipes = course_count.keys()

        # for ANY courses
        else:
            for item, count in course_count.items():
                recipe_count[item] = recipe_count.get(item, 0) + 1
            find_recipes = recipe_count.keys()

    # MATCH TIME
    if max_time:
        find_time = Recipe.query.filter(Recipe.time_in_min < max_time).all()

        for recipe in find_time:
            recipe_count[recipe] = recipe_count.get(recipe, 0) + 1

        find_recipes = recipe_count.keys()

    return render_template("results.html",
                           find_recipes=find_recipes,
                           search_parameters=search_parameters)


@app.route('/recipe/<int:recipe_id>')
def show_recipe(recipe_id):
    """Show detailed recipe page."""

    recipe = Recipe.query.get(recipe_id)

    return render_template("recipe.html", recipe=recipe)


@app.route('/save_recipe', methods=["POST"])
def add_recipe_to_box():
    """Save the recipe to a user recipe box."""

    # Add to database

    return render_template("add_to_box.html")


###############################################################################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
