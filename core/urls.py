from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("hello/", views.say_hello),
    path("api/auth/registration/account-confirm-email/verify-email/", views.CustomVerifyEmailView.as_view(), name='rest_verify_email'),
]