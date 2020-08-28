from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django import forms
import random
from .models import *


# recipe form
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'directions', 'image']

    # to add classes for style to model form items.
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['ingredients'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['directions'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})


food_facts = ["Russia Only Classed Beer As Alcohol In 2011!",
              "The Most Stolen Food In The World Is Cheese!",
              "Bananas Are Berries, But Strawberries Aren't!",
              "Lobsters & Oysters Used To Be Working Class Food",
              "You Can Hear Rhubarb Grow!",
              "Large Groups Of Pistachios Can Spontaneously Combust!",
              "Fruit Stickers Are Edible!",
              "Healthy Foods Cost Up To 10x As Much As Junk Foods.",
              "You Can't Overcook Mushrooms!",
              "Black Pepper Was A Luxury In The Middle Ages",
              "A Quarter Of The World's Hazelnuts Are Used For Nutella!",
              "A Corned Beef Sandwich Made The Voyage To Space In 1965!",
              "Loud Music Makes You Drink More, And Faster!",
              "Without Flies, There Would No Chocolate",
              "The Upper Classes Used To Serve 'Surprise Pie'!",
              "The Number Of Hot Dogs Eaten On 4th July Could Stretch From Washington Dc To La 5 Times Over!"]


def index(request):
    fun_fact = random.choice(food_facts)
    recipes = Recipe.objects.all().order_by("-time")[:3]
    users = User.objects.all()
    all_recipes = Recipe.objects.all()
    rand_recipe = random.choice(all_recipes)
    return render(request, "cookbook/index.html", {
        "fun_fact": fun_fact,
        "recipes": recipes,
        "users": users,
        "rand_recipe": rand_recipe
    })


def profile(request, profile):
    user = User.objects.get(id=profile)
    recipes = user.recipes.all()
    recipe_count = recipes.count()
    # calculate average rating for all reviews and all recipes user has
    num = 0
    count = 0
    for recipe in recipes:
        recipe_num = 0
        recipe_count = 0
        for review in recipe.reviews.all():
            recipe_num = recipe_num + review.rating
            recipe_count = recipe_count + 1
        count = count + 1
        if recipe_count != 0:
            num = num + (recipe_num/recipe_count)
    
    if count == 0:
        avg_rating = "N/A no recipes yet."
    else:
        avg_rating = num/count
        avg_rating = round(avg_rating,2)
        if avg_rating == 0:
            avg_rating = "No reviews yet."
    curr_user = request.user
    follow = True
    unfollow = False
    if user == curr_user or str(curr_user) == "AnonymousUser":
        follow = False
    elif user in curr_user.following.all():
        unfollow = True
    
    return render(request, "cookbook/profile.html", {
        # don't pass in user because it clashes with user name already passed in.
        "user1": user,
        "curr_user": curr_user,
        "follow": follow,
        "unfollow": unfollow,
        "recipe_count": count,
        "avg_rating": avg_rating
    })


def recipe(request, recipe):
    recipe_obj = Recipe.objects.get(id=recipe)
    users = User.objects.all()
    curr_user = request.user
    if str(curr_user) != "AnonymousUser":

        curr_user = User.objects.get(username=curr_user)
        rev_list = recipe_obj.reviews.all().order_by("-time")
        can_review = True
        for rev in rev_list:
            if curr_user == rev.user:
                can_review = False
    else:
        curr_user = None
        can_review = False
        rev_list = recipe_obj.reviews.all().order_by("-time")

    if request.method == 'POST':
        text = request.POST["text"]
        rate = request.POST["rate"]
        review = Review.objects.create(user=curr_user, text=text, rating=rate)
        review.save()
        recipe_obj.reviews.add(review)
        rev_list = recipe_obj.reviews.all().order_by("-time")
        can_review = False
    return render(request, "cookbook/recipe.html", {
        "recipe_obj": recipe_obj,
        "users": users,
        "reviews": rev_list,
        "curr_user": curr_user,
        "can_review": can_review
    })


def editrecipe(request, recipe_id):
    if request.method == "POST":
        recipe = Recipe.objects.get(id=recipe_id)
        # instance needed when updating existing recipe
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
        return redirect("/cookbook/recipe/" + recipe_id)
    else:
        recipe = Recipe.objects.get(id=recipe_id)
        # instance needed when updating existing recipe
        form = RecipeForm(instance=recipe)
        return render(request, "cookbook/editrecipe.html", {
            "recipe": recipe,
            "form": form
        })


def editreview(request):
    review_id = request.POST['id']
    text = request.POST["text"]
    rate = request.POST["rate"]
    review = Review.objects.get(id=review_id)
    review.text = text
    review.rating = rate
    review.save()
    return HttpResponse("done")


def createrecipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            recipe_name = form.cleaned_data['name']
            recipe = Recipe.objects.get(name=recipe_name)
            recipe_id = recipe.id
            curr_user = request.user
            user = User.objects.get(username=curr_user)
            user.recipes.add(recipe)
            return redirect('recipe', recipe=recipe_id)
    else:
        form = RecipeForm()
    return render(request, 'cookbook/createrecipe.html', {'form': form})


def search(request):
    if request.method == 'POST':
        search_type = request.POST["option"]
        text = request.POST["text"]
        users = User.objects.all()
        if search_type == "name":
            search_list = Recipe.objects.filter(
                name__icontains=text).order_by("name")
            message = "Searched By Name:"
        else:
            search_list = Recipe.objects.filter(
                ingredients__icontains=text).order_by("name")
            message = "Searched By Ingredient:"
        return render(request, 'cookbook/search.html', {
            "search_list": search_list,
            "mess": message,
            "users": users,
            "text": text
        })
    else:
        return render(request, 'cookbook/search.html')


def like(request):

    review_id = request.POST['id']
    like = request.POST['like']
    review = Review.objects.get(id=review_id)
    curr_user = request.user
    if like == "true":
        review.like.add(User.objects.get(username=curr_user))
    else:
        review.like.remove(User.objects.get(username=curr_user))
    return HttpResponse("done")


def follow(request, user):
    curr_user = request.user
    # add current user to user's followers list
    follows = (User.objects.get(id=user))
    follows.followers = F('followers') + 1
    follows.save()
    curr_user = request.user
    # add user to current users following list
    User.objects.get(username=curr_user).following.add(
        User.objects.get(id=user))

    return redirect("profile", profile=user)


def following(request):
    current_user = request.user
    user_obj = User.objects.get(username=current_user)
    following = user_obj.following.all()
    users = User.objects.all()
    follow_list = []
    for follow in following:
        follow_list.extend(follow.recipes.all())

    return render(request, 'cookbook/following.html', {
        "follow_list": follow_list,
        "users": users,
        "following": following
    })


def unfollow(request, user):
    user_to_unfollow = User.objects.get(id=user)

    curr_user = request.user
    current_user = User.objects.get(username=curr_user)

    user_to_unfollow.followers = F('followers') - 1
    user_to_unfollow.save()
    User.objects.get(username=curr_user).following.remove(user_to_unfollow)
    return redirect("profile", profile=user)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "cookbook/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cookbook/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "cookbook/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "cookbook/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cookbook/register.html")
