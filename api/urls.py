from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from api.views import UserViewSet, GameViewSet, GenreViewSet, TransactionViewSet, GameStateViewSet, GameScoreViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')
router.register(r'games', GameViewSet, base_name='game')
router.register(r'genres', GenreViewSet, base_name='genre')
router.register(r'transactions', TransactionViewSet, base_name='transaction')
router.register(r'gamestates', GameStateViewSet, base_name='gamestate')
router.register(r'gamescores', GameScoreViewSet, base_name='gamescore')

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]
