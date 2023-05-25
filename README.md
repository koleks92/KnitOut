# KnitOut

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

KnitOut is a web application developed as the CS50W Final Project. It serves as a social portal for knitters, allowing users to search, add, rate, and edit knitting recipes.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Distinctiveness and Complexity](#distinctiveness)

## Installation

To install the necessary requirements, run the following command:


Install requirements
```
pip install -r requirements.txt 

```

After installing the requirements, execute the following commands to set up the project:
```
python manage.py makemigrations
python manage.py migrate
```

Start the development server and click the link displayed in the terminal:
```
python manage.py runserver
```

## Technologies Used

**Backend:**
- Python
- JavaScript
- Django
- Git
- SQLite

**Frontend:**
- HTML
- JavaScript
- CSS
- Bootstrap

## Usage

**Navigation:**

In the top middle part, users can find the KnitOut logo, which always leads to the main page (index.html).
In the top left corner, there is an icon to open the navigation bar.
The navigation bar allows users to navigate to the following sections:
- Home (index.html)
- Recipes - By Difficulty
- Recipes - By Type
- Favorites (if logged in)
- Following (if logged in)
- Add New Recipe (if logged in)
- Log Out (if logged in)
- Log In
- Register
- Search

**Home:**

The Home page displays recently added recipes, and if logged in, recently added recipes by followed users. Each recipe is a link to the recipe page and shows the name, category, difficulty, image, and rating. If the recipe has already been rated by the user (requires the user to be logged in), it is indicated by a black thumbs-up/thumbs-down icon.

**Recipes - By Difficulty:**

This page allows users to choose the difficulty level of recipes (Beginner, Intermediate, Experienced, Expert/Grandma) and be redirected to the search results.

**Recipes - By Type:**

This page allows users to choose the type of recipes (Hats, Sweaters and Jumpers, Scarves, Blankets and Throws, Cardigans, Socks, Gloves, Toys, Other) and be redirected to the search results.

**Search:**

Users can search for recipes by entering a phrase and be redirected to the search results.

**Search Results:**

This page displays all recipes that match the user's query, showing a maximum of 10 recipes per page. If no matching recipes are found, an appropriate message is displayed.

**Favorites:**

This page shows users all their favorite recipes. Users must be logged in and have added recipes to their favorites.

**Following:**

This page displays recipes added by followed users. Users must be logged in and follow other users.

**Add New Recipe:**

Logged-in users can use this page to add a new recipe. Users must enter the name, category, number of steps, amount of yarn, image, and difficulty level. Afterward, the user will be redirected to the next page to add the steps.

**Add New Recipe - Steps:**

This page allows logged-in users to add the steps for a new recipe. The number of steps corresponds to the number provided on the "Add New Recipe" page. After providing all the steps, users can submit them. Once finished, users are redirected to the Recipe Page.

**Recipe Page:**

This page provides detailed information about a recipe, such as the name, category, difficulty, image, number of steps, creation date, author (with a link to the profile page), rating, and a link to view the recipe steps. If a user is logged in, they can add the recipe to their favorites.

**Recipe Steps:**

This page displays all the steps available for a recipe. Users can navigate using the "Previous" and "Next" buttons. If a logged-in user bookmarks a step, they will be taken directly to the bookmarked step on subsequent visits. Additionally, if a logged-in user is the creator of the recipe, they can edit the steps.

**Profile Page:**

This page allows users to view a selected user's profile. Users can see the name, number of followers, number of added recipes, date the user joined KnitOut, and all of the user's recipes. If a user is logged in, they can also choose to follow the displayed user.

**Log In, Log Out, Register:**

These pages allow users to log in, log out, or register a new account.

## Distinctiveness and Complexity
I believe that this project showcases the culmination of all the skills I have acquired from previous projects, allowing me to create something truly exceptional. One of my main objectives was to reduce reliance on Bootstrap libraries in order to focus on developing my own unique CSS/HTML style. As part of this effort, I went the extra mile to create custom APIs for various functionalities, including rating recipes, adding or removing ratings, managing bookmarks, and handling user following.

To enhance user experience, I implemented a custom JavaScript function that enables dynamic changes to the rating bar without the need for page reloading. Furthermore, my goal was to design a webpage/web application that specifically caters to the knitting community, considering their specific needs and preferences.

In terms of visual aesthetics, I aimed for an easy-to-view interface with intuitive navigation and pleasing color schemes. Leveraging CSS, I crafted my own distinctive website style, incorporating unique hover effects, personalized button designs, and customized logos.


## Contributing

If you are interested in contributing, please contact me on GitHub.

## License

This project is licensed under the [MIT License](LICENSE). Make sure to include a copy of the license file in your repository.

## Contact

- [GitHub](https://www.github.com/koleks92)
- [LinkedIn](https://www.linkedin.com/in/jan-konieczek-aa7827251/)
