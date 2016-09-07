"""Models and database functions for Vegan Recipes project."""

from flask_sqlalchemy import SQLAlchemy

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
    password = db.Column(db.String(200), nullable=False)
    profile_img = db.Column(db.String(200), nullable=True)

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

    #Define relationship boxes table
    recipesboxes = db.relationship("RecipeBox",
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

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Website site_id=%s site_name=%s>" % (self.site_id,
                                                      self.site_name)


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

    #Define relationship ingredienttypes table
    ingredienttypes = db.relationship("IngredientType",
                                      backref=db.backref("ingredients"))

    #Define relationship recipesingredients table
    recipesingredients = db.relationship("RecipeIngredient",
                                         backref=db.backref("ingredients"))


class USUnit(db.Model):
    """US unit for ingredients in recipes."""

    __tablename__ = "usunits"

    us_unit_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    us_unit = db.Column(db.String(20),
                        unique=True,
                        nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<USUnit us_unit_id=%s us_unit=%s>" % (self.us_unit_id,
                                                      self.us_unit)

    #Define relationship ingredients table
    recipesingredients = db.relationship("RecipeIngredient",
                                         secondary="usingredientsmeasures",
                                         backref=db.backref("usunits"))


class MetricUnit(db.Model):
    """Metric unit for ingredients in recipes."""

    __tablename__ = "metricunits"

    metric_unit_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    metric_unit = db.Column(db.String(20),
                            unique=True,
                            nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<MetricUnit metric_unit_id=%s metric_unit=%s>" % (
                                                        self.metric_unit_id,
                                                        self.metric_unit)

    #Define relationship ingredients table
    recipesingredients = db.relationship("RecipeIngredient",
                                         secondary="metricingredientsmeasures",
                                         backref=db.backref("metricunits"))


class USAmount(db.Model):
    """Conversion for ingredients in recipes."""

    __tablename__ = "usamounts"

    us_amount_id = db.Column(db.Integer,
                             autoincrement=True,
                             primary_key=True)
    us_amount = db.Column(db.String(64),
                          unique=True,
                          nullable=False)
    us_decimal = db.Column(db.Numeric(7, 2),
                           nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<USAmount us_amount_id=%s amount=%s decimal=%s>" % (
                                                        self.us_amount_id,
                                                        self.us_amount,
                                                        self.us_decimal)

    #Define relationship ingredients table
    recipesingredients = db.relationship("RecipeIngredient",
                                  secondary="usingredientsmeasures",
                                  backref=db.backref("usamounts"))


class MetricAmount(db.Model):
    """Conversion for ingredients in recipes."""

    __tablename__ = "metricamounts"

    metric_amount_id = db.Column(db.Integer,
                                 autoincrement=True,
                                 primary_key=True)
    metric_amount = db.Column(db.Numeric(7, 2),
                              unique=True,
                              nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<MetricAmount metric_amt_id=%s metric_amt=%s>" % (
                                                        self.metric_amount_id,
                                                        self.metric_amount)

    #Define relationship ingredients table
    recipesingredients = db.relationship("RecipeIngredient",
                                  secondary="metricingredientsmeasures",
                                  backref=db.backref("metricamounts"))


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
    recipe_notes = db.Column(db.String(600), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecipeBox recipe_id=%s box_id=%s>" % (self.recipe_id,
                                                       self.box_id)

    #Define relationship boxes table
    boxes = db.relationship("Box",
                            backref=db.backref("recipesboxes"))


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

    link = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecipeIngredient recipe_id=%s ingredient_id=%s>" % (
                                                            self.recipe_id,
                                                            self.ingredient_id)

    #Define relationship usingredientsmeasures table
    usingredientsmeasures = db.relationship("USIngredientMeasure",
                                            backref=db.backref("recipesingredients"))


class IngredientType(db.Model):
    """Type of Ingredient."""

    __tablename__ = "ingredienttypes"

    type_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    type_name = db.Column(db.String(100),
                          unique=True,
                          nullable=True)

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


class USIngredientMeasure(db.Model):
    """US Ingredient Measurement."""

    __tablename__ = "usingredientsmeasures"

    usingmeasure_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    recipeingredient_id = db.Column(db.Integer,
                                    db.ForeignKey('recipesingredients.recipeingredient_id'))
    us_unit_id = db.Column(db.Integer,
                           db.ForeignKey('usunits.us_unit_id'))
    us_amount_id = db.Column(db.Integer,
                             db.ForeignKey('usamounts.us_amount_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<USIngredMeasure usingmeasure_id=%s>" % (self.usingmeasure_id)


class MetricIngredientMeasure(db.Model):
    """Metric Ingredient Measurement."""

    __tablename__ = "metricingredientsmeasures"

    metringmeasure_id = db.Column(db.Integer,
                                  autoincrement=True,
                                  primary_key=True)
    recipeingredient_id = db.Column(db.Integer,
                                    db.ForeignKey('recipesingredients.recipeingredient_id'))
    metric_unit_id = db.Column(db.Integer,
                               db.ForeignKey('metricunits.metric_unit_id'))
    metric_amount_id = db.Column(db.Integer,
                                 db.ForeignKey('metricamounts.metric_amount_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<MetricIngredMeasure metringmeasure_id=%s>" % (self.metringmeasure_id)


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


#####   HELPER FUNCTIONS  ######################################################

def connect_to_db(app, db_uri='postgresql:///recipes'):
    """Connect the database to our Flask app."""

    ###### final database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipes'
    ###### test database, 70+ recipes
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testrecipes'
    ###### test database, 5 recipes
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testing'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)

################################################################################

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
