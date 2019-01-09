from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    inventory = models.ManyToManyField('Game', default=None, blank=True)
    points_level = models.PositiveIntegerField(default=0)
    image = models.URLField(default="/static/media/no-image.png")


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='developer')
    inventory = models.ManyToManyField('Game', default=None, blank=True)


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    credit_bank_reference = models.TextField(max_length=100, blank=True)
    points_level = models.PositiveIntegerField(default=0)
    inventory = models.ManyToManyField('Game', default=None, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
            return Developer.objects.create(user=instance)
#        elif kwargs["user_type"] == "player":
#            return Developer.objects.create(user=instance)
#    post_save.connect(create_profile, sender=User)

#    if created:
#        if hasattr(instance, 'developer'):
#            Developer.objects.create(user=instance)
#        else:
#            Player.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:
        instance.developer.save()
#        elif kwargs["user_type"] == "player":
#            instance.player.save()


class Game(models.Model):
    url = models.URLField(unique=True)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, null=False)
    price = models.FloatField(default=0)
    name = models.CharField(max_length=100, unique=True)
    image = models.FilePathField(default="/static/media/no-image.png")
    description = models.TextField()
    highscore = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Transaction(models.Model):
    player = models.ForeignKey('Profile', on_delete=models.PROTECT, null=False)
    game = models.ForeignKey('Game', on_delete=models.PROTECT, null=False)
    amount = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now=False)


class GameState(models.Model):
    player = models.ForeignKey('Profile', on_delete=models.CASCADE, null=False)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, null=False)
    settings = models.TextField()
    score = models.PositiveIntegerField(default=0)
    game_state = models.TextField()

