from django.db import models
from django.contrib.auth.models import AbstractUser

class RegisterableEmail(models.Model):
    email = models.EmailField(unique=True, blank=True)

class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=True)

    # A AJOUTER
    #genre
    #date de naissance
    #age

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    points = models.IntegerField(default=0)
    current_level = models.CharField(max_length=20, default='beginner')
    verified = models.BooleanField(default=False)


