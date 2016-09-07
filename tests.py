import unittest

from server import app
import server
from model import db, connect_to_db
from model import User, Box, RecipeBox, Recipe
from seed import example_recipes, example_user_boxes, load_users
from StringIO import StringIO
import json
import bcrypt
import webscrape_details

# class GeneralUserTests(unittest.TestCase):
#     """Tests routes for general user."""

#     def setUp(self):
#         self.client = app.test_client()
#         app.config['TESTING'] = True

#     def test_homepage(self):
#         """Tests homepage."""

#         result = self.client.get("/")

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("My Vegan Recipe Collector", result.data)
#         self.assertNotIn("Welcome", result.data)

#     def test_register(self):
#         """Tests new user registration page."""

#         result = self.client.get("/register")

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("or login here", result.data)
#         self.assertNotIn("Welcome", result.data)

#     def test_login(self):
#         """Tests login page."""

#         result = self.client.get("/login")

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("or create a new account", result.data)
#         self.assertNotIn("Welcome", result.data)


# class RegisteredUserTests(unittest.TestCase):
#     """Tests routes for logged-in user."""

#     def setUp(self):
#         self.client = app.test_client()
#         app.config["TESTING"] = True
#         app.config["SECRET_KEY"] = "key"

#         with self.client.session_transaction() as sess:
#             sess["user_id"] = 1
#             sess["username"] = "Ada"

#     def test_homepage(self):
#         """Tests homepage."""

#         result = self.client.get("/")

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("My Vegan Recipe Collector", result.data)
#         self.assertIn("Welcome, Ada", result.data)

#     def test_register(self):
#         """Tests new user registration page."""

#         result = self.client.get("/register", follow_redirects=True)

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("My Vegan Recipe Collector", result.data)
#         self.assertIn("Welcome, Ada", result.data)

#     def test_logout(self):
#         """Tests logout page."""

#         result = self.client.get("/logout", follow_redirects=True)

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("You are now logged out", result.data)
#         self.assertNotIn("Welcome", result.data)


# class RouteDatabaseTests(unittest.TestCase):
#     """Tests routes for general user using recipes in database."""

#     def setUp(self):
#         self.client = app.test_client()
#         app.config["TESTING"] = True
#         app.config["SECRET_KEY"] = "key"

#         connect_to_db(app, db_uri="postgresql:///testdb")

#         db.create_all()
#         example_recipes()

#     def tearDown(self):
#         db.session.close()
#         db.drop_all()

#     def test_search(self):
#         """Tests search form."""

#         result = self.client.get("/search")

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("Produce", result.data)
#         self.assertIn("Appetizer", result.data)
#         self.assertIn("medjool dates", result.data)
#         self.assertIn("Search By Maximum Time", result.data)

#     def test_results(self):
#         """Tests search results."""

#         test_cases = [
#             ("/results?time=&search-term=any", "ANY recipes", "Watermelon Sashimi", "recipes under"),
#             ("/results?time=&search-term=all", "ALL recipes", "Save Recipe", "recipes under"),
#             ("/results?ingredient=tahini&ingredient=vegan+chocolate+chips&ingredient=ground+cumin&course=Appetizer&course=Dessert&time=100&search-term=any", "under 100 min", "Save Recipe", "ALL recipes"),
#             ("/results?ingredient=cornstarch&ingredient=chickpeas&ingredient=pesto&ingredient=pinto+beans&ingredient=avocado&ingredient=fresh+parsley&time=&search-term=all", "No recipes found. Please try again.", "fresh parsley", "ANY recipes")
#         ]

#         for case in test_cases:
#             route, expected_result_1, expected_result_2, not_result = case[0], case[1], case[2], case[3]

#             result = self.client.get(route)

#             self.assertEqual(result.status_code, 200)
#             self.assertIn(expected_result_1, result.data)
#             self.assertIn(expected_result_2, result.data)
#             self.assertNotIn(not_result, result.data)

#     def test_recipe_details(self):
#         """Tests recipe details."""

#         result = self.client.get("/recipe/5")

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("Vegan Milky Way", result.data)
#         self.assertIn("pitted medjool dates", result.data)
#         self.assertIn("Dessert", result.data)
#         self.assertNotIn("Save Recipe", result.data)

#     def test_conversion(self):
#         """Tests ingredient conversions."""

#         pass


