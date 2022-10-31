from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("random", views.random, name="random"),
    path("<str:entry>", views.entry, name="entry"),
    path("<str:entry>/edit", views.edit, name="edit"),
    path("search/", views.search, name="search")
]
