from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

class UserLevel(Enum):
    """Énumération des niveaux d'utilisateur basés sur les points"""
    BEGINNER = (0, "Débutant")
    INTERMEDIATE = (100, "Intermédiaire")
    ADVANCED = (500, "Avancé")
    EXPERT = (1000, "Expert")

    def __init__(self, min_points, label):
        self.min_points = min_points
        self.label = label

class RegisterableEmail(models.Model):
    email = models.EmailField(unique=True, blank=True)

class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    birthdate = models.DateField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    points = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)

    @property
    def current_level(self):
        """Retourne le niveau actuel en fonction des points"""
        for level in sorted(UserLevel, key=lambda l: l.min_points, reverse=True):
            if self.points >= level.min_points:
                return level
        return UserLevel.BEGINNER

    def get_level_label(self):
        """Retourne l'étiquette du niveau actuel"""
        return self.current_level.label

    def get_level_name(self):
        """Retourne le nom du niveau actuel"""
        return self.current_level.name
    
    def add_points(self, amount: int):
        self.points += amount
        self.save(update_fields=['points'])
