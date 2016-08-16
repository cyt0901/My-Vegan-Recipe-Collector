from urllib import urlopen
from bs4 import BeautifulSoup, SoupStrainer


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

    header_info['src_name'] = src_name

    if ',' in course:
        courses = course.split(', ')
        header_info['courses'] = courses
    else:
        header_info['courses'] = [course]

    return header_info


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

    return all_info
