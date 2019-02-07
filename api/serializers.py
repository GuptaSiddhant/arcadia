from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import Game, Genre, Transaction, GameState, GameScore


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = get_user_model()
        fields = [field.name for field in model._meta.fields]
        fields.append('url')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='game-detail')

    class Meta:
        model = Game
        fields = [field.name for field in model._meta.fields]
        fields.append('url')


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='genre-detail')

    # many = True
    class Meta:
        model = Genre
        fields = [field.name for field in model._meta.fields]
        fields.append('url')


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='transaction-detail')

    # many = True
    class Meta:
        model = Transaction
        fields = [field.name for field in model._meta.fields]
        fields.append('url')


class GameStateSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gamestate-detail')

    # many = True
    class Meta:
        model = GameState
        fields = [field.name for field in model._meta.fields]
        fields.append('url')


class GameScoreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gamescore-detail')
    many = True

    class Meta:
        model = GameScore
        fields = [field.name for field in model._meta.fields]
        fields.append('url')
