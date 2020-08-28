# Capstone

Web Programming with Python and JavaScript
Final Project

The website I have create is a recipe sharing application.
Users can upload recipes of their own and can view the recipes others have created as well.
I have implemented search functionality that allows users to search either by names of recipes, or by ingredients.
Users are able to review recipes a single time rating it out of 5 stars along with a comment.
Users are able to edit their own recipes and reviews later on.
Users can follow other users on their profile page sort recipes by those they follow.

I believe my project is distinctive and complex as it builds upon multiple lectures throughout the class.
I explored new features that bootstrap has to offer. My project utilizes django with multiple models. 
I use these models to work with storing information such as image uploads.
I made sure to make the webpage mobile responsive.
Additionally, I implemented live updates to the page using multiple javascript fetch calls.

## index.html
This is the homepage of my website.
Here users are greeted with a food related funfact, the 3 newest recipes and a button that brings users to a random recipe.

## createrecipe.html
This page uses Django's Modelform to auto create a form-group that can be filled out and easily transferred into the database. 

## editrecipe.html
This page uses Django's Modelform to pre-populate its fields with the current recipe to be easily updated into the database.

## following.html
This page will display a listing of all recipes created by users you follow.

## login.html
This is the login page.

## profile.html
This page will display the users followers and following along with their average review score from all your recipes.
When displaying a profile of another user, a follow button will appear to follow that user.
Additionally, a list of all the user's recipes will be displayed.

## recipe.html
This page displays a chosen recipe along with its reviews. If a user has not yet reviewed that recipe, that will be allowed to write one. 

## register.html
This page allows for a new user to create an account.

## search.html
This is the search page allowing for a user to search for recipes either by name or by ingredient.

## layout.html
This page is extended on every html page and includes the navigation bar and links the css and javascript pages to all the website pages.

## views.py
This is where my python code directing and loading for each page is stored. 

## models.py
This file stores my 3 models being the user model where user information is stored, my review model, where user reviews are stored, and my recipe model where user recipes are stored.

## javascript.js
This file is where I write my fetch calls that allow for my webpages to be live updated without refreshing that page.
