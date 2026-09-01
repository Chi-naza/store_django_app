from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # import this to access the new user model we have created: settings.AUTH_USER_MODEL

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15,  null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

