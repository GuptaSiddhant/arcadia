from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    inventory = models.ManyToManyField('Game', default=None, blank=True)
    points_level = models.PositiveIntegerField(default=0)
    image = models.URLField(blank=True, null=True, default='https://pngimage.net/wp-content/uploads/'
                                                           '2018/05/default-user-profile-image-png-2.png')
    is_dev = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    def transactions_all(self):
        return self.transaction_set.all().order_by('timestamp')

    def amount_spent(self):
        transactions = self.transaction_set.filter(payment_result='success')
        amount = 0
        for transaction in transactions:
            amount += transaction.amount
        return amount

    def transactions_dev(self):
        games = self.game_set.all()
        transactions = []
        for game in games:
            transactions += game.transaction_set.all()
        return sorted(transactions, key=lambda instance: instance.timestamp)

    def total_sale(self):
        games = self.game_set.all()
        quantity = 0
        for game in games:
            quantity += game.sale_quantity()
        return quantity

    def amount_earned(self):
        games = self.game_set.all()
        amount = 0
        for game in games:
            amount += game.sale_amount()
        return amount


class Game(models.Model):
    developer = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, null=False)
    url = models.URLField(unique=True, null=False)
    price = models.FloatField(default=0)
    name = models.CharField(max_length=100, unique=True)
    image = models.URLField(default=None, blank=True)
    description = models.TextField(null=False)
    high_score = models.OneToOneField('GameScore', on_delete=models.PROTECT, related_name='high_score_in', blank=True,
                                      null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name', 'genre']

    def scores(self):
        return self.gamescore_set.order_by('-score')[:5]

    def last_save_date(self, player):
        save_date = self.gamestate_set.filter(player=player).order_by('-saveDate').first()
        if save_date is None:
            return 'No saves.'
        return save_date.saveDate.strftime("%d-%m-%Y")

    def player_high_score(self, player):
        game_score = self.gamescore_set.filter(player=player).order_by('-score').first()
        if game_score is None:
            return 0
        return game_score.score

    def sale_quantity(self):
        transactions = self.transaction_set.filter(payment_result='success')
        return transactions.count()

    def sale_amount(self):
        transactions = self.transaction_set.filter(payment_result='success')
        amount = 0
        for transaction in transactions:
            amount += transaction.amount
        return amount

    def __str__(self):
        return str(self.name)


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Transaction(models.Model):
    player = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    game = models.ForeignKey('Game', on_delete=models.PROTECT, null=False)
    amount = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
    payment_reference = models.PositiveIntegerField(default=0)
    payment_result = models.CharField(max_length=50)


class GameState(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, null=False)
    gameState = models.TextField()
    saveDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.game.name + '_' + str(self.pk) + '.save')


class GameScore(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, null=False)
    score = models.PositiveIntegerField(default=0)
    scoreDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.player.username + ": " + str(self.score))
