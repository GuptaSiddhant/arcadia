from django.contrib.auth import get_user_model
from rest_framework import viewsets

from api.serializers import UserSerializer, GameSerializer, GenreSerializer, \
    TransactionSerializer, GameStateSerializer, GameScoreSerializer
from app.models import Game, Genre, Transaction, GameState, GameScore


# ViewSet thats defines the User view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


# ViewSet thats defines the Game view behavior.
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


# ViewSet thats defines the Genre view behavior.
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


# ViewSet thats defines the Transation view behavior.
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


# ViewSet thats defines the GameState view behavior.
class GameStateViewSet(viewsets.ModelViewSet):
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer


# ViewSet thats defines the GameScore view behavior.
class GameScoreViewSet(viewsets.ModelViewSet):
    queryset = GameScore.objects.all()
    serializer_class = GameScoreSerializer
