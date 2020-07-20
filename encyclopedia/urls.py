from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name = "search"),
    path("error",views.error, name = "error"),
    path("newpage", views.newpage, name = "newpage"),
    path("randomize", views.randomize, name = "randomize"),
    path("wiki/edit/<str:title>", views.edit, name = "edit"),
    path("wiki/<str:entry>", views.entry, name = "entry")
]
