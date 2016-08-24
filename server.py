"""Vegan Recipes"""


from jinja2 import StrictUndefined

# from flask import Flask, render_template, redirect, request, flash, session
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy import update

from model import connect_to_db, db
from model import User, Recipe, Website, Serving, Ingredient, USMeasurement, MetricMeasurement, USAmount, MetricAmount, Instruction, Course, RecipeIngredient, IngredientType, RecipeServing, USIngredientMeasure, MetricIngredientMeasure, RecipeCourse, Box, RecipeBox

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

    if not session.get("user_id"):
        return render_template("register_form.html")

    # If a user is already logged in
    flash("You are already logged in")
    return redirect("/")


@app.route('/register', methods=['POST'])
def register_process():
    """Handle registration form."""

    if not session.get("user_id"):
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

    # If a user is already logged in
    flash("You are already logged in")
    return redirect("/")


@app.route('/login')
def login_form():
    """Show login form."""

    if not session.get("user_id"):
        return render_template("login_form.html")
    else:
        # If a user is already logged in
        flash("You are already logged in")
        return redirect("/")


@app.route('/login', methods=['POST'])
def login_process():
    """Login the user."""

    if not session.get("user_id"):
        # Get form variables
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        # Query database to see if username exists
        if not user:
            flash("No such user exists")
            return redirect("/login")

        # Query database to see if password is correct
        if user.password != password:
            flash("Incorrect password")
            return redirect("/login")

        # Add user to the session to be logged in
        session["user_id"] = user.user_id
        session["username"] = user.username

        flash("Logged in")
    else:
        flash("You are already logged in")

    return redirect("/profile")


@app.route('/logout')
def logout():
    """Log out the user."""

    if session.get("user_id"):
        # Remove user from the session to be logged out
        session.pop("user_id", None)
        session.pop("username", None)
        flash("You are now logged out")
        return redirect("/")


@app.route('/profile')
def show_profile():
    """Show user profile."""

    if session.get("user_id"):
        user = User.query.filter_by(user_id=session["user_id"]).first()
        boxes = Box.query.filter_by(user_id=session["user_id"]).all()

        label_recipes = {}

        for box in boxes:
            label_name = box.label_name
            label_recipes[label_name] = label_recipes.get(label_name, []) + box.recipes

        return render_template("profile.html",
                               user=user,
                               label_recipes=label_recipes)
    else:
        return redirect("/")


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

    search_parameters = filter(None, [search_term] + all_ingredients + all_courses + ["< " + max_time + " min"])

    # no other search values except for ANY or ALL search_term
    if len(search_parameters) == 2 and not max_time:
        find_recipes = Recipe.query.all()
        search_parameters = search_parameters[:-1]

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
    serving_range = range(1, 13)

    return render_template("recipe.html",
                           recipe=recipe,
                           serving_range=serving_range)


@app.route('/save_recipe/<int:recipe_id>')
def show_add_recipe(recipe_id):
    """Show form for user to save recipe to recipe box."""

    if session.get("user_id"):
        recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
        user_id = session['user_id']
        boxes = Box.query.filter_by(user_id=user_id).all()

        return render_template("add_to_box.html",
                               recipe=recipe,
                               boxes=boxes)


@app.route('/save_recipe', methods=["POST"])
def save_recipe_to_box():
    """Save the recipe to a user recipe box."""

    if session.get("user_id"):
        label_name = request.form.get("box_label")
        new_label_name = request.form.get("new_label")
        recipe_id = request.form.get("recipe-id")
        user_id = session['user_id']

        if label_name:
            box_id = Box.query.filter_by(user_id=user_id, label_name=label_name).first().box_id
        else:
            box = Box(user_id=user_id,
                      label_name=new_label_name)
            db.session.add(box)
            db.session.commit()

            box_id = Box.query.filter_by(user_id=user_id, label_name=new_label_name).first().box_id

        recipebox = RecipeBox(recipe_id=recipe_id,
                              box_id=box_id)
        db.session.add(recipebox)
        db.session.commit()

        return redirect("/my_recipes")


@app.route('/my_recipes')
def show_recipe_box():
    """Show the user recipe box and labels"""

    user_id = session['user_id']
    boxes = Box.query.filter_by(user_id=user_id).all()

    label_recipes = {}

    for box in boxes:
        label_name = box.label_name
        label_recipes[label_name] = label_recipes.get(label_name, []) + box.recipes

    return render_template("my_recipes.html",
                           label_recipes=label_recipes)


@app.route('/settings', methods=["POST"])
def update_settings():
    """Update database with new values from user."""

    if session.get("user_id"):
        # Get form variables
        username = request.form.get("username")
        password = request.form.get("password")

        user_id = session["user_id"]

        user = User.query.filter_by(user_id=user_id).first()

        user.username = username
        user.password = password

        db.session.add(user)
        db.session.commit()

        flash("Your information has been updated")
        return redirect("/profile")


@app.route('/convert.json')
def convert_serving():
    """Return conversions of serving size."""

    new_serving = int(request.args.get("serving"))
    recipe_name = request.args.get("recipe_name")

    #query database for recipe
    recipe = Recipe.query.filter_by(recipe_name=recipe_name).first()
    orig_serving = recipe.servings[0].serving_size

    all_ings = recipe.recipesingredients
    # calculate conversion values for each ingredient
    for ingredient in recipe.recipesingredients:
        print ingredient

    print "\n\n\n"
    print "new_serving......   ", new_serving
    print "recipe_name.......   ", recipe_name
    print "recipe......   ", recipe
    print "orig_serving....   ", orig_serving
    print "all_ings.....   ", all_ings
    print "\n\n\n"


@app.route('/test')
def test_page():
    """To test data"""

    new_serving = int('6')

    recipe = Recipe.query.filter_by(recipe_id=1).first()
    orig_serving = recipe.servings[0].serving_size

    for ing in recipe.recipesingredients:
        print ing
        print ing.usamounts
        if ing.usamounts:
            for amount in ing.usamounts:
                print amount.us_amount



    print "-" * 50
    print "\n\n\n"
    print "new_serving:::::: ", new_serving
    print "recipe::::::  ", recipe
    print "orig_serving::::::   ", orig_serving
    print "\n\n\n"
    print "-" * 50

    return render_template("testpage.html",
                           new_serving=new_serving,
                           recipe=recipe,
                           orig_serving=orig_serving)


@app.route('/newtest')
def new_testpage():

    new_serving = int('6')
    recipe = Recipe.query.filter_by(recipe_id=1).first()
    orig_serving = recipe.servings[0].serving_size

    calculation = float(new_serving) / float(orig_serving)

    print "\n\n\n"

    print new_serving, "/", orig_serving
    print recipe
    print len(recipe.recipesingredients)
    for i in recipe.recipesingredients:
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print i.ingredients.ingredient_name
        for x in i.usamounts:
            print x.us_amount
            print x.us_decimal
            print ">>>>>", float(x.us_decimal) * calculation
            print "++++++++++++++++++"
        for y in i.metricamounts:
            print y.metric_amount
            print ">>>>>>", float(y.metric_amount) * calculation

    print calculation

    print "Done-----------\n\n\n"




###############################################################################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
