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

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
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

    rec_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rec_name = db.Column(db.String(200), nullable=False)
    time_in_min = db.Column(db.Integer, nullable=False)
    src_url = db.Column(db.String(300), nullable=False)
    img_url = db.Column(db.String(300), nullable=False)
    author = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recipe rec_id=%s rec_name=%s author=%s>" % (self.rec_id,
                                                             self.rec_name,
                                                             self.author)

    #Define relationship boxes table
    boxes = db.relationship("Box",
                            secondary="recboxes",
                            backref=db.backref("recipes"))

    #Define relationship ingredients table
    ingredients = db.relationship("Ingredient",
                                  secondary="recings",
                                  backref=db.backref("recipes"))

    #Define relationship instructions table
    instructions = db.relationship("Instruction",
                                   backref=db.backref("recipes"))

    #Define relationship servings table
    servings = db.relationship("Serving",
                               secondary="recservs",
                               backref=db.backref("recipes"))

    #Define relationship courses table
    courses = db.relationship("Course",
                              secondary="reccourses",
                              backref=db.backref("recipes"))


class Box(db.Model):
    """User-Labeled Recipe Box."""

    __tablename__ = "boxes"

    box_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
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

    serv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    size = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Serving serv_id=%s size=%s>" % (self.serv_id,
                                                 self.size)


class Ingredient(db.Model):
    """Ingredient in recipes."""

    __tablename__ = "ingredients"

    ingred_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingred_name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ingredient ingr_id=%s ingr_name=%s>" % (self.ingred_id,
                                                         self.ingred_name)


class Measurement(db.Model):
    """Measurement in for ingredients in recipes."""

    __tablename__ = "measurements"

    measure_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    unit = db.Column(db.String(64), nullable=False)
    amount = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Measurement meas_id=%s unit=%s amt=%s>" % (self.measure_id,
                                                            self.unit,
                                                            self.amount)

    #Define relationship ingredients table
    ingredients = db.relationship("Ingredient",
                                  secondary="ingmeasures",
                                  backref=db.backref("measurements"))


class Instruction(db.Model):
    """Instruction for recipes."""

    __tablename__ = "instructions"

    inst_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rec_id = db.Column(db.Integer,
                       db.ForeignKey('recipes.rec_id'))
    order = db.Column(db.Integer, nullable=False)
    inst_steps = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Instruction inst_id=%s rec_id=%s order_no=%s>" % (self.inst_id,
                                                                   self.rec_id,
                                                                   self.order)


class Course(db.Model):
    """Course category for recipes."""

    __tablename__ = "courses"

    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Course course_id=%s course_name=%s>" % (self.course_id,
                                                         self.course_name)


class RecipeBox(db.Model):
    """User's  Recipe Box."""

    __tablename__ = "recboxes"

    recbox_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rec_id = db.Column(db.Integer,
                       db.ForeignKey('recipes.rec_id'))
    box_id = db.Column(db.Integer,
                       db.ForeignKey('boxes.box_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecBox rec_id=%s box_id=%s>" % (self.rec_id,
                                                 self.box_id)


class RecipeIngred(db.Model):
    """Connects Recipe with Ingredient."""

    __tablename__ = "recings"

    recing_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rec_id = db.Column(db.Integer,
                       db.ForeignKey('recipes.rec_id'))
    ingred_id = db.Column(db.Integer,
                          db.ForeignKey('ingredients.ingred_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecIngred rec_id=%s ingred_id=%s>" % (self.rec_id,
                                                       self.ingred_id)


class RecipeServing(db.Model):
    """Connects Recipe with Serving."""

    __tablename__ = "recservs"

    recserv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rec_id = db.Column(db.Integer,
                       db.ForeignKey('recipes.rec_id'))
    serv_id = db.Column(db.Integer,
                        db.ForeignKey('servings.serv_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecipeServ rec_id=%s serv_id=%s>" % (self.rec_id,
                                                      self.serv_id)


class IngredMeasure(db.Model):
    """Ingredient Measurement."""

    __tablename__ = "ingmeasures"

    ingmeasure_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingred_id = db.Column(db.Integer,
                          db.ForeignKey('ingredients.ingred_id'))
    measure_id = db.Column(db.Integer,
                           db.ForeignKey('measurements.measure_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<IngredMeasure ingred_id=%s measure_id=%s>" % (self.ingred_id,
                                                               self.measure_id)


class RecipeCourse(db.Model):
    """Recipe Course."""

    __tablename__ = "reccourses"

    reccourse_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rec_id = db.Column(db.Integer,
                       db.ForeignKey('recipes.rec_id'))
    course_id = db.Column(db.Integer,
                          db.ForeignKey('courses.course_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecipeCourse rec_id=%s course_id=%s>" % (self.rec_id,
                                                          self.course_id)



##############################################################################
# Helper functions
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipes'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testrecipes'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
