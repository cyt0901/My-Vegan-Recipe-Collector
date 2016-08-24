from urllib import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import re


def get_img_url(soup):
    """Return url string for recipe image."""

    # Find recipe's img url
    recipe_img = soup.find("div", class_="ERSTopRight").img["src"]

    return recipe_img


def get_header_info(soup):
    """Return dictionary of header info, which includes the website name,
    the recipe category, and the serving size."""

    header_info = {}

    src_name = soup.find("span", itemprop="author").string
    course = soup.find("span", itemprop="recipeCategory").string
    serving = soup.find("span", itemprop="recipeYield").string

    header_info['src_name'] = src_name

    if '-' in serving:
        servings = serving.split('-')
        for serving in servings:
            serving = serving.strip()
        header_info['servings'] = servings
    else:
        header_info['servings'] = [serving]

    if ',' in course:
        courses = course.split(', ')
        header_info['courses'] = courses
    else:
        header_info['courses'] = [course]

    return header_info


def get_ingredients(soup):
    """Return dictionary of measurements and ingredient name."""
    # Find list of ingredients
    ingredients = soup.find_all("li", class_="ingredient")

    ingredient_info = {}

    for n in range(len(ingredients)):
        # check to see if another html element inside ingredient
        # if so, length will be greater than 1
        link = ""
        if len(ingredients[n].contents) > 1:
            for i in range(len(ingredients[n].contents)):
                # to check if there is a link
                if ingredients[n].contents[i].name == 'a':
                    link = ingredients[n].a['href']
            ing = ingredients[n].get_text()

        # only has length of 1
        else:
            # if everything is inside an a tag
            if ingredients[n].a:
                ing = ingredients[n].a.get_text()
            # for everything else
            else:
                ing = ingredients[n].get_text()

        # start with all lowercase
        ing = ing.lower()
        metric_amount = []
        metrics_measures = {}
        # search individual ingredient string to see if metric measurement is in it
        # if not, leave string as is; if it does, save metric values
        if re.search(r'\(\d.*?\)|\(~\d.*?\)', ing):
            # remove metric measurement from string, and return new string
            ing = filter(None, re.split(r'(\(\d.*?\))|(\(~\d.*?\))', ing))
            m = filter(None, re.split(r'\W', ing.pop(1)))
            ing = ' '.join(ing)

            if len(m) == 2:
                metric_amount.append(int(m[0]))
                metric_unit = m[1]
            elif len(m) == 3:
                metric_amount.append(int(m[0]))
                metric_amount.append(int(m[1]))
                metric_unit = m[2]
            elif len(m) == 4:
                metric_amount.append(int(m[2]))
                metric_unit = m[3]

            # add metric measurements to dictionary
            metrics_measures = dict(zip(['metric_unit', 'metric_amount'], [metric_unit, metric_amount]))

        # check if string has any other ()
        # if so, replace with 'placeholder'
        placeholder_content = ""
        if re.search(r'\(.*\)', ing):
            placeholder_content = re.findall(r'\(.*\)', ing)[0]
            ing = re.sub(r'\(.*\)', 'placeholder', ing)
            # ing = ' '.join(filter(None, re.split(r'\(.*\)', ing)))

        # check if string begins with 'optional: ', remove it, and move to end of string
        if ing.startswith('optional: '):
            ing = filter(None, re.split(r'\D*\s*:', ing))[0].strip() + " (optional)"

        """NEED TO COMPARE AGAINST LIST OF COMMON MEASURING UNITS TO SEPARATE
        THE UNITS FROM THE INGREDIENTS"""
        # list of units to compare with
        units = ['pinch', 'tbsp', 'tsp', 'cup', '-ounce can', 'clove', 'head', 'dash']
        removed_words = ['small', 'medium', 'large', 'heaping', 'scant']
        # remove unwanted words
        for word in removed_words:
            if word in ing:
                if "medium-large" in ing:
                    edge_case = "medium-large"
                    ing = ''.join(filter(None, re.split(r'%s' % edge_case, ing)))
                else:
                    ing = ''.join(filter(None, re.split(r'%s' % word, ing)))

        # to make sure whitespaces are consistent
        ing = ' '. join(filter(None, ing.split()))

        # to separate the unit name from the ingredient description
        # the ingredient is in ing
        for unit in units:
            if unit in ing:
                if unit is "-ounce can":
                    ing = filter(None, re.split(r'(\d*%s\s)' % unit, ing))
                elif (unit + 's') not in ing:
                    ing = filter(None, re.split(r'(%s)' % unit, ing))
                else:
                    ing = filter(None, re.split(r'(%s)' % (unit + 's'), ing))

        if type(ing) == list and len(ing) == 3:
            # check if ing[0] is a range; if so, split the numbers
            if "-" in ing[0]:
                ing[0] = filter(None, ing[0].split("-"))

        # make sure all ingredients are now lists
        if type(ing) != list:
            # check for fraction at beginning of string
            if ing[0].isdigit() and re.search(r'(.*?\/\d*)', ing):
                ing = filter(None, re.split(r'(.*?\/\d*)', ing))
            elif ing[0].isdigit() and not re.search(r'(.*?\/\d*)', ing):
                ing = filter(None, re.split(r'(\d+)', ing))
            else:
                ing = [ing]

        # replace placeholder_content
        if placeholder_content:
            ing[-1] = re.sub(r'placeholder', placeholder_content, ing[-1])

        # make sure all values in ing list have no leading/trailing whitespaces
        for i in range(len(ing)):
            # if item is list:
            if type(ing[i]) == list:
                for j in range(len(ing[i])):
                    ing[i][j] = ing[i][j].strip()
            else:
                ing[i] = ing[i].strip()

        # to add all us units and amounts to dictionary
        us_measures = {}
        if len(ing) == 3:
            stripped_ingredient = ing[2]
            if type(ing[0]) == list:
                us_measures = dict(zip(['us_unit', 'us_amount'], [ing[1], ing[0]]))
            else:
                us_measures = dict(zip(['us_unit', 'us_amount'], [ing[1], [ing[0]]]))
        elif len(ing) == 2:
            stripped_ingredient = ing[1]
            if ing[0][0].isdigit():
                if type(ing[0]) == list:
                    us_measures['us_amount'] = ing[0]
                else:
                    us_measures['us_amount'] = [ing[0]]
            else:
                us_measures['us_unit'] = ing[0]
        else:
            stripped_ingredient = ing[0]


        # # add all info to ingredient_info dictionary
        ingredient_info[n] = {}
        if metrics_measures:
            ingredient_info[n]['metrics_measures'] = metrics_measures
        if us_measures:
            ingredient_info[n]['us_measures'] = us_measures
        ingredient_info[n]['stripped_ingredient'] = stripped_ingredient
        # to add links to dictionary
        if link:
            ingredient_info[n]['link'] = link

    return ingredient_info


def get_all_recipe_info(url):
    """Return dictionary of all recipe information."""

    open_url = urlopen(url)
    read_url = open_url.read()

    # Specify a filter to parse html doc with. To be used as arg when using BeautifulSoup.
    only_recipe = SoupStrainer(class_="easyrecipe")

    # Parse only the recipe portion of webpage.
    soup = (BeautifulSoup(read_url, "html.parser", parse_only=only_recipe))

    all_info = {}

    all_info['src_url'] = url
    all_info['img_url'] = get_img_url(soup)
    all_info['site_name'] = get_header_info(soup)['src_name']
    all_info['courses'] = get_header_info(soup)['courses']
    all_info['ingredients'] = get_ingredients(soup)

    return all_info

