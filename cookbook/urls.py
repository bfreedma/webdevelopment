from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<str:recipe>", views.recipe, name="recipe"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("following", views.following, name="following"),
    path("follow/<str:user>", views.follow, name="follow"),
    path("unfollow/<str:user>", views.unfollow, name="unfollow"),
    path("search", views.search, name="search"),
    path("like", views.like, name="like"),
    path("editreview", views.editreview, name="editreview"),
    path("editrecipe/<str:recipe_id>",views.editrecipe, name="editrecipe"),
    path("register", views.register, name="register"),
    path("createrecipe", views.createrecipe, name="createrecipe"),
    path("profile/<str:profile>", views.profile, name="profile")
]