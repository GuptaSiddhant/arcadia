from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import Game, Genre, Transaction, GameState, GameScore


# Serializer for User model to define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = get_user_model()
        fields = [field.name for field in model._meta.fields]
        fields.append('url')


# Serializer for Game model to define the API representation.
class GameSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='game-detail')

    class Meta:
        model = Game
        fields = [field.name for field in model._meta.fields]
        fields.append('url')


# Serializer for Genre model to define the API representation.
class GenreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='genre-detail')

    class Meta:
        model = Genre
        fields = [field.name for field in model._meta.fields]
        fields.append('url')


# Serializer for Transaction model to define the API representation.
class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='transaction-detail')

    class Meta:
        model = Transaction
        fields = [field.name for field in model._meta.fields]
        fields.append('url')


# Serializer for GameState model to define the API representation.
class GameStateSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gamestate-detail')

    class Meta:
        model = GameState
        fields = [field.name for field in model._meta.fields]
        fields.append('url')


# Serializer for GameScore model to define the API representation.
class GameScoreSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='gamescore-detail')

    class Meta:
        model = GameScore
        fields = [field.name for field in model._meta.fields]
        fields.append('url')
