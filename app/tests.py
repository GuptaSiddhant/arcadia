from django.test import TestCase
from app.models import User, Game, Genre, Transaction, GameScore, GameState

class ArcadiaTests(TestCase):
    # setup the test data
    def setUp(self):

        # create Admin user
        User.objects.create(username="adminuser", first_name="Admin", last_name="User", email="adminuser@gmail.com",
                            password="123456789", is_dev=True, is_superuser=True, email_confirmed=True)

        # create Developer user
        User.objects.create(username="devuser", first_name="Developer", last_name="User", email="devuser@gmail.com",
                            password="123456789", is_dev=True, email_confirmed=True)

        # create Player user
        User.objects.create(username="playeruser", first_name="Player", last_name="User", email="playeruser@gmail.com",
                            password="123456789", is_dev=False, email_confirmed=True)
        # create genres
        Genre.objects.create(name="Action")
        Genre.objects.create(name="Arcade")
        Genre.objects.create(name="Battle Royal")
        Genre.objects.create(name="Racing")
        Genre.objects.create(name="Shooting")

        # create games
        Game.objects.create(developer=User.objects.get(username="devuser"), genre=Genre.objects.get(name="Action"),
                            url="https://www.game.com/action", price=10, name="Action game",
                            image="https://www.game.com/image/action", description="Really nice game")

        Game.objects.create(developer=User.objects.get(username="devuser"), genre=Genre.objects.get(name="Arcade"),
                            url="https://www.game.com/arcade", price=10, name="Arcade game",
                            image="https://www.game.com/image/arcade", description="The best game on earth")

        # create GameScore
        GameScore.objects.create(player=User.objects.get(username="playeruser"),
                                 game=Game.objects.get(name="Action game"),
                                 score=20)

        GameScore.objects.create(player=User.objects.get(username="playeruser"),
                                game=Game.objects.get(name="Action game"),
                                score=30)

        #create transactions
        Transaction.objects.create(player=User.objects.get(username="playeruser"),
                                   game=Game.objects.get(name="Action game"),
                                   amount=Game.objects.get(name="Action game").price,
                                   payment_result="success")

        Transaction.objects.create(player=User.objects.get(username="playeruser"),
                                   game=Game.objects.get(name="Action game"),
                                   amount=Game.objects.get(name="Action game").price,
                                   payment_result="success")

        Transaction.objects.create(player=User.objects.get(username="playeruser"),
                                   game=Game.objects.get(name="Action game"),
                                   amount=Game.objects.get(name="Action game").price,
                                   payment_result="initialized")

    def test_player_high_score(self):
        self.assertEqual(Game.objects.get(name="Action game").player_high_score(
            player=User.objects.get(username="playeruser")), 30)

    def test_sale_amount(self):
        self.assertEqual(Game.objects.get(name="Action game").sale_amount(), 20)

    def test_sale_quantity(self):
        self.assertEqual(Game.objects.get(name="Action game").sale_quantity(), 2)