# class DatabaseLoginTests(unittest.TestCase):
#     """Tests routes for registration and login using users in database."""

#     def setUp(self):
#         self.client = app.test_client()
#         app.config["TESTING"] = True
#         app.config["SECRET_KEY"] = "key"

#         connect_to_db(app, db_uri="postgresql:///testdb")

#         db.create_all()

#         load_users(username="Ada", password="12345")

#     def tearDown(self):
#         db.session.close()
#         db.drop_all()

#     def test_register(self):
#         """Tests new user registration."""

#         test_cases = [
#             ({"username": "TestUser", "password": "testing"},
#              "or create a new account"),
#             ({"username": "Ada", "password": "testing"},
#              "Unavailable username")
#         ]

#         for case in test_cases:
#             input_data, expected_result = case[0], case[1]

#             result = self.client.post("/register",
#                                       data=input_data,
#                                       follow_redirects=True)

#             self.assertEqual(result.status_code, 200)
#             self.assertIn(expected_result, result.data)
#             self.assertNotIn("Welcome", result.data)

#     def test_register_success(self):
#         """Tests if new user registration adds user to database."""

#         self.client.post("/register",
#                          data={"username": "TestUser", "password": "testing"},
#                          follow_redirects=True)

#         newuser = User.query.filter(User.username == "TestUser").first()
#         self.assertEqual(newuser.username, "TestUser")
#         self.assertEqual(bcrypt.checkpw("testing", newuser.password.encode('utf-8')), True)

#     def test_login(self):
#         """Tests user login."""

#         test_cases = [
#             ({"username": "Bright", "password": "12345"},
#              "No such user exists"),
#             ({"username": "Ada", "password": "******"},
#              "Incorrect password"),
#             ({"username": "Ada", "password": "12345"},
#              "Welcome, Ada")
#         ]

#         for case in test_cases:
#             input_data, expected_result = case[0], case[1]

#             result = self.client.post("/login",
#                                       data=input_data,
#                                       follow_redirects=True)

#             self.assertEqual(result.status_code, 200)
#             self.assertIn(expected_result, result.data)


# class DatabaseUserTests(unittest.TestCase):
#     """Tests routes for logged-in user using database."""

#     def setUp(self):
#         self.client = app.test_client()
#         app.config["TESTING"] = True
#         app.config["SECRET_KEY"] = "key"

#         connect_to_db(app, db_uri="postgresql:///testdb")

#         db.create_all()

#         example_recipes()
#         example_user_boxes()

#         with self.client.session_transaction() as sess:
#             sess["user_id"] = 1
#             sess["username"] = "Ada"

#     def tearDown(self):
#         db.session.close()
#         db.drop_all()

#     def test_profile(self):
#         """Tests user profile page."""

#         result = self.client.get("/profile")

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("Sun-Dried Tomato Chickpea Burgers", result.data)
#         self.assertIn("Party Food", result.data)
#         self.assertIn("Make some substitutions", result.data)
#         self.assertIn("Change Username or Password", result.data)

#     def test_update_my_recipes(self):
#         """Tests update of user's saved recipes."""

#         test_cases = [
#             {"box_id": 1, "recipe_id": 2, "delete": "Y"},
#             {"box_id": 2, "recipe_id": -1, "delete": "N", "label_name": "Lunch Menu"},
#             {"box_id": 2, "recipe_id": 4, "delete": "N", "notes": "Added new recipe"}
#         ]

#         for case in test_cases:
#             result = self.client.post("/update_my_recipes",
#                                       data=case)

#             self.assertEqual(result.status_code, 200)
#             self.assertIn("Update successful", result.data)

#     def test_update_my_recipes_success(self):
#         """Tests if update of user's saved recipes updates database."""

#         test_cases = [
#             {"box_id": 1, "recipe_id": 2, "delete": "Y"},
#             {"box_id": 2, "recipe_id": -1, "delete": "N", "label_name": "Lunch Menu"},
#             {"box_id": 2, "recipe_id": 4, "delete": "N", "notes": "Added new recipe"}
#         ]

#         for case in test_cases:
#             self.client.post("/update_my_recipes",
#                              data=case)

#             box_id = case["box_id"]
#             recipe_id = case["recipe_id"]

