"""My Vegan Recipe Collector"""

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db
from model import User, Recipe, Course, IngredientType, Box, RecipeBox
from functions import get_my_recipes_data, convert_ingredients, find_matching_recipes
import json
import bcrypt
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = "ABC"

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("index.html")


@app.route('/register')
def register_form():
    """Show registration form."""

    if not session.get("user_id"):
        return render_template("register_form.html")

    return redirect("/")


@app.route('/register', methods=['POST'])
def register_process():
    """Handle registration form."""

    if not session.get("user_id"):
        username = request.form.get("username")
        password = bcrypt.hashpw(request.form.get("password").encode('utf-8'), bcrypt.gensalt())

        if User.query.filter_by(username=username).all():
            flash("Unavailable username")
            return redirect("/register")

        new_user = User(username=username, password=password)
        db.session.add(new_user)

        db.session.commit()

        return redirect("/login")


@app.route('/login')
def login_form():
    """Show login form."""

    if not session.get("user_id"):
        return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Login the user."""

    if not session.get("user_id"):
        username = request.form.get("username")
        password = request.form.get("password").encode('utf-8')

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("No such user exists")
            return redirect("/login")

        if not bcrypt.checkpw(password, user.password.encode('utf-8')):
            flash("Incorrect password")
            return redirect("/login")

        session["user_id"] = user.user_id
        session["username"] = user.username

        flash("Logged in")

    return redirect("/profile")


@app.route('/logout')
def logout():
    """Log out the user."""

    if session.get("user_id"):
        session.pop("user_id", None)
        session.pop("username", None)
        flash("You are now logged out")

        return redirect("/")


@app.route('/profile')
def show_profile():
    """Show user profile."""

    if session.get("user_id"):
        user = User.query.filter_by(user_id=session["user_id"]).first()
        boxes = user.boxes

        return render_template("profile.html",
                               user=user,
                               boxes=boxes)


@app.route('/upload', methods=['POST'])
def upload_img():
    """Upload a profile picture."""

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user = User.query.filter_by(user_id=session["user_id"]).first()

        if user.profile_img:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user.profile_img))

        user.profile_img = filename

        db.session.commit()

        flash("Upload successful.")
    else:
        flash("Only the following formats allowed: .png, .jpg, .jpeg")

    return redirect("/profile")


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

    matching_recipes = find_matching_recipes(search_term=search_term, ingredients=all_ingredients, courses=all_courses, time=max_time)

    if max_time:
        max_time = "under " + max_time + " min"
    else:
        max_time = " "

    return render_template("results.html",
                           matching_recipes=matching_recipes,
                           ingredients=all_ingredients,
                           courses=all_courses,
                           time=max_time,
                           search=search_term)


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

        return render_template("save_recipe.html",
                               recipe=recipe,
                               boxes=boxes)


@app.route('/save_recipe', methods=["POST"])
def save_recipe_to_box():
    """Save the recipe to a user recipe box."""

    if session.get("user_id"):
        label_name = request.form.get("box-label")
        new_label_name = request.form.get("new-label")
        notes = request.form.get("notes")
        recipe_id = request.form.get("recipe-id")
        user_id = session['user_id']

        if label_name and new_label_name:
            flash("Choose only one field.")
            return redirect("/save_recipe/" + str(recipe_id))
        elif label_name:
            box_id = Box.query.filter_by(user_id=user_id, label_name=label_name).first().box_id
        elif new_label_name:
            box = Box(user_id=user_id,
                      label_name=new_label_name)
            db.session.add(box)
            db.session.commit()

            box_id = Box.query.filter_by(user_id=user_id, label_name=new_label_name).first().box_id
        else:
            flash("Choose an existing label or create a new label.")
            return redirect("/save_recipe/" + str(recipe_id))

        if RecipeBox.query.filter_by(box_id=box_id, recipe_id=recipe_id).all():
            flash("This recipe already exists in the selected label category.")
            return redirect('/save_recipe/' + str(recipe_id))
        else:
            recipebox = RecipeBox(recipe_id=recipe_id,
                                  box_id=box_id,
                                  recipe_notes=notes)
            db.session.add(recipebox)
            db.session.commit()

            return redirect("/my_recipes")


@app.route('/my_recipes')
def show_recipe_box():
    """Show visualization of user recipe box with labels and recipes."""

    return render_template("my_recipes.html")


@app.route('/settings', methods=["POST"])
def update_settings():
    """Update database with new values from user."""

    if session.get("user_id"):
        username = request.form.get("username")
        password = request.form.get("password").encode('utf-8')

        user_id = session["user_id"]

        user = User.query.filter_by(user_id=user_id).first()

        if username or password:
            if username:
                user.username = username
            if password:
                user.password = bcrypt.hashpw(password, bcrypt.gensalt())

            db.session.commit()

            flash("Your information has been updated.")
        else:
            flash("No information to update.")

        session["username"] = user.username

        return redirect("/profile")


@app.route('/update_my_recipes', methods=["POST"])
def update_recipe_box():
    """Update database with new info for user's recipe boxes."""

    box_id = int(request.form.get("box_id"))
    recipe_id = int(request.form.get("recipe_id"))
    delete = request.form.get("delete")

    if delete == "Y":
        recipebox = RecipeBox.query.filter_by(box_id=box_id, recipe_id=recipe_id).first()
        db.session.delete(recipebox)
        db.session.commit()
    elif recipe_id != (-1):
        notes = request.form.get("notes")
        recipebox = RecipeBox.query.filter_by(box_id=box_id, recipe_id=recipe_id).first()
        recipebox.recipe_notes = notes
        db.session.commit()
    else:
        label_name = request.form.get("label_name")
        box = Box.query.filter_by(box_id=box_id).first()
        box.label_name = label_name
        db.session.commit()

    return "Update successful"


@app.route('/preview.html')
def update_preview():
    """Send updated preview of users recipe boxes to front-end."""

    user_id = session["user_id"]
    boxes = User.query.filter_by(user_id=user_id).first().boxes

    return render_template("preview.html",
                           boxes=boxes)


@app.route('/show_conversion.json')
def show_conversion():
    """Show conversion of all measurements."""

    new_serving = int(request.args.get("serving"))
    recipe_id = int(request.args.get("recipe_id"))

    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    orig_serving = recipe.servings[0].serving_size
    conversion_amount = float(new_serving) / orig_serving

    new_ingredients = convert_ingredients(recipe, conversion_amount)

    return json.dumps(new_ingredients)


@app.route('/my_recipes.json')
def get_my_recipes():
    """Returns json data for my_recipes"""

    user_id = session["user_id"]
    boxes = Box.query.filter_by(user_id=user_id).all()

    data = get_my_recipes_data(boxes)

    return json.dumps(data)


######### HELPER FUNCTIONS ####################################################

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

###############################################################################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
