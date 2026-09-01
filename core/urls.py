from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("hello/", views.say_hello),
    path("users/", views.UsersListView.as_view()),
]