#             if case["delete"] == "Y":
#                 recipebox = RecipeBox.query.filter_by(box_id=box_id, recipe_id=recipe_id).first()
#                 self.assertFalse(recipebox)
#             elif recipe_id != -1:
#                 notes = case["notes"]
#                 recipebox = RecipeBox.query.filter_by(box_id=box_id, recipe_id=recipe_id).first()
#                 self.assertEqual(recipebox.recipe_notes, notes)
#             else:
#                 label_name = case["label_name"]
#                 box = Box.query.filter_by(box_id=box_id).first()
#                 self.assertEqual(box.label_name, label_name)

#     def test_preview(self):
#         """Tests preview of user's saved recipes."""

#         result = self.client.get("/preview.html")

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("Sun-Dried Tomato Chickpea Burgers", result.data)
#         self.assertIn("My Notes:", result.data)
#         self.assertIn("Need to buy ingredients", result.data)

#     def test_upload(self):
#         """Tests profile picture upload."""

#         test_cases = [
#             ("test.txt", "data/test.txt", "Only the following formats allowed: .png, .jpg, .jpeg"),
#             ("test.png", "static/img/test.png", "Upload successful")
#         ]

#         for case in test_cases:
#             filename, filepath, expected_result = case[0], case[1], case[2]
#             with open(filepath) as test:
#                 imgStringIO = StringIO(test.read())

#             result = self.client.post("/upload",
#                                       data={"file": (imgStringIO, filename)},
#                                       follow_redirects=True)

#             self.assertEqual(result.status_code, 200)
#             self.assertIn(expected_result, result.data)

#     def test_upload_success(self):
#         """Tests if profile picture upload adds to, removes from database."""

#         test_cases = [
#             ("test.png", "static/img/test.png"),
#             ("test2.png", "static/img/test2.png")
#         ]

#         for case in test_cases:
#             filename, filepath = case[0], case[1]
#             with open(filepath) as test:
#                 imgStringIO = StringIO(test.read())

#             self.client.post("/upload",
#                              data={"file": (imgStringIO, filename)},
#                              follow_redirects=True)

#             user = User.query.filter(User.user_id == 1).first()
#             self.assertEqual(user.profile_img, filename)

#     def test_settings(self):
#         """Tests user settings functionality."""

#         test_cases = [
#             ({"username": "", "password": ""},
#              "No information to update"),
#             ({"username": "Ada2016", "password": ""},
#              "Your information has been updated"),
#             ({"username": "", "password": "ada.ada"},
#              "Your information has been updated"),
#             ({"username": "Ada16", "password": "adaadaada"},
#              "Your information has been updated")
#         ]

#         for case in test_cases:
#             input_data, expected_result = case[0], case[1]

#             result = self.client.post("/settings",
#                                       data=input_data,
#                                       follow_redirects=True)

#             self.assertEqual(result.status_code, 200)
#             self.assertIn(expected_result, result.data)

#     def test_settings_success(self):
#         """Tests if updated user settings updates data in database."""

#         test_cases = [
#             {"username": "Ada2016", "password": ""},
#             {"username": "", "password": "ada.ada"},
#             {"username": "Ada16", "password": "adaadaada"}
#         ]

#         for case in test_cases:
#             self.client.post("/settings",
#                              data=case,
#                              follow_redirects=True)

#             if case.get("username"):
#                 user = User.query.filter(User.user_id == 1).first()
#                 self.assertEqual(user.username, case["username"])

#             if case.get("password"):
#                 password = case["password"]
#                 self.assertTrue(bcrypt.checkpw(password, user.password.encode('utf-8')))

#     def test_recipe_details(self):
#         """Tests recipe details."""

#         result = self.client.get("/recipe/5")

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("Vegan Milky Way", result.data)
#         self.assertIn("pitted medjool dates", result.data)
#         self.assertIn("Dessert", result.data)
#         self.assertIn("Save Recipe", result.data)

#     def test_save_recipe(self):
#         """Tests save recipe form."""

#         result = self.client.get("/save_recipe/4")

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("Save Recipe", result.data)
#         self.assertIn("Choose Existing Label", result.data)
#         self.assertIn("Create New Label", result.data)
#         self.assertIn("Weekend Desserts", result.data)

#     def test_save_recipe_success(self):
#         """Tests if saving recipe adds recipe and label to database."""

