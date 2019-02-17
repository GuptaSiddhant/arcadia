from django.test import TestCase
from app.models import User, Game, Genre, Transaction, GameScore, GameState
from datetime import datetime


# Test cases for the Arcadia system

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

        # create test games
        Game.objects.create(developer=User.objects.get(username="devuser"), genre=Genre.objects.get(name="Action"),
                            url="https://www.game.com/action", price=10, name="Action game",
                            image="https://www.game.com/image/action", description="Really nice game")

        Game.objects.create(developer=User.objects.get(username="devuser"), genre=Genre.objects.get(name="Arcade"),
                            url="https://www.game.com/arcade", price=10, name="Arcade game",
                            image="https://www.game.com/image/arcade", description="The best game on earth")

        # create test gamescores
        GameScore.objects.create(player=User.objects.get(username="playeruser"),
                                 game=Game.objects.get(name="Action game"),
                                 score=20)

        GameScore.objects.create(player=User.objects.get(username="playeruser"),
                                 game=Game.objects.get(name="Action game"),
                                 score=30)

        # create test transactions
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

        # create test gamestates
        GameState.objects.create(player=User.objects.get(username="playeruser"),
                                 game=Game.objects.get(name="Arcade game"),
                                 gameState='{"playerItems":["A rock","A rock","A rock"],"score":10}')

        GameState.objects.create(player=User.objects.get(username="playeruser"),
                                 game=Game.objects.get(name="Arcade game"),
                                 gameState='{"playerItems":["A paper","A paper","A paper"],"score":20}')

    # test the player high scrore function
    def test_player_high_score(self):
        self.assertEqual(Game.objects.get(name="Action game").player_high_score(
            player=User.objects.get(username="playeruser")), 30)

    # test the sale amount function
    def test_sale_amount(self):
        self.assertEqual(Game.objects.get(name="Action game").sale_amount(), 20)

    # test the sale_quantity function
    def test_sale_quantity(self):
        self.assertEqual(Game.objects.get(name="Action game").sale_quantity(), 2)

    # test last_save_date function when gamestate for a game does not exist
    def test_last_save_date_not_exist(self):
        self.assertEqual(Game.objects.get(name="Action game").last_save_date(player=User.objects.get
        (username="playeruser")), "No saves.")

    # test last_save_date function when gamestate for a game exist
    def test_last_save_date_exists(self):
        self.assertEqual(Game.objects.get(name="Arcade game").last_save_date(player=User.objects.get
        (username="playeruser")), datetime.now().strftime("%d-%m-%Y"))
