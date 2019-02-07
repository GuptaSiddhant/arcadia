from django.contrib.auth import get_user_model
from rest_framework import viewsets

from api.serializers import UserSerializer, GameSerializer, GenreSerializer, \
    TransactionSerializer, GameStateSerializer, GameScoreSerializer
from app.models import Game, Genre, Transaction, GameState, GameScore


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class GameStateViewSet(viewsets.ModelViewSet):
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer


class GameScoreViewSet(viewsets.ModelViewSet):
    queryset = GameScore.objects.all()
    serializer_class = GameScoreSerializer