#         test_cases = [
#             ({"box-label": "", "new-label": "", "recipe-id": 4},
#              "Choose an existing label or create a new label"),
#             ({"box-label": "Weekend Desserts", "new-label": "", "recipe-id": 4},
#              "This recipe already exists in the selected label category"),
#             ({"box-label": "Party Food", "new-label": "", "recipe-id": 4},
#              "CLICK ICONS TO EXPAND"),
#             ({"box-label": "", "new-label": "Easy Recipes", "recipe-id": 4},
#              "CLICK ICONS TO EXPAND"),
#             ({"box-label": "Party Food", "new-label": "Simple Recipes", "recipe-id": 4},
#              "Choose only one field")
#             ]

#         for case in test_cases:
#             input_data, expected_result = case[0], case[1]

#             result = self.client.post("/save_recipe",
#                                       data=input_data,
#                                       follow_redirects=True)

#             self.assertEqual(result.status_code, 200)
#             self.assertIn(expected_result, result.data)

#     def test_my_recipe(self):
#         """Tests saved recipe visualization page."""

#         result = self.client.get("/my_recipes")

#         self.assertEqual(result.status_code, 200)
#         self.assertIn("CLICK ICONS TO EXPAND", result.data)
#         self.assertIn("My Recipes", result.data)

#     def test_my_recipe_json(self):
#         """Tests if saved recipe visualization page uses data from database."""

#         result = self.client.get("/my_recipes.json")
#         data = json.loads(result.data)
#         label_data = data[1]
#         recipe_data = data[2]

#         self.assertEqual(result.status_code, 200)
#         self.assertEqual(label_data["name"], "Party Food")
#         self.assertEqual(recipe_data["name"], "Sun-Dried Tomato Chickpea Burgers")


# class ModelTests(unittest.TestCase):
#     """Tests model instantiations."""

#     def setUp(self):
#         self.client = app.test_client()
#         app.config["TESTING"] = True
#         app.config["SECRET_KEY"] = "key"

#         connect_to_db(app, db_uri="postgresql:///testdb")

#         db.create_all()

#     def tearDown(self):
#         db.session.close()
#         db.drop_all()

#     def test_User(self):
#         """Tests User model instantiation."""

#         add_user = User(username="TestUser", password="**password**")
#         db.session.add(add_user)

#         user = User.query.filter(User.username == "TestUser").first()

#         self.assertEqual(user.password, "**password**")
#         self.assertEqual(user.profile_img, None)
#         self.assertEqual(user.__repr__(), "<User user_id=1 username=TestUser>")

#     def test_Box(self):
#         """Tests Box model instantiation."""

#         add_user = User(username="TestUser", password="**password**")
#         db.session.add(add_user)

#         add_box = Box(user_id=1, label_name="To Try")
#         db.session.add(add_box)

#         box = Box.query.filter(Box.label_name == "To Try").first()

#         self.assertEqual(box.user_id, 1)
#         self.assertEqual(box.__repr__(), "<Box box_id=1 user_id=1>")


# class HelperFunctionsTests(unittest.TestCase):
#     """Tests helper functions that use database."""

#     def setUp(self):
#         self.client = app.test_client()
#         app.config["TESTING"] = True
#         app.config["SECRET_KEY"] = "key"

#         connect_to_db(app, db_uri="postgresql:///testdb")

#         db.create_all()

#     def tearDown(self):
#         db.session.close()
#         db.drop_all()

#     def test_conversion(self):
#         """Tests conversion function."""

#         recipe = Recipe.query.first()
#         pass


# class SeedDatabaseTests(unittest.TestCase):
#     """Tests single functions."""

#     def test_function(self):
#         pass


class WebScrapeTests(unittest.TestCase):
    """Tests single functions."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        def _mock_get_img_url(soup):
            return "http://cdn3.minimalistbaker.com/wp-content/uploads/2016/06/Cauliflower-Rice-Stuffed-Pepper-SQUARE.jpg"

        webscrape_details.get_img_url = _mock_get_img_url

    def test_img_url(self):
        """Tests if image url is returned from html."""

        soup = '<div>some html</div>'

        result = webscrape_details.get_img_url(soup)

        self.assertEqual(result, "http://cdn3.minimalistbaker.com/wp-content/uploads/2016/06/Cauliflower-Rice-Stuffed-Pepper-SQUARE.jpg")






###############################################################################

if __name__ == "__main__":

    unittest.main()

    # coverage run --source=model.py,seed.py,server.py,tests.py,webscrape_details.py tests.py helper_functions.py
