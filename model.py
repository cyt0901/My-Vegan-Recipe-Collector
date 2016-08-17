"""Models and database functions for Vegan Recipes project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################


# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s>" % (self.user_id,
                                                  self.username)

    #Define relationship boxes table
    boxes = db.relationship("Box",
                            backref=db.backref("users"))


class Recipe(db.Model):
    """Recipe on website."""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    recipe_api_id = db.Column(db.Integer, nullable=True)
    recipe_name = db.Column(db.String(200), nullable=False)
    time_in_min = db.Column(db.Integer, nullable=False)
    src_url = db.Column(db.String(300), nullable=False)
    img_url = db.Column(db.String(300), nullable=False)
    site_id = db.Column(db.Integer,
                        db.ForeignKey('websites.site_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recipe recipe_id=%s recipe_name=%s>" % (self.recipe_id,
                                                         self.recipe_name)

    #Define relationship boxes table
    boxes = db.relationship("Box",
                            secondary="recipesboxes",
                            backref=db.backref("recipes"))

    #Define relationship ingredients table
    ingredients = db.relationship("Ingredient",
                                  secondary="recipesingredients",
                                  backref=db.backref("recipes"))

    #Define relationship recipesingredients table
    recipesingredients = db.relationship("RecipeIngredient",
                                         backref=db.backref("recipes"))

    #Define relationship instructions table
    instructions = db.relationship("Instruction",
                                   backref=db.backref("recipes"))

    #Define relationship servings table
    servings = db.relationship("Serving",
                               secondary="recipesservings",
                               backref=db.backref("recipes"))

    #Define relationship courses table
    courses = db.relationship("Course",
                              secondary="recipescourses",
                              backref=db.backref("recipes"))

    #Define relationship websites table
    websites = db.relationship("Website",
                               backref=db.backref("recipes"))


class Website(db.Model):
    """Website where recipes scraped from."""

    __tablename__ = "websites"

    site_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    site_name = db.Column(db.String(200), unique=True, nullable=False)


class Box(db.Model):
    """User-Labeled Recipe Box."""

    __tablename__ = "boxes"

    box_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    label_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Box box_id=%s user_id=%s>" % (self.box_id,
                                               self.user_id)


class Serving(db.Model):
    """Servings for recipes."""

    __tablename__ = "servings"

    serving_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    serving_size = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Serving serving_id=%s serving_size=%s>" % (self.serving_id,
                                                            self.serving_size)


class Ingredient(db.Model):
    """Ingredient in recipes."""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    ingredient_name = db.Column(db.Text,
                                unique=True,
                                nullable=False)
    type_id = db.Column(db.Integer,
                        db.ForeignKey('ingredienttypes.type_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ingredient ingredient_id=%s ingredient_name=%s>" % (
                                                        self.ingredient_id,
                                                        self.ingredient_name)

    #Define relationship websites table
    ingredienttypes = db.relationship("IngredientType",
                                      backref=db.backref("ingredients"))


class Measurement(db.Model):
    """Measurement in for ingredients in recipes."""

    __tablename__ = "measurements"

    measure_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    unit_of_measure = db.Column(db.String(64), nullable=False)
    amount = db.Column(db.Numeric(6, 2), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Measurement measure_id=%s unit_of_measure=%s amt=%s>" % (
                                                        self.measure_id,
                                                        self.unit_of_measure,
                                                        self.amount)

    #Define relationship ingredients table
    ingredients = db.relationship("Ingredient",
                                  secondary="ingredientsmeasures",
                                  backref=db.backref("measurements"))


class Instruction(db.Model):
    """Instruction for recipes."""

    __tablename__ = "instructions"

    instruction_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipes.recipe_id'))
    step_order = db.Column(db.Integer, nullable=False)
    step_instruction = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Instruction instruction_id=%s recipe_id=%s step_order=%s>" % (
                                                        self.instruction_id,
                                                        self.recipe_id,
                                                        self.step_order)


class Course(db.Model):
    """Course category for recipes."""

    __tablename__ = "courses"

    course_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Course course_id=%s course_name=%s>" % (self.course_id,
                                                         self.course_name)


class RecipeBox(db.Model):
    """User's  Recipe Box."""

    __tablename__ = "recipesboxes"

    recipebox_id = db.Column(db.Integer,
                             autoincrement=True,
                             primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipes.recipe_id'))
    box_id = db.Column(db.Integer,
                       db.ForeignKey('boxes.box_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecipeBox recipe_id=%s box_id=%s>" % (self.recipe_id,
                                                       self.box_id)


class RecipeIngredient(db.Model):
    """Connects Recipe with Ingredient."""

    __tablename__ = "recipesingredients"

    recipeingredient_id = db.Column(db.Integer,
                                    autoincrement=True,
                                    primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipes.recipe_id'))
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey('ingredients.ingredient_id'))

    original_string = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecipeIngredient recipe_id=%s ingredient_id=%s>" % (
                                                            self.recipe_id,
                                                            self.ingredient_id)


class IngredientType(db.Model):
    """Type of Ingredient."""

    __tablename__ = "ingredienttypes"

    type_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    type_name = db.Column(db.String(100),
                          unique=True,
                          nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<IngredientType type_id=%s type_name=%s>" % (self.type_id,
                                                             self.type_name)


class RecipeServing(db.Model):
    """Connects Recipe with Serving."""

    __tablename__ = "recipesservings"

    recipeserving_id = db.Column(db.Integer,
                                 autoincrement=True,
                                 primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipes.recipe_id'))
    serving_id = db.Column(db.Integer,
                           db.ForeignKey('servings.serving_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecipeServing recipe_id=%s serving_id=%s>" % (self.recipe_id,
                                                               self.serving_id)


class IngredientMeasure(db.Model):
    """Ingredient Measurement."""

    __tablename__ = "ingredientsmeasures"

    ingredientmeasure_id = db.Column(db.Integer,
                                     autoincrement=True,
                                     primary_key=True)
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey('ingredients.ingredient_id'))
    measure_id = db.Column(db.Integer,
                           db.ForeignKey('measurements.measure_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<IngredMeasure ingred_id=%s measure_id=%s>" % (
                                                            self.ingredient_id,
                                                            self.measure_id)


class RecipeCourse(db.Model):
    """Recipe Course."""

    __tablename__ = "recipescourses"

    recipecourse_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipes.recipe_id'))
    course_id = db.Column(db.Integer,
                          db.ForeignKey('courses.course_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecipeCourse recipe_id=%s course_id=%s>" % (self.recipe_id,
                                                             self.course_id)


##############################################################################
# Helper functions
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipes'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testrecipes'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testing'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
