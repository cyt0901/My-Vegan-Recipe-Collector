"""Utility file to seed database with data from api and through webscraping"""

from model import Recipe, Serving, Course, Website, Measurement, Ingredient, Instruction, RecipeIngredient, IngredientMeasure, RecipeServing, RecipeCourse, User, IngredientType
from model import connect_to_db, db
from server import app
from webscrape_details import get_all_recipe_info
import unirest
import os
import re


def load_users(username, password):
    """Load sample users."""

    print "Users"

    user = User(username=username,
                password=password)

    db.session.add(user)
    db.session.commit()


def load_website(scrape_info):
    """Load website name."""

    print "Websites"

    site_name = scrape_info['site_name']

    # if the website does not already exist in database, add to database
    if not Website.query.filter_by(site_name=site_name).all():
        website = Website(site_name=site_name)

        db.session.add(website)

    db.session.commit()


def load_courses(scrape_info):
    """Load course(s) for the recipe."""

    print "Course(s)"

    courses = scrape_info['courses']

    for course_name in courses:
        # if the course does not already exist in database, add to database
        if not Course.query.filter_by(course_name=course_name).all():
            course = Course(course_name=course_name)

            db.session.add(course)

    db.session.commit()


def load_servings(api_info):
    """Load serving size(s) for the recipe."""

    print "Serving(s)"

    serving_size = int(api_info['servings'])

    if not Serving.query.filter_by(serving_size=serving_size).all():
        serving = Serving(serving_size=serving_size)

        db.session.add(serving)

    db.session.commit()


def load_ingredienttypes(api_info):
    """Load ingredient types for the recipe."""

    print "Ingredient Type(s)"

    all_ingredients = api_info['extendedIngredients']  # list of ingredients

    for ingredient in all_ingredients:
        type_name = ingredient['aisle']

        if not IngredientType.query.filter_by(type_name=type_name).all():
            ingredienttype = IngredientType(type_name=type_name)

            db.session.add(ingredienttype)

    db.session.commit()


def load_ingredients(api_info):
    """Load ingredients for the recipe."""

    print "Ingredient(s)"

    all_ingredients = api_info['extendedIngredients']  # list of ingredients

    for ingredient in all_ingredients:
        ingredient_name = ingredient['name']
        type_name = ingredient['aisle']

        if not Ingredient.query.filter_by(ingredient_name=ingredient_name).all():
            type_id = IngredientType.query.filter_by(type_name=type_name).first().type_id
            ingredient = Ingredient(ingredient_name=ingredient_name, type_id=type_id)

            db.session.add(ingredient)

    db.session.commit()


def load_measurements(api_info):
    """Load measurements for the recipe."""

    print "Measurement(s)"

    all_ingredients = api_info['extendedIngredients']  # list of ingredients

    for ingredient in all_ingredients:
        unit_of_measure = ingredient['unit']
        amount = ingredient['amount']

        if not Measurement.query.filter_by(unit_of_measure=unit_of_measure,
                                           amount=amount).all():
            measurement = Measurement(unit_of_measure=unit_of_measure,
                                      amount=amount)

            db.session.add(measurement)

    db.session.commit()


def load_recipes(api_info, scrape_info):
    """Load recipes into database."""

    print "Recipe"

    if not Recipe.query.filter_by(recipe_name=api_info['title']).all():
        recipe_name = api_info['title']
        recipe_api_id = api_info['id']
        time_in_min = int(api_info['readyInMinutes'])
        src_url = scrape_info['src_url']
        img_url = scrape_info['img_url']
        site_id = Website.query.filter_by(site_name=scrape_info['site_name']).first().site_id

        recipe = Recipe(recipe_name=recipe_name,
                        time_in_min=time_in_min,
                        recipe_api_id=recipe_api_id,
                        src_url=src_url,
                        img_url=img_url,
                        site_id=site_id)

        db.session.add(recipe)

    db.session.commit()


def load_recipe_ingredients(api_info):
    """Load recipeingredients into database."""

    print "Recipe Ingredients"

    all_ingredients = api_info['extendedIngredients']  # list all ingredients

    for ingredient in all_ingredients:
        ingredient_name = ingredient['name']
        ingredient_id = Ingredient.query.filter_by(ingredient_name=ingredient_name).first().ingredient_id
        recipe_id = Recipe.query.filter_by(recipe_name=api_info['title']).first().recipe_id
        original_string = ingredient['originalString']

        recipeingredient = RecipeIngredient(original_string=original_string,
                                            recipe_id=recipe_id,
                                            ingredient_id=ingredient_id)

        db.session.add(recipeingredient)

    db.session.commit()


