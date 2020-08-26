from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import F
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import User, Post


def index(request):

    if request.method == "POST":
        text = request.POST["newPost"]
        current_user = request.user
        post = Post.objects.create(user=current_user, text=text)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        posts_lists = Post.objects.all().order_by("-time")
        paginator = Paginator(posts_lists, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        current_user = request.user
        return render(request, "network/index.html", {
            'page_obj': page_obj,
            'curr_user': current_user,
        })


def edit(request):
    post_id = request.POST['id']
    text = request.POST["text"]

    post = Post.objects.get(id=post_id)
    post.text = text
    post.save()
    return HttpResponse("done")


def like(request):
    post_id = request.POST['id']
    like = request.POST['like']
    post = Post.objects.get(id=post_id)
    curr_user = request.user
    if like == "true":
        post.like.add(User.objects.get(username=curr_user))
    else:
        post.like.remove(User.objects.get(username=curr_user))
    return HttpResponse("done")


def following(request):
    current_user = request.user
    if str(current_user) == "AnonymousUser":
        page_obj = None
    else:
        # user__in is used to match a query to a list of things.
        posts_lists = Post.objects.filter(
            user__in=current_user.following.all()).order_by("-time")
        paginator = Paginator(posts_lists, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {

        "page_obj": page_obj,
        "curr_user": current_user
    })


def follow(request, user):

    curr_user = request.user
    # add current user to user's followers list
    follows = (User.objects.get(username=user))
    follows.followers = F('followers') + 1
    follows.save()
    curr_user = request.user
    # add user to current users following list
    User.objects.get(username=curr_user).following.add(
        User.objects.get(username=user))

    return HttpResponseRedirect("/profile/" + user)


def unfollow(request, user):
    user_to_unfollow = User.objects.get(username=user)

    curr_user = request.user
    current_user = User.objects.get(username=curr_user)

    user_to_unfollow.followers = F('followers') - 1
    user_to_unfollow.save()
    User.objects.get(username=curr_user).following.remove(user_to_unfollow)
    return HttpResponseRedirect("/profile/" + user)


def profile(request, profile):
    user = User.objects.get(username=profile)
    curr_user = request.user
    follow = True
    unfollow = False
    if user == curr_user or str(curr_user) == "AnonymousUser":
        follow = False
    elif user in curr_user.following.all():
        unfollow = True

    posts_lists = Post.objects.filter(user=user).order_by("-time")
    paginator = Paginator(posts_lists, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "curr_user": curr_user,
        "user": user,
        "follow": follow,
        "unfollow": unfollow,
        "page_obj": page_obj
    })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
