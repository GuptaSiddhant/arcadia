from django.contrib import admin

from app.models import Player, Developer, Game, Genre, Transaction, GameState

# Define an inline admin descriptor for Player model
# which acts a bit like a singleton
class PlayerInline(admin.StackedInline):
    model = Player
    verbose_name_plural = 'players'

# Define an inline admin descriptor for Player model
# which acts a bit like a singleton
class DeveloperInline(admin.StackedInline):
    model = Developer
    verbose_name_plural = 'developers'

admin.site.register(Player)
admin.site.register(Developer)
admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(Transaction)
admin.site.register(GameState)
