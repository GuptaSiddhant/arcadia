from django.contrib import admin

from app.models import User, Game, Genre, Transaction, GameState, GameScore


# Define an inline admin descriptor for User model
# which acts a bit like a singleton
class UserInline(admin.StackedInline):
    model = User
    verbose_name_plural = 'users'


admin.site.register(User)
admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(Transaction)
admin.site.register(GameState)
admin.site.register(GameScore)