def load_instructions(api_info, instruction_info):
    """Load instructions for the recipe."""

    print "Instruction(s)"

    recipe_name = api_info['title']

    for instruction in instruction_info:
        step_instruction = instruction['step']
        step_order = instruction['number']
        recipe_id = Recipe.query.filter_by(recipe_name=recipe_name).first().recipe_id

        step = Instruction(step_order=step_order,
                           step_instruction=step_instruction,
                           recipe_id=recipe_id)

        db.session.add(step)

    db.session.commit()


def load_ingredient_measures(api_info):
    """Load ingredientmeasures for recipe."""

    print "Ingredients Measurements"

    all_ingredients = api_info['extendedIngredients']  # list all ingredients

    for ingredient in all_ingredients:
        unit_of_measure = ingredient['unit']
        amount = ingredient['amount']

        ingredient_id = Ingredient.query.filter_by(ingredient_name=ingredient['name']).first().ingredient_id
        measure_id = Measurement.query.filter_by(unit_of_measure=unit_of_measure, amount=amount).first().measure_id

        ingredientmeasure = IngredientMeasure(ingredient_id=ingredient_id,
                                              measure_id=measure_id)
        db.session.add(ingredientmeasure)

    db.session.commit()


def load_recipe_servings(api_info):
    """Load recipeservings for recipe."""

    print "Recipe Servings"

    serving_id = Serving.query.filter_by(serving_size=int(api_info['servings'])).first().serving_id
    recipe_id = Recipe.query.filter_by(recipe_name=api_info['title']).first().recipe_id

    recipeserving = RecipeServing(serving_id=serving_id,
                                  recipe_id=recipe_id)

    db.session.add(recipeserving)

    db.session.commit()


def load_recipe_courses(api_info, scrape_info):
    """Load recipecourses for recipe."""

    print "Recipe Courses"

    courses = scrape_info['courses']
    recipe_id = Recipe.query.filter_by(recipe_name=api_info['title']).first().recipe_id

    for course_name in courses:
        course_id = Course.query.filter_by(course_name=course_name).first().course_id
        recipecourse = RecipeCourse(course_id=course_id,
                                    recipe_id=recipe_id)

        db.session.add(recipecourse)

    db.session.commit()


###############################################################################

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # test-case urls
    urls = ["http://minimalistbaker.com/sun-dried-tomato-chickpea-burgers/",
            "http://minimalistbaker.com/cauliflower-rice-stuffed-peppers/",
            "http://minimalistbaker.com/banana-split-smoothie/",
            "http://minimalistbaker.com/strawberry-rhubarb-crumble-bars-gf/",
            "http://minimalistbaker.com/no-bake-almond-butter-cup-bars/",
            "http://minimalistbaker.com/asian-quinoa-salad/"]

    for url in urls:

        #info from webscraping
        scrape_info = get_all_recipe_info(url)

        #general recipe info through api request
        url_recipe_name = filter(None, re.split(r'.*com\/', url))[0]

        response1 = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/extract?forceExtraction=false&url=http://minimalistbaker.com/%s" % url_recipe_name,
            headers={
                "X-Mashape-Key": os.environ['MASHAPE_KEY']
            }
        )

        api_info = response1.body
        recipe_api_id = api_info['id']

        #instructions for recipe through api request
        response2 = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/%s/analyzedInstructions?stepBreakdown=true" % recipe_api_id,
            headers={
                "X-Mashape-Key": os.environ['MASHAPE_KEY'],
                "Accept": "application/json"
            }
        )

        instruction_info = response2.body[0]['steps']

        load_website(scrape_info)
        load_courses(scrape_info)
        load_servings(api_info)
        load_ingredienttypes(api_info)
        load_ingredients(api_info)
        load_measurements(api_info)
        load_recipes(api_info, scrape_info)
        load_recipe_ingredients(api_info)
        load_instructions(api_info, instruction_info)
        load_ingredient_measures(api_info)
        load_recipe_servings(api_info)
        load_recipe_courses(api_info, scrape_info)

    # test-case users
    load_users('Ada', '12345')
    load_users('Grace', 'hbacad')
