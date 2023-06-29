from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<title>", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("newpage/", views.newpage, name="newpage"),
    path("editpage/", views.editpage, name="editpage"),
    path("random/", views.random, name="random")
]
