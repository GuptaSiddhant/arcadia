from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    inventory = models.ManyToManyField('Game', default=None, blank=True)
    points_level = models.PositiveIntegerField(default=0)
    image = models.URLField(default=None, blank=True)
    is_dev = models.BooleanField(default=False)


class Game(models.Model):
    developer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, null=False)
    url = models.URLField(unique=True)
    price = models.FloatField(default=0)
    name = models.CharField(max_length=100, unique=True)
    image = models.URLField(default=None, blank=True)
    description = models.TextField()
    highscore = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Transaction(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False)
    game = models.ForeignKey('Game', on_delete=models.PROTECT, null=False)
    amount = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
    payment_reference = models.PositiveIntegerField(default=0)
    payment_result = models.CharField(max_length=50)


class GameState(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, null=False)
    settings = models.TextField()
    game_state = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)


class GameScore(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, null=False)
    score = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
