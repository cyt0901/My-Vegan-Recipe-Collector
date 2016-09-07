from fractions import Fraction
from model import Ingredient, Course, Recipe


def convert_us_amt(ingredient, conversion_amount):
    """Convert the fractional values of us measurements."""

    amounts = []

    for amount in ingredient.usamounts:
        new_decimal = float(amount.us_decimal) * conversion_amount
        whole_num = int(new_decimal)

        if whole_num == 0:
            new_fraction = str(Fraction(new_decimal).limit_denominator(32))
        elif (new_decimal - whole_num) == 0.0:
            new_fraction = str(whole_num)
        else:
            if Fraction(new_decimal - whole_num).limit_denominator(32) != 0:
                new_fraction = str(whole_num) + " " + str(Fraction(new_decimal - whole_num).limit_denominator(32))
            else:
                new_fraction = str(whole_num)

        amounts.append(new_fraction)

    if len(amounts) > 1:
        amounts = amounts[0] + " - " + amounts[1]
        if ingredient.usunits:
            amounts = amounts + " " + ingredient.usunits[0].us_unit
    else:
        amounts = amounts[0]
        if ingredient.usunits:
            amounts = amounts + " " + ingredient.usunits[0].us_unit

    return amounts


def convert_us_unit(conversion_amount):
    """Convert the us unit of measure, 'pinch'."""

    if conversion_amount < 0.5:
        amounts = "small smidgen"
    elif conversion_amount == 0.5:
        amounts = "smidgen"
    elif 0.5 < conversion_amount < 1.0:
        amounts = "small pinch"
    elif conversion_amount == 1.0:
        amounts = "pinch"
    elif conversion_amount > 1.0:
        amounts = str(int(round(conversion_amount))) + " pinches"

    return amounts


def convert_met_amt(ingredient, conversion_amount):
    """Convert the decimal values of metric measurements."""

    metrics = []
    metric_unit = ingredient.metricunits[0].metric_unit

    for amount in ingredient.metricamounts:
        new_metric = str("{0:.2f}".format(float(amount.metric_amount) * conversion_amount))

        metrics.append(new_metric)

    if len(metrics) > 1:
        metrics = "(" + metrics[0] + " - " + metrics[1] + " " + metric_unit + ")"
    else:
        metrics = "(" + metrics[0] + " " + metric_unit + ")"

    return metrics


def convert_ingredients(recipe, conversion_amount):
    """Return converted ingredient measurements."""

    all_ingredients = []

    for i in range(len(recipe.recipesingredients)):

        ingredient = recipe.recipesingredients[i]
        ingredient_info = {}

        if ingredient.usamounts:
            amounts = convert_us_amt(ingredient, conversion_amount)
            ingredient_info['us_amount'] = amounts
        elif ingredient.usunits and not ingredient.usamounts:
            amounts = convert_us_unit(conversion_amount)
            ingredient_info['us_amount'] = amounts

        if ingredient.metricamounts:
            metrics = convert_met_amt(ingredient, conversion_amount)
            ingredient_info['metric_amount'] = metrics

        ingredient_info['ingredient'] = ingredient.original_string

        if ingredient.link:
            ingredient_info['extlink'] = ingredient.link
        else:
            ingredient_info['extlink'] = None

        all_ingredients.append(ingredient_info)

    return all_ingredients


def get_my_recipes_data(boxes):
    """Return saved recipes, labels as list of dictionaries, for d3 visual."""

    data = [{"name": "My Recipes", "parent": None, "value": 6, "img": "/static/img/my_rec_icon.jpg"}]

    for box in boxes:
        each_box = dict(zip(["name", "parent", "value", "img"], [box.label_name, "My Recipes", 4, "/static/img/leaf0.png"]))
        data.append(each_box)
        for recipe in box.recipes:
            each_recipe = dict(zip(["name", "parent", "value", "img", "url"], [recipe.recipe_name, box.label_name, 3.5, recipe.img_url, "/recipe/" + str(recipe.recipe_id)]))
            data.append(each_recipe)

    return data


def match_ingredients(ingredients, search_term):
    """Return list of recipes taht match the list of ingredients given."""

    recipe_count = {}

    find_ingredients = Ingredient.query.filter(Ingredient.ingredient_name.in_(ingredients)).all()

    for ingredient in find_ingredients:
        find_recipes = ingredient.recipes
        for recipe in find_recipes:
            recipe_count[recipe] = recipe_count.get(recipe, 0) + 1

    if search_term == "all":
        for item, count in recipe_count.items():
            if count != len(ingredients):
                del recipe_count[item]

    return recipe_count.keys()


def match_courses(courses, search_term):
    """Return list of recipes that match the list of courses given."""

    find_courses = Course.query.filter(Course.course_name.in_(courses)).all()

    course_count = {}

    for course in find_courses:
        find_courses = course.recipes
        for recipe in find_courses:
            course_count[recipe] = course_count.get(recipe, 0) + 1

    if search_term == "all":
        for item, count in course_count.items():
            if count != len(courses):
                del course_count[item]

    return course_count.keys()


def match_time(time):
    """Return list of recipes that are under the maximum time given."""

    find_time = Recipe.query.filter(Recipe.time_in_min < int(time)).all()

    time_count = {}

    for recipe in find_time:
        time_count[recipe] = time_count.get(recipe, 0) + 1

    return time_count.keys()


def find_matching_recipes(search_term, ingredients, courses, time):
    """Return list of recipes that match the search parameters."""

    find_ingredients = set()
    find_courses = set()
    find_time = set()

    if not ingredients and not courses and not time:
        recipes = Recipe.query.all()

        return recipes

    if ingredients:
        find_ingredients = set(match_ingredients(ingredients, search_term))

    if courses:
        find_courses = set(match_courses(courses, search_term))

    if time:
        find_time = set(match_time(time))

    if search_term == "any":
        recipes = find_ingredients | find_courses | find_time
    else:
        recipes = find_ingredients & find_courses & find_time

    return recipes
