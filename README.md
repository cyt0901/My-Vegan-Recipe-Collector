
# My Vegan Recipe Collector
![My Vegan Recipe Collector](/static/img/Vegan_clipart.png)

### Project Motivation
The goal was to build an app that combined the process of looking for vegan recipes with the search and save features of general recipe-finder apps. Therefore, **My Vegan Recipe Collector** aims to simplify the search for vegan recipes.

First, the user does not have to filter the search results to accommodate for only the vegan diet. It allows users to perform filtered searches by ingredients, time, and course type (or any combination of the aforementioned) to find recipes' detailed list of ingredients and instructions. With an added conversion feature, users can convert the ingredient measurements to any serving size from 1 to 12. Furthermore, recipes can be saved by categeories using user-generated labels, which can be accessed and updated at a later time.

## Table of Contents
1. [Technologies Used](#technologies)
2. [Data Model](#model)
3. [Webscraping](#webscraping)
4. [Seeding Data](#seeding)
5. [Search Recipes](#search)
6. [Recipe Details](#recipe)
7. [Measurement Conversion](#conversion)
8. [User Features](#user)
9. [User Recipe Boxes](#boxes)
10. [Data Visualization](#d3)
11. [Testing](#testing)
12. [Extra Notes](#notes)
13. [Author](#author)

## <a name="technologies"></a>Technologies Used
* [Python](https://www.python.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [Flask](http://flask.pocoo.org/)
* [Flask - SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
* [Jinja2](http://jinja.pocoo.org/docs/dev/)
* [Bootstrap](http://getbootstrap.com/)
* JavaScript
* [jQuery](https://jquery.com/)
* [AJAX](https://developer.mozilla.org/en-US/docs/AJAX/Getting_Started)
* [d3](https://d3js.org/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
* [Spoonacular API](https://spoonacular.com/food-api)
#### Additional Resources
[![Minimalist Baker](/static/img/minimalist-baker.png)](http://minimalistbaker.com/)

## <a name="model"></a>Data Model
A large component of this app is its intricate relational data model. With 19 inter-related tables, user and recipe data is stored in the local PostgreSQL database.

![Data Model](/static/img/screenshot-model.png)

## <a name="webscraping"></a>Webscraping
Using the Spoonacular API, most information about the recipe is found, but some information, such as course type is not included. Thus, this information, which is available through webscraping, is extracted using Beautiful Soup.

After examining the data from the Spoonacular API, it was found that the list of ingredients provided was different than what was expected. To explain, although the ingredients list was provided by the API call, it was found that meta data was parsed from the ingredient string, thus, losing some components, including any links. Because data was lost in the process, the ingredients from the API call were not desirable data. Thus, webscraping was used to extract the original ingredient strings, including the links, from the website. 

Then, in order to use the scraped ingredient data, each ingredient string needed to be split by US measurements, metric measurements, and the ingredient description. On a further note, the measurements are optional pieces of the string, so many conditional statements were used to check the contents of each string. In order to extract the actual measurements from the string, Python's regular expression module was used to find and split up the string accordingly.

A function was created to abstract the process of extracting recipe data from both the Spoonacular API and the webscraping at one time. The function was built in a way to accept a URL string as an argument when it is called, which will prompt the API calls and the webscraping function.

## <a name="seeding"></a>Seeding Data
Once all the data has been acquired, it should be seeded to the PostgreSQL database. However, because the tables in the database are so heavily-related with so many foreign key dependencies, it proved to be quite a challenge to figure out the precise order the data must be seeded. 

Using models, Flask SQLAlchemy, and test cases, the data was successfully added to the  database when a URL is provided

## <a name="search"></a>Search Recipes
On the search page, the user may submit a form that lists out the filters that the user may search by. The user can search by ingredients, course type, and maximum time, and the search condition may be set to "any" or "all" terms selected.

![Search Recipes](/static/img/screenshot-search.png)

Once the form is submitted, the server processes the form and performs a database query depending on the search parameters selected. Again, conditional statements played a significant role in this feature as all the filters are optional.

The most interesting part about this section was figuring out how to meet the "any" or "all" condition the user has selected. In order to test if all terms are met, a counter dictionary was set up to determine if the length of the list of the selected ingredients(or courses) matches the count number of the recipe. If they do not match, the recipe is removed from the dictionary. This process, coupled with conditional statements, allows for the "any" or "all" condition to be met. 

Once the matching recipes are found, the recipe objects are passed to Jinja2, and a new template is rendered, displaying the results.

![Search Results](/static/img/screenshot-results.png)

## <a name="recipe"></a>Recipe Details
Next, the recipe details page contains data about the recipe.

![Recipe Details](/static/img/screenshot-recipe.png)

The page includes the recipe's list of ingredients as well as the instructions.

![More Recipe Details](/static/img/screenshot-recipe2.png)

## <a name="conversion"></a>Measurement Conversion
An important feature for any well-built recipe search app is if it has a conversion feature, so **My Vegan Recipe Collector** includes it on the recipe details page. Using an AJAX call, both the US and metric measurements for the ingredients are updated on the page once the user selects a new serving size.

#### Before the Conversion
![Measurement Conversion Before](/static/img/screenshot-convert-before.png)

#### After the Conversion
![Measurement Conversion After](/static/img/screenshot-convert-after.png)

## <a name="user"></a>User Features
Using Flask sessions and PostgreSQL database queries, the user's registration or login information is checked before adding or updating the database. Password hashing through bcrypt is used to store the hashed values of user passwords.

#### Registration
![Registration](/static/img/screenshot-register.png)

#### Login
![Login](/static/img/screenshot-login.png)

###### Updating Username and Password
A user can change the username and/or password through the profile page.

![Update Login](/static/img/screenshot-update-login.png)

###### Upload Profile Image
A user may upload a profile picture to the profile page. The image name is saved to the users table in the database and is then saved to an uploads folder on the server. If an image is already associated with the user, meaning the user is changing the profile picture, not only is the new image added to the database and the uploads folder, but the old image is removed from the uploads folder.

![Upload Profile Image](/static/img/screenshot-upload-profile.png)

## <a name="boxes"></a>User Recipe Boxes
A logged in user may choose to save recipes. By doing so, a new row is added to the PostgreSQL database. The user can create the label names for the recipe boxes (or categories) and customize them when needed through the profile page. Also, users may add recipe notes to also be stored in the database.

#### Saving a Recipe
![Save to Recipe Box](/static/img/screenshot-save.png)

#### Updating Recipe Boxes
A user may update any recipe box labels, delete recipes from certain boxes, and add or edit recipe notes through the user profile page. Making changes in the form will update the data in the PostgreSQL database to reflect the changes.

![Update Recipe Box](/static/img/screenshot-update-box.png)

## <a name="d3"></a>Data Visualization
In order to show the user's recipe boxes in a clearer and more interesting way, d3 was implemented to show the boxes and the recipes in each box using a d3 tree diagram. When the user clicks on a node, its children is displayed, thus making an interesting visualization.

![D3 Data Visualization](/static/img/screenshot-d3-tree.png)

## <a name="testing"></a>Testing
Some tests were written to test the integration and functionality of certain parts of the app. The components that were tested the most were the routes to check if the returned HTML was what was expected.

## <a name="notes"></a>Extra Notes
The pages were rendered using Jinja2 templating, and objects were passed from the server to the front-end in order to make attributes more readily accessible from the front-end. Because the tables in the database are so interwoven, accessing data through the defined relationships of the tables was challenging at times.

The Bootstrap framework was used to make the pages more responsive. As it comes with its own set of default styles for HTML elements, in order to override those styles, a closer inspection of the current DOM was necessary. Finding and locating inherited styles was a difficult at times.

## <a name="v2"></a>Version 2.0
* More testing, especially to test webscraping and conversion
* Refactoring code to include class methods
* Adding additional vegan websites to pull data from
* Automate database seeding to occur at regular time intervals
* Plus more!

## <a name="about"></a>Author
Iris Han is a software engineer currently residing in San Francisco, CA.
For more information, visit her [LinkedIn](https://www.linkedin.com/in/irisbhan) profile.