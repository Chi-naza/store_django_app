from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # import this to access the new user model we have created: settings.AUTH_USER_MODEL

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
